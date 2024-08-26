from typing import Tuple
import music21
from IO.IO import IO
from . import Rythm_Object
import random
from fractions import Fraction

MAX_DOTS = 2
WHOLE = 4

NAME_FRACTION_DICT = {
    "w":Fraction("1/1"),
    "w.":Fraction("1/1")+Fraction("1/2"),
    "w..":Fraction("1/1")+Fraction("1/2")+Fraction("1/4"),
    "h":Fraction("1/2"),
    "h.":Fraction("1/2")+Fraction("1/4"),
    "h..":Fraction("1/2")+Fraction("1/4")+Fraction("1/8"),
    "q":Fraction("1/4"),
    "q.":Fraction("1/4")+Fraction("1/8"),
    "q..":Fraction("1/4")+Fraction("1/8")+Fraction("1/16"),
    "e":Fraction("1/8"),
    "e.":Fraction("1/8")+Fraction("1/16"),
    "e..":Fraction("1/8")+Fraction("1/16")+Fraction("1/32"),
    "s":Fraction("1/16"),
    "s.":Fraction("1/16")+Fraction("1/32"),
    "s..":Fraction("1/16")+Fraction("1/32")+Fraction("1/64"),
    "t":Fraction("1/32"),
    "t.":Fraction("1/32")+Fraction("1/64"),
    "sf":Fraction("1/64"),
    "ht":Fraction("1/3"),
    "qt":Fraction("1/6"),
    "et":Fraction("1/12"),
    "st":Fraction("1/24"),
    "tt":Fraction("1/48")
}

FRACTION_POOL = {
"w":    [Fraction("1/1"), Fraction("1/2"), Fraction("1/4"), Fraction("1/8"),Fraction("1/16"),Fraction("1/3"),Fraction("1/6")],
"w.":   [Fraction("1/1"), Fraction("1/2"), Fraction("1/4"), Fraction("1/8"),Fraction("1/16"),Fraction("1/3"),Fraction("1/6")],
"w..":  [Fraction("1/1"), Fraction("1/2"), Fraction("1/4"), Fraction("1/8"),Fraction("1/16")],
"h":    [Fraction("1/2"), Fraction("1/4"), Fraction("1/8"), Fraction("1/16"), Fraction("1/6"), Fraction("1/12")],
"h.":   [Fraction("1/2"), Fraction("1/4"), Fraction("1/8"), Fraction("1/16"), Fraction("1/6"), Fraction("1/12")],
"h..":  [Fraction("1/2"), Fraction("1/4"), Fraction("1/8"), Fraction("1/16")],
"q":    [Fraction("1/4"), Fraction("1/8"), Fraction("1/16"), Fraction("1/12")],
"q.":   [Fraction("1/4"), Fraction("1/8"), Fraction("1/16"), Fraction("1/12")],
"q..":  [Fraction("1/4"), Fraction("1/8"), Fraction("1/16")],
"e":    [Fraction("1/8"), Fraction("1/16"), Fraction("1/24")],
"e.":   [Fraction("1/8"),Fraction("1/16"), Fraction("1/24"), Fraction("1/48")],
"e..":  [Fraction("1/8"), Fraction("1/16"), Fraction("1/32")],
"s":    [Fraction("1/16"), Fraction("1/32"), Fraction("1/48")],
"s.":   [Fraction("1/16"), Fraction("1/32")],
"s..":  [Fraction("1/16"), Fraction("1/32"), Fraction("1/64")],
"t":    [Fraction("1/32")],
"t.":   [Fraction("1/32"), Fraction("1/64")],
"sf":   [Fraction("1/64")] }

FRACTION_NAME_DICT = {v: k for k, v in NAME_FRACTION_DICT.items()}

class Rythm_Builder:
    def __init__(self) -> None:
        super().__init__()        
        self.IO = IO()  

    def parse_rythm_string(self, rythm_string:str="4/4:60_q_q_q_q") -> list[Rythm_Object.Rythm_Object]:
        time_signature = "4/4"
        result_rythm_list = []
        offset = 0.
        rythms = rythm_string.split('_') 
        first_elem = rythms[0]
        tempo = 60        
        for _, ryth in enumerate(rythms):
            if any(char.isdigit() for char in ryth):
                #Time Signature is detected
                if ":" in ryth:
                    time_signature, tempo = ryth.split(":")
                    tempo = int(tempo)
                else:
                    if "/" in ryth:
                        time_signature = ryth
                        tempo = 60
                    else:
                        tempo = int(ryth)
                continue
            rythm_object, off = self.create_rythm_object(value=ryth, time_signature=time_signature, offset=offset, tempo=tempo)
            result_rythm_list.append(rythm_object)
            offset += off
        return result_rythm_list,tempo

    def create_rythm_object(self, value:str="q", time_signature:str="4/4", offset:float=0., tempo:int=60) -> Tuple[Rythm_Object.Rythm_Object, float]:
        is_triplet = False
        try:
            val = NAME_FRACTION_DICT[value]
            if value[-1] == "t":
                is_triplet = True                
        except KeyError:
            print(f"key {value} is not a valid dictionary key!")
        dots = value.count('.')
        if dots > MAX_DOTS:
            dots = MAX_DOTS
        duration_object = music21.duration.Duration(val*WHOLE, dots=dots)
        ryth_obj = Rythm_Object.Rythm_Object(value=duration_object.fullName, short=value, duration=duration_object, reference_time_signature=time_signature ,dots=dots, offset=offset, reference_bpm=tempo, is_part_of_tuplet=is_triplet)
        offset = ryth_obj.duration.quarterLength
        return ryth_obj, offset

    def _cumulative_sum(self, candidates, target):
            candidates.sort()
            res=set()
            intermedia=[]
            self._recursion(candidates,target,res,intermedia)
            return [list(i) for i in res] 

    def _recursion(self,candidates,target,res,intermedia):
        for i in candidates:
            if target==i:
                temp=intermedia+[i]
                temp.sort()
                if temp is not None:
                    res.add(tuple(temp))
                return
            elif target>i:
                self._recursion(candidates,target-i,res,intermedia+[i])
            else:
                return        
    
    # it seems that sum Numerices will change the order of the numerics array (dont know why), need an other solution here
    def create_alternative_rythm_string(self, rythm_string:str="e"):     
        results = []
        counts =  []
        parts  = rythm_string.split('_')        
        for pidx, p in enumerate(parts):   
            if any(char.isdigit() for char in p):
                continue
            named_results = []
            duration_to_fit = NAME_FRACTION_DICT[p]
            numerics = FRACTION_POOL[p]                             
            possible_replacements = self._cumulative_sum(numerics,target=duration_to_fit)                     
            replacement = random.choice(possible_replacements)
            for r in replacement:
                named_results.append(FRACTION_NAME_DICT[r])        
            #fix, I dont know why this shit happens        
            numerics = numerics[::-1]       
            counts.append(len(named_results))     
            full_string = "_".join(named_results) 
            results.append(full_string)        
        return ('_'.join(results),counts)        
    
   


    
    