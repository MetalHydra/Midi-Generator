//
// Created by denni on 15.05.2023.
//
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
    static int CalculateNotePosition(const std::string &_note) {
        std::map<char, int> noteValues = {
                {'C', 0},
                {'D', 2},
                {'E', 4},
                {'F', 5},
                {'G', 7},
                {'A', 9},
                {'B', 11}
        };

        std::map<char, int> accidentalValues = {
                {'#', 1},
                {'b', -1},
                {'x', 2},
                {'d', -2}
        };

        int notePosition = noteValues[_note[0]];
        for (int i = 1; i < _note.length(); i++) {
            notePosition += accidentalValues[_note[i]];
        }
        return notePosition % 12;
    };

    Note(const std::string &note, int octave) {
        // check if note is in list
        if (std::find(notes.begin(), notes.end(), note) != notes.end()) {
            this->note = note;
            this->octave = octave;
        } else {
            throw std::invalid_argument("Note is not in list");
        }

        int notePosition = CalculateNotePosition(note);
        this->midi = notePosition + 12 *(octave + 1);
        this->frequency = 440.0 * pow(2, (notePosition - 9) / 12.0);
    };

    std::string GetNoteWithOctave() {
        return this->note + std::to_string(this->octave);
    };

};