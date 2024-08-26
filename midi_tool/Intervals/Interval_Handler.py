from typing import Tuple
from IO.IO import IO
import music21
import numpy as np

class Interval_Handler:    
    def __init__(self) -> None:
        super().__init__()
        self.IO = IO()
        self.file = self.IO.read_json_file("./configs/intervals.json")

    def get_intervals_from_scale(self, scale:str="major"):        
        return self.file["scales"][scale]

    def get_notes_from_scale(self, root:str="C0", scale:str="major", replace_flat_sign:bool=True, ignore_octave:bool=True) -> list[str]:        
        components = []        
        scale = self.get_intervals_from_scale(scale)
        for _, inter in enumerate(scale):
            gi = music21.interval.Interval(inter)
            nt = gi.transposeNote(music21.note.Note(root))
            if not ignore_octave:
                if replace_flat_sign:
                    components.append(nt.nameWithOctave.replace('-','b'))
                else:
                    components.append(nt.nameWithOctave)
            else:
                if replace_flat_sign:
                    components.append(nt.name.replace('-','b'))
                else:
                    components.append(nt.name)
        return components

    def get_all_notes(self) -> list[str]:
        return ["A","Ab","A#","B","Bb","C","Cb","C#","D","Db","D#","E","Eb","F","F#","G","Gb","G#"]

    def get_modes(self) -> list[str]:        
        return list(self.file["scales"].keys())

    def get_random_scale(self) -> str:
        return np.random.choice(self.get_modes())  

    def get_chord_qualities(self, quantity:str="basic") -> list[str]:
        return list(self.file["chord_intervals"][quantity].keys())

    def get_chord_intervals_from_quality(self, key:str="maj", quantity:str="basic") -> list[int]:
        return list(self.file["chord_intervals"][quantity][key])

    def numeric_interval_to_name(self, intervals:int or list[int]) -> list[str]:
        result = []
        if isinstance(intervals, list):
            for idx, elem in enumerate(intervals):
                result.append(music21.interval.Interval(elem).name)
        else:
            result = [music21.interval.Interval(intervals).name]
        return result

    def named_interval_to_numeric(self, intervals:int or list[int]) -> list:
        result = []
        if isinstance(intervals, list):
            for idx, elem in enumerate(intervals):
                result.append(music21.interval.Interval(elem).semitone)
        else:
            result = [music21.interval.Interval(intervals).semitone]
        return result

    def get_chord_components_from_key(self, root:str="A4", chord:str="maj", replace_flat_sign:bool=False, ignore_octave:bool=False) -> list[str]:
        intervals = self.get_chord_intervals_from_quality(chord)
        components = []
        for _, inter in enumerate(intervals):
            gi = music21.interval.Interval(inter)
            nt = gi.transposeNote(music21.note.Note(root))
            if replace_flat_sign:
                if ignore_octave:
                    components.append(nt.name.replace('-','b'))
                else:
                    components.append(nt.nameWithOctave.replace('-','b'))
            else:
                if ignore_octave:
                    components.append(nt.name)
                else:
                    components.append(nt.nameWithOctave)
        return components    
    


