#include "number.h"
#include <string>
#include <algorithm>
#include <stdexcept>

uint2022_t from_uint(uint32_t i) {
    uint2022_t result;
    result.parts[0] = i;
    return result;
}

uint2022_t from_string(const char* buff) {
    uint2022_t result;
    std::string str(buff);

    if (str.empty()) {
        return result;
    }

    for (char c : str) {
        if (!isdigit(c)) {
            throw std::invalid_argument("Invalid character in input string");
        }
    }

    for (size_t i = 0; i < str.size(); ++i) {
        uint32_t carry = 0;
        for (size_t j = 0; j < result.kDigits; ++j) {
            uint64_t value = static_cast<uint64_t>(result.parts[j]) * 10 + carry;
            result.parts[j] = static_cast<uint32_t>(value & 0xFFFFFFFF);
            carry = static_cast<uint32_t>(value >> 32);
        }

        if (carry != 0) {
            throw std::overflow_error("Number too large for uint2022_t");
        }

        uint32_t digit = str[i] - '0';
        carry = digit;
        for (size_t j = 0; j < result.kDigits && carry != 0; ++j) {
            uint64_t sum = static_cast<uint64_t>(result.parts[j]) + carry;
            result.parts[j] = static_cast<uint32_t>(sum & 0xFFFFFFFF);
            carry = static_cast<uint32_t>(sum >> 32);
        }

        if (carry != 0) {
            throw std::overflow_error("Number too large for uint2022_t");
        }
    }

    return result;
}

uint2022_t operator+(const uint2022_t& lhs, const uint2022_t& rhs) {
    uint2022_t result;
    uint32_t carry = 0;

    for (size_t i = 0; i < lhs.kDigits; ++i) {
        uint64_t sum = static_cast<uint64_t>(lhs.parts[i]) + rhs.parts[i] + carry;
        result.parts[i] = static_cast<uint32_t>(sum & 0xFFFFFFFF);
        carry = static_cast<uint32_t>(sum >> 32);
    }

    if (carry != 0) {
        throw std::overflow_error("Addition overflow in uint2022_t");
    }

    return result;
}

uint2022_t operator-(const uint2022_t& lhs, const uint2022_t& rhs) {
    uint2022_t result;
    uint32_t borrow = 0;

    for (size_t i = 0; i < lhs.kDigits; ++i) {
        uint64_t diff = static_cast<uint64_t>(lhs.parts[i]) - rhs.parts[i] - borrow;
        result.parts[i] = static_cast<uint32_t>(diff & 0xFFFFFFFF);
        borrow = (diff >> 32) ? 1 : 0;
    }

    if (borrow != 0) {
        throw std::underflow_error("Subtraction underflow in uint2022_t");
    }

    return result;
}

uint2022_t operator*(const uint2022_t& lhs, const uint2022_t& rhs) {
    uint2022_t result;

    for (size_t i = 0; i < lhs.kDigits; ++i) {
        uint32_t carry = 0;
        for (size_t j = 0; j < rhs.kDigits; ++j) {
            if (i + j >= result.kDigits) continue;

            uint64_t product = static_cast<uint64_t>(lhs.parts[i]) * rhs.parts[j] +
                result.parts[i + j] + carry;
            result.parts[i + j] = static_cast<uint32_t>(product & 0xFFFFFFFF);
            carry = static_cast<uint32_t>(product >> 32);
        }
    }

    return result;
}

uint2022_t operator/(const uint2022_t& lhs, const uint2022_t& rhs) {
    if (rhs == from_uint(0)) {
        throw std::invalid_argument("Division by zero");
    }

    uint2022_t quotient;
    uint2022_t remainder;
    uint2022_t divisor = rhs;

    for (int i = lhs.kDigits * 32 - 1; i >= 0; --i) {
        uint32_t carry = 0;
        for (int j = 0; j < remainder.kDigits; ++j) {
            uint32_t new_carry = remainder.parts[j] >> 31;
            remainder.parts[j] = (remainder.parts[j] << 1) | carry;
            carry = new_carry;
        }

        if ((lhs.parts[i / 32] >> (i % 32)) & 1) {
            remainder.parts[0] |= 1;
        }

        bool can_subtract = true;
        for (int j = divisor.kDigits - 1; j >= 0; --j) {
            if (remainder.parts[j] > divisor.parts[j]) {
                break;
            }
            else if (remainder.parts[j] < divisor.parts[j]) {
                can_subtract = false;
                break;
            }
        }

        if (can_subtract) {
            remainder = remainder - divisor;
            quotient.parts[i / 32] |= (1 << (i % 32));
        }
    }

    return quotient;
}

bool operator==(const uint2022_t& lhs, const uint2022_t& rhs) {
    for (size_t i = 0; i < lhs.kDigits; ++i) {
        if (lhs.parts[i] != rhs.parts[i]) {
            return false;
        }
    }
    return true;
}

bool operator!=(const uint2022_t& lhs, const uint2022_t& rhs) {
    return !(lhs == rhs);
}

std::ostream& operator<<(std::ostream& stream, const uint2022_t& value) {
    if (value == from_uint(0)) {
        stream << "0";
        return stream;
    }

    uint2022_t tmp = value;
    std::string result;

    while (tmp != from_uint(0)) {
        uint32_t remainder = 0;
        for (int i = tmp.kDigits - 1; i >= 0; --i) {
            uint64_t value = (static_cast<uint64_t>(remainder) << 32) + tmp.parts[i];
            tmp.parts[i] = static_cast<uint32_t>(value / 10);
            remainder = static_cast<uint32_t>(value % 10);
        }
        result.push_back(remainder + '0');
    }

    std::reverse(result.begin(), result.end());
    stream << result;

    return stream;
}
