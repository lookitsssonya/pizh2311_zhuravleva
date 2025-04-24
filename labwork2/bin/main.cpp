
#include <lib/number.h>
#include <iostream>

int main() {
    uint2022_t a = from_uint(42);
    uint2022_t b = from_uint(5);
    uint2022_t c = from_string("15");
    uint2022_t d = from_string("6");

    std::cout << "42 + 5 = " << (a + b) << "\n";
    std::cout << "42 - 5 = " << (a - b) << "\n";
    std::cout << "42 * 5 = " << (a * b) << "\n";


    std::cout << "15 + 6 = " << (c + d) << "\n";
    std::cout << "15 - 6 = " << (c - d) << "\n";
    std::cout << "15 * 6 = " << (c * d) << "\n";



    std::cout << "42 == 5? " << (a == b ? "true" : "false") << "\n";
    std::cout << "42 != 5? " << (a != b ? "true" : "false") << "\n";

    return 0;
}