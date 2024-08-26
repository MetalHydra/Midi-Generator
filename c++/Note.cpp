//
// Created by denni on 21.05.2023.
//
#include "Note.h"

Note::Note(const std::string &note, int octave) {
    Update(note, octave);
};

int Note::CalculateNotePosition(const std::string &_note) {
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

void Note::Update(const std::string &note_name, int note_octave) {
    std::string note = "";
    std::string additional_accidental = "";
    int octave = 0;
    int midi = 0;
    int note_position = 0;
    float frequency = 0.0;

    for (auto &nt : this->notes) {
        if(note_name.find(nt) == 0) {
            // split string into nt  and additional accidental
            note = nt;
            additional_accidental = note_name.substr(nt.length());
            break;
        }
    }
    note_position = CalculateNotePosition(note_name);

    midi = note_position + 12 * (note_octave + 1);
    frequency = BASE_FREQUENCY * pow(2, ((midi-69) / 12.0));

    this->result.note_without_octave = note;
    this->result.octave = note_octave;
    this->result.note_name_with_octave = note + std::to_string(note_octave);
    this->result.midi = midi;
    this->result.frequency = frequency;
    this->result.note_position = note_position;
    this->result.additional_accidental = additional_accidental;
};

Note_Result Note::get_infos() {
    return this->result;
}

void Note::print() {
    std::cout << "note name: " << this->result.note_without_octave << " \n octave: " << this->result.octave << " \n midi: " << this->result.midi << " \n frequency: " << this->result.frequency << std::endl;
};

std::tuple<std::string, int> Note::transposeNote(Interval& interval) {
    auto note_infos = this->result;
    auto interval_infos = interval.get_infos();

    std::vector<std::string> base_notes = {"C", "D", "E", "F", "G", "A", "B"};
    std::map<char, int> note_dict = {
            {'C', 0}, {'D', 1}, {'E', 2},
            {'F', 3}, {'G', 4}, {'A', 5}, {'B', 6}
    };

    auto base_char = static_cast<char>(note_infos.note_without_octave[0]);
    int base = note_dict[base_char] + interval_infos.offset;
    int rounds = 0;
    if (base > 6) {
        while (base > 6) {
            base -= 7;
            rounds += 1;
        }
    } else if (base < 0) {
        while (base < 0) {
            base += 7;
            rounds -= 1;
        }
    }
    std::string base_note = base_notes[base % 7];
    int target_val = (note_infos.note_position + interval_infos.semitones) % 12;
    std::string acc_info = "";

    if (interval_infos.accidental.length() > 0) {
        acc_info = interval_infos.accidental.substr(0, 1);
    }

    std::string harmonics = generateEnharmonic(target_val, base_note);
    std::string res_note = harmonics;
    int new_octave = note_infos.octave + rounds;
    return std::tuple{res_note, new_octave};
}

std::string Note::generateEnharmonic(int target_value, const std::string &base_string) {
    std::string sharp_res = base_string;
    std::string flat_res = base_string;
    int base_value = CalculateNotePosition(base_string);
    if (target_value > base_value) {
        for (int i = 0; i < (target_value - base_value); i++) {
            sharp_res += "#";
        }
    } else if (target_value < base_value) {
        for (int i = 0; i < (12 - (base_value - target_value)); i++) {
            sharp_res += "#";
        }
    } else {
        sharp_res += "";
    }

    if (target_value > base_value) {
        for (int i = 0; i < (12 - (target_value - base_value)); i++) {
            flat_res += "b";
        }
    } else if (target_value < base_value) {
        for (int i = 0; i < (base_value - target_value); i++) {
            flat_res += "b";
        }
    } else {
        flat_res += "";
    }

    std::string res;
    if (sharp_res.length() > flat_res.length()) {
        res = flat_res;
    } else {
        res = sharp_res;
    }
    return res;
}
