from IO.IO import IO
import numpy as np
from Intervals.Interval_Handler import Interval_Handler
from itertools import cycle
import librosa

# TODO Refactoring this class
class Note_Utils:
    
    def __init__(self) -> None:
        super().__init__()
        self.IO = IO()
        self.IH = Interval_Handler()
        self.chord_look = None#self.IO.read_json_file("../configs/chord_lookup.json")    


    # Mapping flat notes to sharp and vice versa
    def flat_to_sharp(self, notes:list, type:str="stf"):        
        assert notes != [], "note array cant be empty"        
        sharps = {
            "A#":"Bb",
            "B#":"C",
            "C#":"Db",
            "D#":"Eb",
            "E#":"F",
            "F#":"Gb",
            "G#":"Ab"
        }
        flats = {
            "Bb":"A#",
            "Cb":"B",
            "Db":"C#",
            "Eb":"D#",
            "Fb":"E",
            "Gb":"F#",
            "Ab":"G#"
        }
        
        conv = []
        if type == "stf":
            for elem in notes:
                if elem in sharps.keys():
                    conv.append(sharps[elem])
                else:
                    conv.append(elem)
        elif type == "fts":
            for elem in notes:
                if elem in flats.keys():
                    conv.append(flats[elem])
                else:
                    conv.append(elem)        
        return conv    
    
    def midi_numbers_to_notes(self, numbers:list[int]=[21], with_ocatave:bool=True) -> list[str]:
        return librosa.midi_to_note(numbers, octave=with_ocatave, unicode=False)

    def notes_to_midi_numbers(self, notes:list[str]=["A4"]) -> np.ndarray:
        return librosa.note_to_midi(notes)

 
    def choose_single_note_from_position(self, position:list[int]=[1], scale:str="major", root:str="A4"):        
        results = []
        notes = self.IH.get_notes_from_scale(root=root, scale=scale)
        for pos in position:
            results.append(notes[pos-1])
        return results
    
    def get_chord_notes(self, chord:str="C2:5", arpeggio_direction:str="arp_down"):
        root,quality = chord.split(":")
        components = self.IH.get_chord_components_from_key(root=root, chord=quality, ignore_octave=False)
        return components
   
    def choose_random_root(self, default_octave:int=2, random_octave:bool=False, min_ocatave:int=1, max_octave:int=6):        
        notes = ["A","Ab","A#","B","Bb","C","Cb","C#","D","Db","D#","E","Eb","F","F#","G","Gb","G#"]
        random_note = np.random.choice(notes)
        default_octave = default_octave
        if random_octave:
            default_octave = np.random.randint(min_ocatave, max_octave, size=1)[0]
        return random_note + str(default_octave) 