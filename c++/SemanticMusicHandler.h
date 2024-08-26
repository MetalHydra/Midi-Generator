//
// Created by denni on 15.05.2023.
//

#ifndef SEMTANTIC_MUSIC_HANDLER_SEMANTICMUSICHANDLER_H
#define SEMTANTIC_MUSIC_HANDLER_SEMANTICMUSICHANDLER_H
#include "iostream"
#include "algorithm"
#include <list>
#include <map>
#include "cmath"


class Note {
private:
    std::list<std::string> notes = {"C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A","A#", "B"};
    std::string note;
    int octave;
    int midi;
    float frequency;
public:


};


#endif //SEMTANTIC_MUSIC_HANDLER_SEMANTICMUSICHANDLER_H
