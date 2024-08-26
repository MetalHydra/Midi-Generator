import pretty_midi as pm
import numpy as np

class Midi_Utils:
        
    def __init__(self) -> None:
        pass

    def quantize_midi(self, grid:float=1/32, fit_ends:bool=True,end_resolution:float=1/64, midi_file:str="default.mid") -> None:
        midi_dir = "../Midi_Files/"
        midi_file = midi_dir + midi_file
        pm = pm.PrettyMIDI(midi_file)
        print(pm.get_piano_roll().shape)
        name = midi_file.split('.')[0] + "_quantized" + ".mid"
        ending = pm.get_end_time()
        grid_time_locations = np.arange(0.0,ending, step=grid)
        grid_time_locations_e = np.arange(0.0,ending, step=end_resolution)
        for inst in pm.instruments:
           for note in inst.notes:
               ons = note.start    
               end = note.end                
               idx = (np.abs(grid_time_locations-ons)).argmin()
               idx_e = (np.abs(grid_time_locations_e-end)).argmin()
               note.start = grid_time_locations[idx]
               if fit_ends:
                   note.end = grid_time_locations_e[idx_e]
        pm.write(name)

        def merge_midi_files(self, target_filename:str, list_of_midi_files:list[str], fixed_tempo:int=60, randomize_oder:bool=False) -> None:
            end = 0
            midi_dir = "../Midi_Files/"
            if randomize_oder:
                list_of_midi_files = np.random.shuffle(list_of_midi_files).tolist()
            mf = pm.PrettyMIDI(initial_tempo=fixed_tempo)
            inst = pm.Instrument(program=0)
            for file in list_of_midi_files:
                if not file.endswith(".mid"):
                    file += ".mid"
                file = midi_dir + file
                print(file)
                midi_file = self.read_midi_file(filename=file)            
                cur_inst_notes = midi_file.instruments[0].notes
                cur_inst_bends = midi_file.instruments[0].pitch_bends
                cur_control_changes = midi_file.instruments[0].control_changes
                for nt in cur_inst_notes:
                    inst.notes.append(pm.Note(velocity=nt.velocity, pitch=nt.pitch, start=nt.start+end, end=nt.end+end))
                if cur_inst_bends != []:
                    for pbs in cur_inst_bends:
                        inst.pitch_bends.append(pm.PitchBend(pitch=pbs.pitch, time=pbs.time+end))
                if cur_control_changes != []:
                    for cc in cur_control_changes:
                        inst.control_changes.append(pm.ControlChange(number=1, value=cc.value, time=cc.time+end))            
                end = midi_file.get_end_time()
            mf.instruments.append(inst)
            mf.write(midi_dir+target_filename)