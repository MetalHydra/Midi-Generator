import numpy as np
import json
import pretty_midi as pm
import os

class IO:    
    def __init__(self) -> None:
        super().__init__()

    def get_all_files_from_path(self, path:str, ending:list[str]):  
        all_files = []
        for root, dirs, files in os.walk(path):
            for f in files:
                if f.endswith(ending[0]) or f.endswith(ending[1]):
                    all_files.append(root+"/"+f)
        return all_files

    def read_json_file(self, filename:str):        
        try:
            with open(filename,'r', encoding='utf-8') as config_file:
                settings = json.load(config_file)
                return settings
        except FileNotFoundError as fnfe:
            raise fnfe(f"cannot load {filename} file")

    def write_json_file(self, filename:str, data:object):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f)
        except FileNotFoundError as fnfe:
            raise fnfe(f"cannot load {filename} file")   

    def check_for_file(self, filename:str=""):
        return os.path.exists(filename)

    def read_midi_file(self, filename:str):        
        try:
            return pm.PrettyMIDI(filename)
        except FileNotFoundError as fnfe:
            raise fnfe(f"could not find file {filename}")
    
    
        
            