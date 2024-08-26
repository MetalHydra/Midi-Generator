from dataclasses import dataclass, field
from Rythms.Rythm_Object import Rythm_Object
import music21
import numpy as np

@dataclass
class Note_Object:
    name:str = ""
    root:str = ""
    quality:str = ""
    rythm_Object:Rythm_Object = Rythm_Object(value="quarter",short="q",dots=0, duration=music21.duration.Duration(type="quarter", dots=0))
    components:list[str] = field(default_factory=list) 
    midi_components:list[str] = field(default_factory=list) 
    component_onsets:list[float] = field(default_factory=list)
    component_durations:list[float] = field(default_factory=list)
    component_velocities:list[int] = field(default_factory=list)
    component_endings:list[int] = field(default_factory=list)
    _music21_component:music21.note.Note or music21.note.Rest or music21.chord.Chord = None
    effect: str = ""
    bending:list[float] = None

    def __repr__(self) -> str:
        return f"name:{self.name}, quality:{self.quality}, components:{self.components}, midi_components:{self.midi_components}, onsets:{self.component_onsets}, durations:{self.component_durations}"

    def __post_init__(self) -> None:
        num_of_components = len(self.components)
        self.component_onsets = [self.rythm_Object.offset_in_seconds] * num_of_components
        self.component_durations = [self.rythm_Object.duration_in_seconds] * num_of_components
        self.component_velocities = [127] * num_of_components
        self.component_endings = [self.rythm_Object.ending_in_seconds] * num_of_components
        if self.is_rest():
            self._music21_component = music21.note.Rest()
        if self.is_note():
            self._music21_component = music21.note.Note(self.root)
        if self.is_chord() or self.is_custom():
            print("midi components",self.components)
            self._music21_component = music21.chord.Chord(self.components)
        self._music21_component.duration = self.rythm_Object.duration

    def get_annotations(self) -> dict:
        annotation_dict = {
            "name":self.name,
            "root":self.root,
            "quality":self.quality,
            "components":self.components,
            "midi_components":self.midi_components,
            "onsets":self.component_onsets,
            "durations":self.component_durations,
            "velocities":self.component_velocities,
            "endings":self.component_endings,
            "bending":self.bending          }
        return annotation_dict

    def get_musicxml(self) -> str:
        "returns a musicxml representation as string"
        musicxml = f""""""
        return musicxml
    
    def is_rest(self) -> bool:
        return self.root == "R"
    
    def is_note(self) -> bool:
        return self.root != "R" and self.quality == "" 

    def is_chord(self) -> bool:
        return self.root != "R" and self.quality != "" 
    
    def is_custom(self) -> bool:
        return self.quality == "custom"
    
    def add_bending(self, bending:list[float]) -> None:
        self.bending = bending

    def is_bended(self) -> bool:
        return self.bending is None

    def augment_velocity(self, lower:int=90, upper:int=127) -> None:
        new_velos = np.random.randint(lower, upper, size=len(self.component_velocities))
        self.component_velocities = new_velos