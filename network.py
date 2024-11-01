import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

cmap = ListedColormap([[224, 224, 224], [34, 34, 34]])

class Network:

    def __init__(self, height, width, probability):

        self.height = height
        self.width = width
        self.probability = probability

        self.network = [[1 if random.uniform(0, 1) <= self.probability else 0 for _ in range(self.width)] for _ in range(self.height)]
        self.labeled_network = []   # Labeled network contains cluster names. Needs to be corrected for unions by the cluster-vector
        self.N = [0]                # Cluster-Vector containing cluster-sizes. Negative values represent new cluster-names after a union



    def __solve_label_conflict(self, conflicted_label):

            # TODO: make method more efficient

            m = self.N[conflicted_label]
            if m < 0:
                while True:
                    r = -m
                    m = self.N[r]
                    if m >= 0:
                        break
                return r
            else:
                return conflicted_label

    def draw_raw_network(self, name):

        # draw network and save it
        plt.matshow(self.network, cmap=cmap)
        plt.savefig(name)
        plt.clf()


    def draw_labeled_network(self, name):

        if self.labeled_network == []:
            print('no labels found, run hoshen-kopelman first')

        else:
            print(self.labeled_network)
            print('\n')
            print(self.N)
            quantity_measured = 0
            for i in self.N:
                if i > 0:
                    quantity_measured += i

            quantity_set = 0
            for row in range(self.height):
                for col in range(self.width):
                    if self.network[row][col] != 0:
                        quantity_set += 1

            print('\n'+str(quantity_measured - quantity_set))
            fig, ax = plt.subplots()
            ax.matshow(self.labeled_network, cmap=cmap, interpolation='none')

            for (i, j), z in np.ndenumerate(self.labeled_network):
                if z != self.width * self.height:       # don't draw empty fields

                    if self.N[z] < 0:                   # correct for unions, displayed by negative values in N
                         z = self.__solve_label_conflict(z)
                    ax.text(j, i, format(z), ha='center', va='center',
                        bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3'))

            plt.savefig(name)
            plt.clf()



    def hoshen_kopelman(self):

        max_label = 1                       # current max cluster label, counting up (zero shall be excluded)

        for row in range(self.height):
            labeled_row = []

            for col in range(self.width):

                if self.network[row][col] != 0:
                    tile_above = 0 if row < 1 else self.network[row - 1][col]
                    tile_left = 0 if col < 1 else self.network[row][col - 1]

                    label_above = self.width * self.height if row < 1 else self.labeled_network[row - 1][col]
                    label_left = self.width * self.height if col < 1 else labeled_row[col-1]


                    if tile_left == 0 and tile_above == 0:
                        labeled_row.append(max_label)
                        max_label += 1
                        self.N.append(1)

                    elif tile_left == 0 and tile_above == 1:
                        if self.N[label_above] < 0:
                            resolved_label = self.__solve_label_conflict(label_above)
                            labeled_row.append(resolved_label)
                            labeled_row[col-1] = resolved_label
                            self.N[resolved_label] += 1

                        else:
                            labeled_row.append(label_above)
                            self.N[label_above] += 1


                    elif tile_left == 1 and tile_above == 0:

                        if self.N[label_left] < 0:
                            resolved_label = self.__solve_label_conflict(label_left)
                            labeled_row.append(resolved_label)
                            labeled_row[col-1] = resolved_label
                            self.N[resolved_label] += 1
                        else:
                            labeled_row.append(label_left)
                            self.N[label_left] += 1

                    elif tile_left == 1 and tile_above == 1:

                        resolved_label_left = label_left if self.N[label_left] > 0 else self.__solve_label_conflict(label_left)
                        resolved_label_above = label_above if self.N[label_above] > 0 else self.__solve_label_conflict(label_above)

                        if resolved_label_above < resolved_label_left:

                            labeled_row.append(resolved_label_above)

                            labeled_row[col-1] = resolved_label_left
                            self.labeled_network[row-1][col] = resolved_label_above

                            self.N[resolved_label_above] += 1
                            self.N[resolved_label_above] += self.N[resolved_label_left]
                            self.N[resolved_label_left] = - resolved_label_above

                        elif label_above > label_left:

                            labeled_row.append(resolved_label_left)

                            labeled_row[col-1] = resolved_label_left
                            self.labeled_network[row-1][col] = resolved_label_above

                            self.N[resolved_label_left] += 1
                            self.N[resolved_label_left] += self.N[resolved_label_above]
                            self.N[resolved_label_above] = - resolved_label_left

                        elif label_above == label_left:
                            labeled_row.append(label_left)
                            self.N[label_left] += 1


                else:
                    labeled_row.append(self.width * self.height)

            self.labeled_network.append(labeled_row)



