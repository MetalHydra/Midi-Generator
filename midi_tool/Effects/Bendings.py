import numpy as np
from .Funcs import Funcs

class Bendings:
    '''This class Simulates Bendings by modifying Pitch Wheel Values accordingly to predefined Functions like sine, cosine, exp or log'''
    def __init__(self) -> None:
        self.funcs = Funcs()

    def tremolo_slow(self):
        max_bound = 20
        x, y = self.funcs.combined(points_per_segment=[32], seg_funcs=["sin"], point_ranges=[(0,4*np.pi)], scales=[1.], scale_ranges=[(0,max_bound)], add_noise=True)        
        return x, y

    def tremolo_fast(self):
        max_bound = 20
        x, y = self.funcs.combined(points_per_segment=[64], seg_funcs=["saw"], point_ranges=[(0,8*np.pi)], scales=[1.], scale_ranges=[(0,max_bound)], add_noise=True)       
        return x, y
    
    def bend_up(self, steps:int=1):
        max_bound = int(8191*steps)
        min_bound = int(-8192*steps)
        x, y = self.funcs.combined(points_per_segment=[8], seg_funcs=["exp"], point_ranges=[(0,np.pi)], scales=[1.], scale_ranges=[(0,max_bound)], add_noise=True)
        return x, y      

    def bend_down(self, steps:int=1):
        max_bound = int(8191*steps)
        min_bound = int(-8192*steps)
        x, y = self.funcs.combined(points_per_segment=[8], seg_funcs=["exp"], point_ranges=[(0,np.pi)], scales=[-1.], scale_ranges=[(0,max_bound)], add_noise=True)
        return x, y

    def bend_up_down(self, steps:float=1.):
        max_bound = int(8191*steps)
        min_bound = int(-8192*steps)
        x, y = self.funcs.combined(points_per_segment=[8,8], seg_funcs=["exp", "exp"], point_ranges=[(0,np.pi),(np.pi,2*np.pi)],scales=[1,-1],scale_ranges=[(0,max_bound),(0,max_bound)], add_noise=True)
        nx = np.linspace(0,3, y.shape[0])
        return nx, y