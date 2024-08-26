from dataclasses import dataclass
from typing import Tuple
import music21

WHOLE = 4
SHORTS = {
    "whole":"w",
    "half":"h",
    "quarter":"q",
    "eighth":"e",
    "16th":"s",
    "32nd":"t",
    "64":"sf"
}

@dataclass
class Rythm_Object:
    value : str
    short : str
    duration : music21.duration.Duration(type="quarter", dots=0)    
    dots : int = 0
    offset: float = 0.
    ending:float = 0.
    reference_bpm: int = 60
    offset_in_seconds: float = 0.
    duration_in_seconds: float = 0.
    ending_in_seconds: float = 0.
    reference_time_signature: str = "4/4"
    _music21_time_signature: music21.meter.TimeSignature = None
    is_part_of_tuplet: bool = False
    _tempo = None

    def __post_init__(self) -> None:
        self.ending = self.offset + self.duration.quarterLength  
        self._tempo = music21.tempo.MetronomeMark(number=self.reference_bpm)    
        self._music21_time_signature = music21.meter.TimeSignature(self.reference_time_signature)  
        self.offset_in_seconds = self.offset_to_seconds()
        self.duration_in_seconds = self.duration_to_seconds()
        self.ending_in_seconds = self.offset_in_seconds + self.duration_in_seconds

    def __repr__(self) -> str:
         return f"value:{self.value}, dots:{self.dots}, ts:{self.reference_time_signature}, duration:{self.duration_in_seconds}, offset:{self.offset_in_seconds}, ending:{self.ending_in_seconds}"

    def offset_to_seconds(self) -> float:
        return self._tempo.durationToSeconds(self.offset)

    def duration_to_seconds(self) -> float:
        return self._tempo.durationToSeconds(self.duration)

    #def duration_to_seconds(self, bpm:int=60) -> Tuple[float,float]:
    #    measure = self.reference_time_signature
    #    num, denum = measure.split('/')
    #    num = int(num)
    #    denum = int(denum)
    #    meas = 60/bpm
    #    full_measure_length = meas*4
    #    return full_measure_length, meas*self.duration.quarterLength

    def is_part_of_tuplet(self) -> bool:
        return self.is_part_of_tuplet()
    
