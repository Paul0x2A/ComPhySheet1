import random
import matplotlib.pyplot as plt
import numpy as np

class Network:

    def __init__(self, height, width, quantity, probability):

        self.height = height            # define fixed height for every field
        self.width = width              # define fixed width for every field
        self.quantity = quantity        # define quantity of fields to simulate
        self.probability = probability  # define a probability to simulate
        self.world = []
        self.__init_world()

    def __init_world(self):

        # 'world' is a 3-dim list of 2-dim 'network' matrices
        for i in range(self.quantity):

            # each network is a height x width matrix with values 0 and 1, determined by probability
            network = [[1 if random.uniform(0, 1) <= self.probability else 0 for _ in range(self.width)] for _ in range(self.height)]
            self.world.append(network)


    def draw_raw_networks(self):

        for i in range(self.quantity):

            # draw each network and save it
            plt.matshow(self.world[i])
            plt.savefig(str(i))
            plt.clf()


    def hoshen_kopelman(self):
        print('nothing here yet')
