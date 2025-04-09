#include <iostream>
#include <fstream>
#include <string>

int main(int argc, char* argv[]) {
    bool count_lines = false;
    bool count_words = false;
    bool count_bytes = false;
    bool count_chars = false;
    std::string filename;

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "-l") count_lines = true;
        else if (arg == "-w") count_words = true;
        else if (arg == "-c") count_bytes = true;
        else if (arg == "-m") count_chars = true;
        else filename = arg;
    }

    if (!count_lines && !count_words && !count_bytes && !count_chars) {
        count_lines = count_words = count_bytes = true;
    }

    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: could not open file " << filename << std::endl;
        return 1;
    }

    int lines = 0, words = 0, bytes = 0, chars = 0;
    std::string line;

    while (getline(file, line)) {
        lines++;
        bytes += line.length() + 1; 
        chars += line.length() + 1; 

        bool in_word = false;
        for (char c : line) {
            if (isspace(c)) {
                in_word = false;
            }
            else if (!in_word) {
                words++;
                in_word = true;
            }
        }
    }

    if (count_lines) std::cout << lines << " ";
    if (count_words) std::cout << words << " ";
    if (count_bytes) std::cout << bytes << " ";
    if (count_chars) std::cout << chars << " ";
    std::cout << filename << std::endl;

    file.close();
    return 0;
}
