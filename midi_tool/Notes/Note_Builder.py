import enum
import music21
from sklearn.utils import deprecated
from Intervals.Interval_Handler import Interval_Handler
from . import Note_Object
from Rythms.Rythm_Object import Rythm_Object
from Rythms.Rythm_Builder import Rythm_Builder
from .Note_Utils import Note_Utils
import numpy as np
import pretty_midi as pm
import uuid
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as BS
from Fretboard.Fretboard import Fretboard
from copy import copy
from Effects.Muscixml_Effects import MXML_Effects

class Note_Builder:
    
    def __init__(self) -> None:
        self.IH = Interval_Handler()        
        self.RB = Rythm_Builder()    
        self.NU = Note_Utils()
        self.FB = Fretboard()
        self.ME = MXML_Effects()
        
    # creates a single Note, when quality is unspecified
    # creates a Rest, if Root Note is specified as R
    # from components can be specified as A4!C3!E-5 in root note
    def create_element(self, root_note:str or int="A4", quality:str="", components:list[str or int]=[38],effect="no",
                                                            rythm_type:Rythm_Object=Rythm_Object(value="quarter",short="q",duration=music21.duration.Duration(1/4))) -> Note_Object:
        element = None        
        other_comp = []       
        _from_custom_midi_numbers: bool = False
        _is_mixed: bool = False
        if "!" in root_note:
            components = root_note.split("!")     
            _from_custom_midi_numbers = all(i.isdigit() for i in components)    
            _is_mixed = any(i.isdecimal() for i in components)
            print(_is_mixed)
            if _from_custom_midi_numbers and not _is_mixed:     
                other_comp = self.NU.midi_numbers_to_notes(numbers=components)
                # switching components with other_components if necessery
                tmp = other_comp
                other_comp = components
                components = tmp
            elif _is_mixed:
                raise ValueError("mixing midi numbers with notes is not supported")
            else:
                other_comp = self.NU.notes_to_midi_numbers(components) 
                element = Note_Object.Note_Object(name="",root="",quality="custom",rythm_Object=rythm_type, effect=effect,components=components,midi_components=other_comp)
                        
        elif root_note == "R":
            element = Note_Object.Note_Object(name="Rest", root="R", quality="", rythm_Object=rythm_type, effect="no", components=["R"], midi_components=["R"])
        elif root_note != "R" and quality == "":
            element = Note_Object.Note_Object(name=root_note, root=root_note, quality="", rythm_Object=rythm_type, effect=effect, components=[root_note], midi_components=self.NU.notes_to_midi_numbers([root_note]))
        elif root_note != "R" and quality != "" and quality != "custom":                
            chord_components = self.IH.get_chord_components_from_key(root=root_note, chord=quality, replace_flat_sign=True)
            element = Note_Object.Note_Object(name=root_note[0]+quality,root=root_note,quality=quality, rythm_Object=rythm_type, effect=effect, components=chord_components, midi_components=self.NU.notes_to_midi_numbers(chord_components))
        return element      
    
    def create_melody(self, note_elements:list[Note_Object.Note_Object], mode:str='random'):
        new_note_string = ""
        new_rythm_string = ""
        for idx, note_element in enumerate(note_elements):
            cur_rythm_string = note_element.rythm_Object.short
            alternative_rythm, length = self.RB.create_alternative_rythm_string(cur_rythm_string)
            length = length[0]
            if note_element.is_rest():
                new_rythm_string += cur_rythm_string+'_'
                new_note_string += "R:_"
            elif note_element.is_note():
                new_rythm_string += cur_rythm_string+'_'
                new_note_string += note_element.root+':'+'_'
            elif note_element.is_chord() or note_element.is_custom():
                components = note_element.components
                n_comps = components
                if len(components) < length:
                    n_comps = np.resize(components, length)
                if mode == 'reverse':
                    n_comps = n_comps[::-1]
                elif mode == 'random':
                    np.random.shuffle(n_comps)
                for c_idx, c_comp in enumerate(n_comps):
                    new_note_string += c_comp+':'+'_'
                new_rythm_string += alternative_rythm+'_'
        return (new_note_string, new_rythm_string)
    
    def create_music21_stream(self, note_elements:list[Note_Object.Note_Object]) -> music21.stream.Stream:
        stream = music21.stream.Stream()
        ts = "4/4"
        effect_list = [] #this list is needed for injecting the right musicxml effects
        for n_idx, nelem in enumerate(note_elements):
            if ts != nelem.rythm_Object.reference_time_signature:
                ts = nelem.rythm_Object.reference_time_signature
                stream.append(nelem.rythm_Object._music21_time_signature)
                stream.append(nelem.rythm_Object._tempo)
            stream.append(nelem._music21_component)
        return stream

    def stream_to_midi(self, stream:music21.stream.Stream, filename:str="default.midi"):
        mf = music21.midi.translate.streamToMidiFile(stream)
        mf.open("./Midi/"+filename, 'wb')
        mf.write()
        mf.close()

    def stream_to_musicxml(self,  note_elements:list[Note_Object.Note_Object], filename:str="default") -> None:
        stream = music21.stream.Stream()
        ts = "4/4"
        effect_list = [] #this list is needed for injecting the right musicxml effects
        note_lists = []
        print(note_elements[1].effect)
        for n_idx, nelem in enumerate(note_elements):
            if ts != nelem.rythm_Object.reference_time_signature:
                ts = nelem.rythm_Object.reference_time_signature
                stream.append(nelem.rythm_Object._music21_time_signature)
                stream.append(nelem.rythm_Object._tempo)
            effect_list.append(nelem.effect)
            note_lists.append(nelem.components)
            stream.append(nelem._music21_component)
        note_lists = [element for sublist in note_lists for element in sublist]
        GEX = music21.musicxml.m21ToXml.GeneralObjectExporter()
        mxml = GEX.fromGeneralObject(stream)
        SX = music21.musicxml.m21ToXml.ScoreExporter(mxml)
        mxmlData = SX.parse()       
        tree = ET.ElementTree(mxmlData)
        tree_string = ET.tostring(tree.getroot(), encoding='utf-8')
        tree_string = tree_string.decode('utf-8')
        soup = BS(tree_string, 'xml')
        #print("soup,", soup)
        results = soup.find_all('note')
        #print("note results: ", results)
        tuning_string = self.FB.get_tuning_as_musicxml() 
        soup_tuning = BS(tuning_string, 'xml')
        soup.attributes.append(copy(soup_tuning))
        for i, note_elem in enumerate(results):
            fr_str = self.FB.get_fret_string(note=note_lists[i])
            technical_string = f"""<notations><technical>{fr_str}</technical></notations>"""
            technical_soup = BS(technical_string, 'xml')
            note_elem.append(technical_soup)           
            if not effect_list[i] == 'no':
                eff = effect_list[i]
                eff_tup = self.ME.get_musicxml_string(eff)
                print("eff tup", eff_tup[0])
                effts = eff_tup[0]
                for ef in effts:
                    soup_effect = BS(ef, 'xml')
                    if eff_tup[1] == False:
                        note_elem.append(soup_effect)
                    else:
                        note_elem.technical.append(soup_effect)
        with open("./MusicXML/"+filename, 'w') as f:
            f.write(str(soup))  
        print("finished writing musicxml file")      
        # Tab staff and staff-tuning have to be set in the attributes Tag of a part
        
        #for r in results:
        #    r.append(xml_tuning)
        #tree.write("./MusicXML/"+filename, encoding="utf-8", xml_declaration=True)

    def create_midi_from_notes(self, elements:list[Note_Object.Note_Object], name:str=str(uuid.uuid4())) -> None:
        tempo = elements[0].rythm_Object.reference_bpm
        pmf = pm.PrettyMIDI(initial_tempo=tempo)
        time_sigs = []
        cur_time_sig = ""
        inst = pm.Instrument(program=0)
        for idx, elem in enumerate(elements):
            ts = elem.rythm_Object.reference_time_signature
            if cur_time_sig != ts:
                cur_time_sig = ts
                num, denum = cur_time_sig.split("/")
                num = int(num)
                denum = int(denum)
                print("time sig change", cur_time_sig, elem.rythm_Object.offset_in_seconds)
                time_sigs.append(pm.TimeSignature(numerator=num, denominator=denum,time=elem.rythm_Object.offset_in_seconds))
            onsets = elem.component_onsets
            endings = elem.component_endings
            velocities = elem.component_velocities
            pitches = elem.midi_components
            for n_idx, pitch in enumerate(pitches):  
                note = pm.Note(velocity=velocities[n_idx], pitch=pitch, start=onsets[n_idx], end=endings[n_idx])
                inst.notes.append(note)
        pmf.time_signature_changes = time_sigs
        pmf.instruments.append(inst)
        pmf.write("./Midi/"+name+".midi")

    def parse_effect_string(self, effects:str) -> list[str]:
        # pm = palm mute
        # fbu = full up bending + hold (2 semitones)
        # hbu = half up bending + hold (1 semitone)
        # fbud = full up bending + release
        # fbud = half up bending + release
        # tr = tremolo
        part = effects.split("_")
        return part

    def create_list_of_notes(self, note_string:str="C4:_C4:_C4:_C4:", rythm_string:str="4/4:60_q_q_q_q", effect_string="no_no_no_no") -> list[Note_Object.Note_Object]:
        result = []
        elements = note_string.split("_")
        rythm_list,tempo = self.RB.parse_rythm_string(rythm_string=rythm_string)
        effect = self.parse_effect_string(effect_string)
        for elem, ryth, eff in zip(elements, rythm_list, effect):
            if not ":" in elem:
                elem = elem+":"
            if ":" in elem:                   
                root, quality = elem.split(':')
                result.append(self.create_element(root_note=root,quality=quality, rythm_type=ryth, effect=eff))   
            elif "!" in elem: 
                result.append(self.create_element(root_note=elem,quality="custom", rythm_type=ryth, effect=eff))            
        return result

    def create_files_from_list(self, note_string:list[str]=["C4:"], rythm_string:list[str]=["4/4:60_q"], effect_strings:list[str] = ["no"], filename:list[str] or None=None, to_midi:bool=True, to_mxml:bool=True):
        if filename is None:
            filename = [str(uuid.uuid4())*len(note_string)]        
        assert type(note_string) == type(rythm_string), 'note strings and rythm string must have the same type. either list of strings or strings'        
        for nstr, rstr, eff, name in zip(note_string, rythm_string, effect_strings, filename):
            elements = self.create_list_of_notes(note_string=nstr, rythm_string=rstr, effect_string=eff)
            if to_midi:
                self.create_midi_from_notes(elements=elements, name=name)
            if to_mxml:
                stream = self.create_music21_stream(elements)
                self.stream_to_midi(stream, name+".midi")
                self.stream_to_musicxml(elements, name+".musicxml")