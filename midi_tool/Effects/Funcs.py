from audioop import add
import numpy as np
from scipy import signal, interpolate


class Funcs():
    def __init__(self) -> None:
        self.func_map = {
            "sin":np.sin,
            "cos":np.cos,
            "saw":signal.sawtooth,
            "squared":signal.square,
            "exp":np.exp,
            "exp2":np.exp2,
            "log":np.log
        }        

    def create_x_samples(self, start:float=0., end:float=2*np.pi, num:int=8, scale:str="linear",add_noise:bool=False, noise_range:tuple[float]=(-0.125,0.125)) -> np.ndarray:
        if scale == "log":
            x = np.logspace(start,end,num=num)
        else:
            x =  np.linspace(start,end,num=num)
        if add_noise:
                noise = np.random.uniform(noise_range[0],noise_range[1], size=num)
                print(noise.shape)
                x += noise
        return x

    def create_y_samples(self, x_samples:np.ndarray or list, scale:float=1., y_func:str="sin", add_noise:bool=False, noise_range:tuple[float]=(-0.125,0.125)) -> np.ndarray:
            y = scale*self.func_map[y_func](x_samples)
            if add_noise:
                noise = np.random.uniform(noise_range[0],noise_range[1], size=x_samples.shape[0])
                y += noise
            return y

    def combined(self, points_per_segment:list[int]=[5,8,5], seg_funcs:list[str]=["exp","sin","log"], scales:list[float]=[1.,1.,1.], 
                                        point_ranges:list=[(0,0.5*np.pi),(0.5*np.pi,2*np.pi),(2*np.pi,3*np.pi)], scale_ranges:list=[(-1,1),(-1,1),(-1,1)], 
                                                                                                                        add_noise:bool=True, noise_range:tuple[float]=(-0.125,0.125)) -> np.ndarray:
        assert len(points_per_segment) == len(seg_funcs) == len(point_ranges) == len(scales) == len(scale_ranges), 'points per segments, seg_funcs and point ranges should all have the same length'        
        combined_x = []
        combined_y = []
        for idx, num_samps in enumerate(points_per_segment):
            _range = point_ranges[idx]     
            _scale = scale_ranges[idx]      
            x = self.create_x_samples(start=_range[0], end=_range[1], num=num_samps, add_noise=add_noise, noise_range=noise_range)
            y = self.create_y_samples(x, y_func=seg_funcs[idx], scale=scales[idx], add_noise=add_noise, noise_range=noise_range)
            y_scaled = self.scale_data_to_equal_range(data=y, lower=_scale[0], upper=_scale[1])
            combined_x.append(x)
            combined_y.append(y_scaled)
        combined_x = np.hstack(combined_x)
        combined_y = np.hstack(combined_y)        
        return (combined_x, combined_y)

    def scale_data_to_equal_range(self, data:np.ndarray, lower:float=-1., upper:float=1.) -> np.ndarray:        
        scaled_data = (data - np.min(data)) / (np.max(data) - np.min(data)) * (upper - lower) + lower      
        return scaled_data

 