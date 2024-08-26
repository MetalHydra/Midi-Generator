//
// Created by denni on 21.05.2023.
#include "iostream"
#include "algorithm"
#include <list>
#include <map>
#include <tuple>
#include "cmath"
#include <any>
#pragma once

struct Interval_Result{
    int semitones;
    std::string accidental;
    std::string short_name;
    std::string name;
    int offset;
};

class Interval {
private:
    std::map<std::string, std::string> name_fullname_map = {
            {"P", "Perfect"}, {"m", "Minor"}, {"M", "Major"}, {"d", "Diminished"},
            {"A", "Augmented"}, {"dd", "doubly diminished"}, {"AA", "doubly augmented"},
    };

    std::list<std::string> prefixes = {"AA", "dd", "A", "d", "P", "m", "M" };
    std::map<std::string, std::tuple<std::string, int, std::string>> semitone_map = {
            {"P1", {"P1", 0, ""}},
            {"m2", {"m2", 1, "b"}},
            {"M2", {"M2", 2, "#"}},
            {"m3", {"m3", 3, "b"}},
            {"M3", {"M3", 4, "#"}},
            {"P4", {"P4", 5, ""}},
            {"P5", {"P5", 7, ""}},
            {"m6", {"m6", 8, "b"}},
            {"M6", {"M6", 9, "#"}},
            {"m7", {"m7", 10, "b"}},
            {"M7", {"M7", 11, "#"}},
            {"P8", {"P8", 12, ""}},
            {"A1", {"P1", 1, "#"}},
            {"AA1", {"P1", 2, "#"}},
            {"A2", {"M2", 3, "#"}},
            {"AA2", {"M2", 4, "#"}},
            {"A3", {"M3", 5, "#"}},
            {"AA3", {"M3", 6, "#"}},
            {"A4", {"P4", 6, "#"}},
            {"AA4", {"P4", 7, "#"}},
            {"A5", {"P5", 8, "#"}},
            {"AA5", {"P5", 9, "#"}},
            {"A6", {"M6", 10, "#"}},
            {"AA6", {"M6", 11, "#"}},
            {"A7", {"M7", 12, "#"}},
            {"AA7", {"M7", 13, "#"}},
            {"A8", {"P8", 13, "#"}},
            {"AA8", {"P8", 14, "#"}},
            {"d1", {"P1", -1, "b"}},
            {"dd1", {"P1", -2, "b"}},
            {"d2", {"m2", 0, "b"}},
            {"dd2", {"m2", -1, "b"}},
            {"d3", {"m3", 2, "b"}},
            {"dd3", {"m3", 1, "b"}},
            {"d4", {"P4", 4, "b"}},
            {"dd4", {"P4", 3, "b"}},
            {"d5", {"P5", 6, "b"}},
            {"dd5", {"P5", 5, "b"}},
            {"d6", {"m6", 7, "b"}},
            {"dd6", {"m6", 6, "b"}},
            {"d7", {"m7", 9, "b"}},
            {"dd7", {"m7", 8, "b"}},
            {"d8", {"P8", 11, "b"}},
            {"dd8", {"P8", 10, "b"}},
    };
    Interval_Result result;

public:
    Interval(const std::string &interval);
    void Update(const std::string &interval_name);
    Interval_Result get_infos();
    void print();
};


