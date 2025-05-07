#include <stdexcept>
#include "ArgParser.h"
#include <iostream>
#include <string>
#include <sstream>

namespace ArgumentParser {

    ArgParser::ArgParser(std::string program_name)
        : program_name_(std::move(program_name)), help_requested_(false) {
    }

    ArgParser::ArgParser(char short_name, const std::string name)
        : program_name_(name), help_requested_(false) {
    }

    ArgParser::ArgParser() : help_requested_(false) {}

    ArgParser::~ArgParser() {}

    ArgParser& ArgParser::AddStringArgument(const std::string& long_name) {
        Argument arg;
        arg.long_name = long_name;
        arg.is_flag = false;
        arg.is_set = false;
        arg.value_str = new std::string;
        arguments_.push_back(std::move(arg));
        return *this;
    }

    ArgParser& ArgParser::AddStringArgument(char short_name, const std::string& long_name) {
        Argument arg;
        arg.long_name = long_name;
        arg.short_name = short_name;
        arg.is_flag = false;
        arg.is_set = false;
        arg.value_str = new std::string;
        arguments_.push_back(std::move(arg));
        return *this;
    }

    ArgParser& ArgParser::AddStringArgument(char short_name, const std::string& long_name, const std::string& description) {
        Argument arg;
        arg.short_name = short_name;
        arg.long_name = long_name;
        arg.description = description;
        arg.is_flag = false;
        arguments_.push_back(std::move(arg));
        return *this;
    }

    ArgParser& ArgParser::AddIntArgument(const std::string& long_name) {
        Argument arg;
        arg.long_name = long_name;
        arg.is_flag = false;
        arg.is_set = false;
        arg.value_int = new std::vector<int>();
        arguments_.push_back(std::move(arg));
        return *this;
    }

    ArgParser& ArgParser::AddIntArgument(char short_name, const std::string& long_name) {
        Argument arg;
        arg.long_name = long_name;
        arg.short_name = short_name;
        arg.is_flag = false;
        arg.is_set = false;
        arg.value_int = new std::vector<int>();
        arguments_.push_back(std::move(arg));
        return *this;
    }

    ArgParser& ArgParser::AddIntArgument(const std::string& long_name, const std::string& help_description_) {
        Argument arg;
        arg.long_name = long_name;
        arg.is_flag = false;
        arg.is_set = false;
        arg.value_int = new std::vector<int>();
        arguments_.push_back(std::move(arg));
        return *this;
    }

    ArgParser& ArgParser::AddFlag(char short_name, const std::string& long_name) {
        Argument arg;
        arg.long_name = long_name;
        arg.short_name = short_name;
        arg.is_flag = true;
        arg.is_set = false;
        arg.value_bool = new bool(false);
        arguments_.push_back(std::move(arg));
        return *this;
    }

    ArgParser& ArgParser::AddFlag(char short_name, const std::string& long_name, const std::string& description) {
        Argument arg;
        arg.long_name = long_name;
        arg.short_name = short_name;
        arg.is_flag = true;
        arg.is_set = false;
        arg.value_bool = new bool(false);
        arguments_.push_back(std::move(arg));
        return *this;
    }

    ArgParser& ArgParser::AddFlag(const std::string long_name, const std::string& long_name_) {
        Argument arg;
        arg.long_name = long_name;
        arg.short_name = '\0';
        arg.is_flag = true;
        arg.is_set = false;
        arg.value_bool = new bool(false);
        arguments_.push_back(std::move(arg));
        return *this;
    }

    ArgParser& ArgParser::StoreValue(std::string& value) {
        if (arguments_.empty()) throw std::logic_error("No argument to store value for.");
        auto& arg = arguments_.back();
        if (arg.is_flag) throw std::logic_error("Attempt to store string value in flag argument.");
        arg.value_str = &value;
        return *this;
    }

    ArgParser& ArgParser::StoreValue(bool& value) {
        if (arguments_.empty()) throw std::logic_error("No argument to store value for.");
        auto& arg = arguments_.back();
        if (!arg.is_flag) throw std::logic_error("Attempt to store bool value in non-flag argument.");
        arg.value_bool = &value;
        return *this;
    }

    ArgParser& ArgParser::StoreValues(std::vector<int>& values) {
        if (arguments_.empty()) throw std::logic_error("No argument to store values for.");
        auto& arg = arguments_.back();
        if (arg.is_flag) throw std::logic_error("Attempt to store int values in flag argument.");
        arg.value_int = &values;
        return *this;
    }

    ArgParser& ArgParser::MultiValue(size_t min_values) {
        if (arguments_.empty()) throw std::logic_error("No argument to set multi-value for.");
        arguments_.back().min_values = min_values;
        return *this;
    }

    ArgParser& ArgParser::Positional() {
        if (arguments_.empty()) throw std::logic_error("No argument to set as positional.");
        arguments_.back().is_positional = true;
        return *this;
    }

    ArgParser& ArgParser::Default(bool default_flag) {
        if (arguments_.empty() || !arguments_.back().is_flag) throw std::logic_error("privet");
        arguments_.back().default_value_bool = default_flag;
        return *this;
    }

    ArgParser& ArgParser::Default(const char* default_value) {
        if (arguments_.empty()) throw std::logic_error("No string argument to set default value for.");
        auto& lastArg = arguments_.back();
        if (!lastArg.is_flag) {
            lastArg.default_value_str = default_value;
            if (!lastArg.is_set && lastArg.value_str) {
                *lastArg.value_str = default_value;
            }
        }
        return *this;
    }

    std::string ArgParser::GetStringValue(const std::string& arg_name, const std::string& default_value) const {
        for (const auto& arg : arguments_) {
            if (arg.long_name == arg_name && arg.value_str) return *arg.value_str;
        }
        return default_value;
    }

    int ArgParser::GetIntValue(const std::string& arg_name, int default_value) const {
        for (const auto& arg : arguments_) {
            if (arg.long_name == arg_name && arg.value_int) {
                if (!arg.value_int->empty()) return arg.value_int->front();
                return default_value;
            }
        }
        return default_value;
    }

    bool ArgParser::GetFlag(const std::string& arg_name) const {
        for (const auto& arg : arguments_) {
            if (arg.long_name == arg_name && arg.is_flag) {
                if (arg.value_bool) return *(arg.value_bool);
                return arg.default_value_bool;
            }
        }
        return false;
    }

    ArgParser& ArgParser::AddHelp(char short_name, const std::string& long_name, const std::string& description) {
        Argument help_argument;
        help_argument.long_name = long_name;
        help_argument.short_name = short_name;
        help_argument.description = description;
        help_argument.is_flag = true;
        help_argument.is_help = true;
        help_argument.value_bool = &help_requested_;
        arguments_.push_back(std::move(help_argument));
        return *this;
    }

    bool ArgParser::Help() const {
        return help_requested_;
    }

    std::string ArgParser::HelpDescription() const {
        std::ostringstream help_stream;
        help_stream << program_name_ << "\n";
        if (!help_description_.empty()) help_stream << help_description_ << "\n\n";

        for (const auto& arg : arguments_) {
            if (arg.short_name != '\0') help_stream << "-" << arg.short_name << ", ";
            if (!arg.long_name.empty()) {
                help_stream << "--" << arg.long_name;
                if (!arg.is_flag) help_stream << "=<" << (arg.value_str ? "string" : "int") << ">";
            }
            if (!arg.description.empty()) help_stream << ", " << arg.description;
            if (arg.min_values > 0) help_stream << " [repeated, min args = " << arg.min_values << "]";
            if (arg.is_flag && arg.default_value_bool) help_stream << " [default = true]";
            help_stream << "\n";
        }

        help_stream << "\n-h, --help Display this help and exit\n";
        return help_stream.str();
    }

    bool ArgParser::ProcessLongArgument(const std::string& arg) {
        size_t equal_pos = arg.find('=');
        std::string key = arg.substr(2, equal_pos - 2);
        std::string value = (equal_pos != std::string::npos) ? arg.substr(equal_pos + 1) : "true";

        for (auto& argument : arguments_) {
            if (argument.long_name == key) {
                if (argument.is_flag) {
                    if (equal_pos != std::string::npos) return false;
                    if (argument.value_bool) *(argument.value_bool) = true;
                }
                else {
                    if (equal_pos == std::string::npos) return false;
                    if (argument.value_int != nullptr) {
                        char* end = nullptr;
                        long val = strtol(value.c_str(), &end, 10);
                        if (end != value.c_str() && *end == '\0' && val >= INT_MIN && val <= INT_MAX) {
                            argument.value_int->push_back(static_cast<int>(val));
                        }
                        else {
                            return false;
                        }
                    }
                    else if (argument.value_str != nullptr) {
                        *(argument.value_str) = value;
                    }
                }
                argument.is_set = true;
                return true;
            }
        }
        return false;
    }

    bool ArgParser::ProcessShortArgument(const std::string& arg) {
        for (size_t j = 1; j < arg.length(); ++j) {
            char short_key = arg[j];
            bool is_last_character = (j == arg.length() - 1);

            Argument* argument = FindArgumentByShortKey(short_key);
            if (!argument) return false;

            if (argument->is_flag) {
                if (argument->value_bool) *(argument->value_bool) = true;
            }
            else {
                if (is_last_character) return false;
                std::string value = arg.substr(j + 2);
                if (argument->value_str) *(argument->value_str) = value;
                j = arg.length();
            }
            argument->is_set = true;
        }
        return true;
    }

    bool ArgParser::ProcessPositionalArgument(const std::string& arg, size_t& positional_arg_index) {
        if (positional_arg_index >= arguments_.size()) return false;
        Argument& positional_arg = arguments_[positional_arg_index];
        if (!positional_arg.is_positional) return false;

        char* end = nullptr;
        long val = strtol(arg.c_str(), &end, 10);
        if (end != arg.c_str() && *end == '\0' && val >= INT_MIN && val <= INT_MAX) {
            positional_arg.value_int->push_back(static_cast<int>(val));
            positional_arg.is_set = true;
        }
        else {
            return false;
        }
        return true;
    }

    bool ArgParser::Parse(const std::vector<std::string>& args) {
        size_t positional_arg_index = 0;
        for (size_t i = 1; i < args.size(); ++i) {
            std::string arg = args[i];

            if (arg.substr(0, 2) == "--") {
                if (!ProcessLongArgument(arg)) return false;
            }
            else if (arg[0] == '-') {
                if (!ProcessShortArgument(arg)) return false;
            }
            else {
                if (!ProcessPositionalArgument(arg, positional_arg_index)) return false;
            }
        }

        return CheckArgumentsAfterParsing();
    }

    bool ArgParser::CheckArgumentsAfterParsing() {
        for (const auto& argument : arguments_) {
            if (argument.is_positional && argument.min_values > 0 && argument.value_int
                && argument.value_int->size() < argument.min_values) {
                return false;
            }
        }

        for (const auto& argument : arguments_) {
            if (argument.min_values > 0 && argument.value_int && argument.value_int->size() < argument.min_values) {
                return false;
            }
        }

        for (auto& argument : arguments_) {
            if (!argument.is_set) {
                if (!argument.is_flag) {
                    if (argument.value_str) *argument.value_str = argument.default_value_str;
                }
                else {
                    if (argument.value_bool) *argument.value_bool = argument.default_value_bool;
                }
            }
        }

        for (auto& argument : arguments_) {
            if (argument.is_help && argument.is_set) {
                help_requested_ = true;
                return true;
            }
        }

        for (const auto& argument : arguments_) {
            if (!argument.is_flag && !argument.is_set && argument.default_value_str.empty()) {
                return false;
            }
        }

        return true;
    }
}