import network


P = network.Network(16, 16, 0.7)
P.hoshen_kopelman()
P.draw_raw_network('test')
P.draw_labeled_network('labels')
