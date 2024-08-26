//
// Created by denni on 21.05.2023.
//

#ifndef SEMTANTIC_MUSIC_HANDLER_NOTE_H
#define SEMTANTIC_MUSIC_HANDLER_NOTE_H

#define BASE_FREQUENCY 440.0
#include "Interval.h"

struct Note_Result {
    std::string note_name_with_octave;
    std::string note_without_octave;
    std::string additional_accidental;
    int octave;
    int note_position;
    int midi;
    float frequency;
};

class Note {
private:
    const std::list<std::string> notes = {"C#", "Db", "D#", "Eb", "F#", "Gb", "G#", "Ab", "A#", "Bb" ,"C", "D", "E", "F", "G", "A", "B"};
    Note_Result result;
public:
    Note(const std::string &note, int octave);
    int CalculateNotePosition(const std::string &_note);
    void Update(const std::string &note_name, int note_octave);
    std::tuple<std::string, int> transposeNote(Interval& interval);
    Note_Result get_infos();
    void print();
    std::string generateEnharmonic(int target_value, const std::string& base_string);

};
#endif //SEMTANTIC_MUSIC_HANDLER_NOTE_H
