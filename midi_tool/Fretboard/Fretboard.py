from unittest import result
import numpy as np
from Notes.Note_Utils import Note_Utils

class Fretboard:
    def __init__(self,name:str="guitar", strings:int=7, frets:int=24, tuning:list[str]=["B1","E2","A2","D3","G3","B3","E4"]) -> None:
        assert strings == len(tuning), "number of strings must match with tuning list"
        self.name = name
        self.strings = strings
        self.frets = frets+1
        self.tuning = tuning
        self.NU = Note_Utils()
        self.tuning_in_midi = None
        self.fretboard = np.zeros(shape=(self.strings, self.frets))
        self._build_fretboard()        

    def get_number_of_strings(self) -> int:
        return self.strings

    def get_tuning(self) -> list[int]:
        return self.tuning_in_midi[::-1]

    def _build_fretboard(self) -> None:
        self.tuning_in_midi = self.NU.notes_to_midi_numbers(self.tuning)
        self.fretboard[:,0] = self.tuning_in_midi
        for row_idx, row in enumerate(self.fretboard):
            start_val = row[0]
            midi_vals = np.arange(start=start_val, stop=start_val+self.frets)
            self.fretboard[row_idx] = midi_vals
        self.fretboard = self.fretboard.flatten()        

    def get_musicxml_string_fret(self, string:int=1, fret:int=1)-> str:
        ret_str = f"""<string>{string}</string>
                        <fret>{fret}</fret>"""
        return ret_str

    def get_fret_string(self, note:str="A4") -> str:
        pos = self.find_note_positions(note)
        res_string = self.get_musicxml_string_fret(pos[0]+1, pos[1])
        return res_string
        
    def find_positions(self, notes:list[str]) -> list[np.ndarray]:
        results = []
        for idx, note in enumerate(notes): 
            note = self.NU.notes_to_midi_numbers(note)        
            res = np.argwhere(self.fretboard==note)
            x,y = np.unravel_index(res, shape=(self.strings,self.frets))
            z = np.column_stack((x,y))
            results.append(z)
        return results
        
    # just give in multiple octaves
    def find_note_positions(self, note:str, position="first"):
        note = self.NU.notes_to_midi_numbers(note)        
        res = np.argwhere(self.fretboard==note)
        x,y = np.unravel_index(res, shape=(self.strings,self.frets))
        z = np.column_stack((x,y))
        if position == "first":
            z = z[0]
        print("positions on fretboard are: ", z)
        return z

    def get_segment(self, start_fret:int=0, covered_frets:int=5):
        tmp = np.reshape(self.fretboard, newshape=(self.strings, self.frets))
        v = np.lib.stride_tricks.sliding_window_view(tmp, window_shape=(self.strings,covered_frets))
        return v[0][start_fret]

    def display(self):
        raise NotImplementedError("this function is not implemented yet")

    def change_tuning(self, tuning:list[str]):
        raise NotImplementedError("This function is not implemented yet")

    def get_tuning_as_musicxml(self) -> str:
        xml_string = f"""
        <root>             
            <clef>
                <sign>TAB</sign>
                <line>5</line>
            </clef>
        <staff-details>
        <staff-lines>{self.strings}</staff-lines>"""
        for idx, tun in enumerate(self.tuning):
            oct = tun[-1]
            root = tun[:-1]
            tuning_string = f"""<staff-tuning line=\"{idx+1}\"><tuning-step>{root}</tuning-step><tuning-octave>{oct}</tuning-octave></staff-tuning>"""     
            xml_string += tuning_string   
        xml_string += "</staff-details></root>" 
        return xml_string