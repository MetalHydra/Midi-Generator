import IO
import numpy as np
import ast

class Drum_Utils:
    def __init__(self) -> None:
        super().__init__()
        self.IO = IO.IO()
        self.drum_instruments = self.IO.read_json_file("./configs/drum_transitions.json")        
    
    def choose_random_drum_instrument(self) -> object or np.ndarray:
        return np.random.choice(list(self.drum_instruments.keys()), size=1)[0]         
        
    def get_possible_drum_insts(self) -> list[str]:
        return list(self.drum_instruments.keys())
    
    def choose_random_drum_on_initial(self,runs:int=1, initial:str='[38]', from_initial:bool=True) -> list:
        res = []
        initial = initial        
        if not from_initial:
            initial = self.choose_random_drum_instrument()               
        init_prob = self.drum_instruments[initial]
        for _ in range(runs):
            elem = np.random.choice(list(self.drum_instruments.keys()), p=init_prob)            
            initial = elem
            init_prob = self.drum_instruments[initial]
            res.append(ast.literal_eval(elem))        
        return res    
    
    