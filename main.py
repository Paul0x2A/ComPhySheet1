import network


P = network.Network(6, 6, 0.6)
P.hoshen_kopelman()
P.draw_raw_network('test')
P.draw_labeled_network('labels')
