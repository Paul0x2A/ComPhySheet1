import numpy

import network
import time

L = 2**15
P = network.Network(L, L, 0.6)
s = time.perf_counter()
P.hoshen_kopelman()
print(f'Size {L} took {time.perf_counter()-s} s') # Size 32768 took 7.354308100000708 s with ~ 20 GB RAM for a short time
#P.plot_grid(labeled=True, file_name='test')
