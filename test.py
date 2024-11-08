import network

P = network.Network(16, 16, 0.3)
P.hoshen_kopelman()
P.plot_grid(labeled=True, file_name='test')
