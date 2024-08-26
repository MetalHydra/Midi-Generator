//
// Created by denni on 21.05.2023.
//
#include "Interval.h"

Interval::Interval(const std::string &name) {
        this->Update(name);
    };

void Interval::Update(const std::string &interval_name) {
    std::string name = "";
    std::string fullname = "";
    int semitones = 0;
    int offset = 0;
    int direction = 1;

    name = interval_name;
    std::string current_prefix;
    std::string tmp_interval_name = interval_name;
    if (interval_name[0] == '-') {
        direction = -1;
        fullname += "descending ";
        tmp_interval_name = interval_name.substr(1);
    };

    for (auto &prefix: this->prefixes) {
        if (tmp_interval_name.substr(0, prefix.length()) == prefix) {
            current_prefix = prefix;
            break;
        }
    }


    fullname += this->name_fullname_map[current_prefix];

    std::string str_number = tmp_interval_name.substr(current_prefix.length());
    int number = std::stoi(str_number);
    int octave = static_cast<int>((number-1) / 7.0);
    int steps = (number -1) - (octave * 7);

    fullname += str_number;
    semitones += octave * 12;

    offset = steps;
    std::string n_steps = std::to_string(steps + 1);
    std::string new_interval = current_prefix + n_steps;
    auto [base_interval, additional_semitones, accidental] = this->semitone_map[new_interval];
    semitones += additional_semitones;
    semitones *= direction;
    offset *= direction;

    if (direction < 0) {
        if (accidental == "#") {
            accidental = "b";
        }
        else if (accidental == "b") {
            accidental = "#";
        }
        else {
            accidental = "";
        }
    }

    this->result.name = fullname;
    this->result.short_name = name;
    this->result.accidental = accidental;
    this->result.semitones = semitones;
    this->result.offset = offset;
};

void Interval::print(){
    std::cout << "name: " << this->result.name << " \n short name: " << this->result.short_name << " \n semitones: " << this->result.semitones << " \n offset: " << this->result.offset << " \n accidental: " << this->result.accidental << std::endl;
};

Interval_Result Interval::get_infos(){
    return this->result;
};

