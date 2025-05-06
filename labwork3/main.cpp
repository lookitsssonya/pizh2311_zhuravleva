#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <filesystem>
#include <algorithm>
#include <cstdint>
#include <cstring>

namespace fs = std::filesystem;

std::vector<std::vector<uint64_t>> read_initial_state(uint16_t length, uint16_t width,
    const std::string& input_file) {
    std::vector<std::vector<uint64_t>> grid(width, std::vector<uint64_t>(length, 0));

    std::ifstream file(input_file);
    if (!file.is_open()) {
        std::cerr << "Error: Cannot open input file '" << input_file << "': "
            << strerror(errno) << "\n";
        throw std::runtime_error("File open failed");
    }

    uint16_t x, y;
    uint64_t value;
    while (file >> x >> y >> value) {
        if (x >= length || y >= width) {
            std::cerr << "Warning: Coordinates (" << x << "," << y
                << ") out of bounds, skipping\n";
            continue;
        }
        grid[y][x] = value;
    }

    return grid;
}

uint32_t get_color(uint64_t grains) {
    if (grains == 0) return 0xFFFFFF; 
    if (grains == 1) return 0x00FF00; 
    if (grains == 2) return 0xFF00FF; 
    if (grains == 3) return 0xFFFF00; 
    return 0x000000; 
}

void save_to_bmp(const std::vector<std::vector<uint64_t>>& grid,
    const std::string& filename) {
    try {
        uint16_t width = static_cast<uint16_t>(grid.empty() ? 0 : grid[0].size());
        uint16_t height = static_cast<uint16_t>(grid.size());

        if (width == 0 || height == 0) {
            std::cerr << "Error: Empty grid, cannot save BMP\n";
            return;
        }

#pragma pack(push, 1)
        struct BMPHeader {
            uint16_t file_type = 0x4D42;
            uint32_t file_size = 0;
            uint16_t reserved1 = 0;
            uint16_t reserved2 = 0;
            uint32_t offset_data = 54;

            uint32_t header_size = 40;
            int32_t width = 0;
            int32_t height = 0;
            uint16_t planes = 1;
            uint16_t bit_count = 24;
            uint32_t compression = 0;
            uint32_t image_size = 0;
            int32_t x_pixels_per_meter = 0;
            int32_t y_pixels_per_meter = 0;
            uint32_t colors_used = 0;
            uint32_t colors_important = 0;
        };
#pragma pack(pop)

        BMPHeader header;
        header.width = width;
        header.height = height;

        uint32_t row_stride = (width * 3 + 3) & ~3;
        header.image_size = row_stride * height;
        header.file_size = header.offset_data + header.image_size;

        fs::create_directories(fs::path(filename).parent_path());

        std::ofstream file(filename, std::ios::binary);
        if (!file) {
            std::cerr << "Error: Failed to create file '" << filename
                << "': " << strerror(errno) << "\n";
            return;
        }

        file.write(reinterpret_cast<const char*>(&header), sizeof(header));
        if (!file) {
            std::cerr << "Error: Failed to write BMP header\n";
            return;
        }

        std::vector<uint8_t> row(row_stride, 0);
        for (int y = height - 1; y >= 0; --y) {
            for (int x = 0; x < width; ++x) {
                uint32_t color = get_color(grid[y][x]);
                row[x * 3 + 0] = static_cast<uint8_t>(color);
                row[x * 3 + 1] = static_cast<uint8_t>(color >> 8);
                row[x * 3 + 2] = static_cast<uint8_t>(color >> 16);
            }
            file.write(reinterpret_cast<const char*>(row.data()), row_stride);
        }

        std::cout << "Saved: " << filename << "\n";
    }
    catch (const std::exception& e) {
        std::cerr << "Error in save_to_bmp: " << e.what() << "\n";
    }
}

bool is_stable(const std::vector<std::vector<uint64_t>>& grid) {
    for (const auto& row : grid) {
        for (uint64_t grains : row) {
            if (grains > 3) return false;
        }
    }
    return true;
}

void sandpile_iteration(std::vector<std::vector<uint64_t>>& grid) {
    std::vector<std::pair<uint16_t, uint16_t>> to_update;

    for (uint16_t y = 0; y < grid.size(); ++y) {
        for (uint16_t x = 0; x < grid[y].size(); ++x) {
            if (grid[y][x] > 3) {
                to_update.emplace_back(x, y);
            }
        }
    }

    for (const auto& [x, y] : to_update) {
        uint64_t grains = grid[y][x];
        uint64_t to_transfer = grains / 4;
        grid[y][x] = grains % 4;

        if (y > 0) grid[y - 1][x] += to_transfer;
        if (y < grid.size() - 1) grid[y + 1][x] += to_transfer;
        if (x > 0) grid[y][x - 1] += to_transfer;
        if (x < grid[y].size() - 1) grid[y][x + 1] += to_transfer;
    }
}

void print_usage(const char* program_name) {
    std::cerr << "Usage: " << program_name << " -l LENGTH -w WIDTH -i INPUT_FILE [-o OUTPUT_DIR] [-m MAX_ITER] [-f FREQ]\n"
        << "Required:\n"
        << "  -l, --length    Grid length\n"
        << "  -w, --width     Grid width\n"
        << "  -i, --input     Input TSV file\n"
        << "Optional:\n"
        << "  -o, --output    Output directory (default: 'output')\n"
        << "  -m, --max-iter  Maximum iterations (default: 1000)\n"
        << "  -f, --freq      Save frequency (default: 10)\n";
}

int main(int argc, char* argv[]) {
    uint16_t length = 0;
    uint16_t width = 0;
    std::string input_file;
    std::string output_dir = "output";
    uint32_t max_iter = 1000;
    uint32_t freq = 10;

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];

        if (arg == "-l" || arg == "--length") {
            if (i + 1 < argc) length = static_cast<uint16_t>(std::stoi(argv[++i]));
        }
        else if (arg == "-w" || arg == "--width") {
            if (i + 1 < argc) width = static_cast<uint16_t>(std::stoi(argv[++i]));
        }
        else if (arg == "-i" || arg == "--input") {
            if (i + 1 < argc) input_file = argv[++i];
        }
        else if (arg == "-o" || arg == "--output") {
            if (i + 1 < argc) output_dir = argv[++i];
        }
        else if (arg == "-m" || arg == "--max-iter") {
            if (i + 1 < argc) max_iter = static_cast<uint32_t>(std::stoi(argv[++i]));
        }
        else if (arg == "-f" || arg == "--freq") {
            if (i + 1 < argc) freq = static_cast<uint32_t>(std::stoi(argv[++i]));
        }
        else {
            std::cerr << "Unknown option: " << arg << "\n";
            print_usage(argv[0]);
            return 1;
        }
    }

    if (length == 0 || width == 0 || input_file.empty()) {
        std::cerr << "Error: Missing required arguments\n";
        print_usage(argv[0]);
        return 1;
    }

    try {
        fs::create_directories(output_dir);
        std::cout << "Output directory: " << fs::absolute(output_dir) << "\n";

        std::cout << "Loading initial state from: " << fs::absolute(input_file) << "\n";
        auto grid = read_initial_state(length, width, input_file);

        for (uint32_t iter = 0; iter <= max_iter; ++iter) {
            bool should_save = (freq > 0 && iter % freq == 0) || iter == max_iter;

            if (should_save) {
                std::string filename = output_dir + "/iter_" + std::to_string(iter) + ".bmp";
                save_to_bmp(grid, filename);
            }

            if (is_stable(grid)) {
                std::cout << "Model stabilized after " << iter << " iterations\n";
                save_to_bmp(grid, output_dir + "/final.bmp");
                break;
            }

            sandpile_iteration(grid);
        }

    }
    catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
        return 1;
    }

    return 0;
}