import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

cmap = ListedColormap([[34, 34, 34], [224, 224, 224]])

class Network:

    # if save is true, plots will be exported. Not useful for jupyter
    def __init__(self, height, width, probability, save=False):

        self.height = height
        self.width = width
        self.probability = probability
        self.save = save

        # True, False matrix with occupied spots, hstack and vstack put an unoccupied row/column on the left/top for simpler computation
        self.network = np.hstack((np.ones((height + 1, 1)), np.vstack((np.ones((1, width)), np.random.uniform(0, 1, (height, width)))))) <= probability
        # Matrix with cluster labels, 0 is none
        self.labeled_network = np.zeros((height, width), dtype=np.uint32)   # Labeled network contains cluster names. Needs to be corrected for unions by the cluster-vector
        # Map of cluster label to cluster size, negative size links to another cluster, height*width/2 is max cluster amount (checkerboard pattern)
        self.N = np.zeros(int(np.ceil(height*width/2)), dtype=np.int32)                # Cluster-Vector containing cluster-sizes. Negative values represent new cluster-names after a union
        #print(self.network)


    def __solve_label_conflict(self, conflicted_label):
        # TODO: make method more efficient
        r = conflicted_label
        m = self.N[conflicted_label]
        if m < 0:
            while m < 0:
                r = -m
                m = self.N[r]
            #self.N[conflicted_label] = r  # updating causes problems, would need to update labeled network
        return r

    def draw_raw_network(self, name):
        # draw network and save it
        plt.matshow(np.array([a[1:] for a in self.network[1:]]), cmap=cmap)
        if self.save:
            plt.savefig(f"out/{name}.png")
            plt.clf()


    def draw_labeled_network(self, name):
        #print(self.labeled_network)
        #print('\n')
        #print(self.N)
        #quantity_measured = np.sum(self.N, where=self.N > 0)
        #quantity_set = self.network.sum() # works since True == 1
        #print('\n'+str(quantity_measured - quantity_set))
        fig, ax = plt.subplots()
        ax.matshow(np.array([a[1:] for a in self.network[1:]]), cmap=cmap, interpolation='none')

        for (i, j), z in np.ndenumerate(self.labeled_network):
            if z != 0:       # don't draw empty fields
                l = self.__solve_label_conflict(z)
                ax.text(j, i, f'{l}', ha='center', va='center', color=(0.9, 0.9, 0.9))
        if self.save:
            plt.savefig(f'out/{name}.png')
            plt.clf()



    def hoshen_kopelman(self):
        max_label = int(1)                       # current max cluster label, counting up (zero shall be excluded)
        for row in range(1, self.height + 1): # first col/row is empty

            for col in range(1, self.width + 1):

                if self.network[row][col]:
                    tile_above = self.network[row - 1][col]
                    tile_left = self.network[row][col - 1]

                    label_above = self.labeled_network[row - 2][col-1]
                    label_left = self.labeled_network[row-1][col-2]


                    if not tile_left and not tile_above: # both neighbors empty -> new cluster
                        self.labeled_network[row-1][col-1] = int(max_label)
                        self.N[max_label] = 1
                        max_label += 1
                    elif tile_left != tile_above: # one neighbor is empty and one is not -> append cell
                        label = label_above if tile_above else label_left
                        label = self.__solve_label_conflict(label)
                        self.labeled_network[row-1][col-1] = label
                        self.N[label] += 1     
                    else: # both neighbors must be occupied -> conflict

                        resolved_label_left = self.__solve_label_conflict(label_left)
                        resolved_label_above = self.__solve_label_conflict(label_above)

                        if resolved_label_left == resolved_label_above: # left and above are the same -> append cell
                            self.labeled_network[row-1][col-1] = resolved_label_left
                            self.N[resolved_label_left] += 1
                            continue

                        label = resolved_label_left if resolved_label_left < resolved_label_above else resolved_label_above
                        other_label = resolved_label_left if resolved_label_left > resolved_label_above else resolved_label_above

                        #labeled_row[col-1] = resolved_label_left
                        #self.labeled_network[row-1][col] = resolved_label_above
                        self.labeled_network[row-2][col-1] = label
                        self.labeled_network[row-1][col-2] = label
                        self.labeled_network[row-1][col-1] = label
                        self.N[label] += 1
                        self.N[label] += self.N[other_label]
                        self.N[other_label] = -int(label)
            # end col loop
        # end row loop                    

    def cluster_sizes(self):
        return dict(zip(*np.unique(np.where(self.N > 0,  self.N, np.zeros(len(self.N))), return_counts=True)))
