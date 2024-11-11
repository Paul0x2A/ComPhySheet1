import random
from netrc import netrc

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

cmap = ListedColormap([[34, 34, 34], [224, 224, 224]])

class Network:

    # if save is true, plots will be exported. Not useful for jupyter
    def __init__(self, height, width, probability):

        self.height = height
        self.width = width
        self.probability = probability
        self.analysed = False # True if hoshen koppelman was used
        self.fixed = True # True if all conlficts are fixed in the network

        # True, False matrix with occupied spots, hstack and vstack put an unoccupied row/column on the left/top for simpler computation
        self.network = np.hstack((np.ones((height + 1, 1)), np.vstack((np.ones((1, width)), np.random.uniform(0, 1, (height, width)))))) <= probability
        # Matrix with cluster labels, 0 is none
        self.labeled_network = np.zeros((height, width), dtype=np.uint32)   # Labeled network contains cluster names. Needs to be corrected for unions by the cluster-vector
        # Map of cluster label to cluster size, negative size links to another cluster, height*width/2 is max cluster amount (checkerboard pattern)
        self.N = np.zeros(int(np.ceil(height*width/2)), dtype=np.int32)                # Cluster-Vector containing cluster-sizes. Negative values represent new cluster-names after a union
        #print(self.network)

    # does not fix labels in the network!
    def __resolve_label(self, conflicted_label):

        r = conflicted_label
        m = self.N[conflicted_label]
        if m < 0:
            while m < 0:
                r = -m
                m = self.N[r]
        return r

    def plot_grid(self, fig=None, ax=None, labeled=False, file_name=None, network=None):
        """
        Plots a given 2d matrix with true, false values
        :param fig: fig to create axis from (created by default)
        :param ax: axis to plot on (created by default)
        :param labeled: if labels should be drawn on each occupied cell
        :param file_name: file name to save the plot to (default: None)
        :param network: network to plot (default self.network)
        """
        if not self.analysed: self.hoshen_kopelman()
        if ax is None:
            if fig is None:
                fig = plt.figure()
            ax = fig.subplots()
        if network is None:
            network = np.array([a[1:] for a in self.network[1:]])
        ax.matshow(network, cmap=cmap)
        if labeled:
            for i, j in np.ndindex(self.labeled_network.shape):
                l = self.label_at(i, j)
                ax.text(j, i, f'{l}', ha='center', va='center', color=(0.9, 0.9, 0.9))
            self.fixed = True
        if file_name is not None:
            plt.savefig(f'out/{file_name}.png')

    def plot_cluster(self, cluster_label, fig=None, ax=None, labeled=False, file_name=None):
        """
        Plots a cluster of this network
        :param cluster_label: label of cluster to plot
        :param fig: fig to create axis from (created by default)
        :param ax: axis to plot on (created by default)
        :param labeled: if labels should be drawn on each occupied cell
        :param file_name: file name to save the plot to (default: None)
        """
        self.fix_labels()
        n = np.copy(self.labeled_network) # copy to not modify this network
        n[n != cluster_label] = 0      # set all wich are not the cluster to 0
        n = n[~np.all(n == 0, axis=1)] # delete columns with 0
        n = n[:, ~np.all(n == 0, axis=0)] # delete rows with 0
        self.plot_grid(fig, ax, labeled, file_name, network=n>0)

    def plot_largest_cluster(self, fig=None, ax=None, labeled=False, file_name=None):
        self.plot_cluster(np.argmax(self.N), fig=fig, ax=ax, labeled=labeled, file_name=file_name)

    def is_occupied(self, row, col):
        return self.network[row+1][col+1]

    # retrieves and fixes a label at a position
    def label_at(self, row, col):
        l = self.labeled_network[row][col]
        if self.fixed: return l
        n = self.N[l]
        if n < 0:
            while True:
                l = -n
                n = self.N[l]
                if n >= 0: break
            self.labeled_network[row][col] = l
        return l

    # fixes all labels in the network
    def fix_labels(self):
        if not self.analysed: self.hoshen_kopelman()
        if self.fixed: return
        for i, j in np.ndindex(self.labeled_network.shape):
            self.label_at(i, j)
        self.fixed = True

    # calculates cluster which perculate
    def get_perculations(self):
        """
        :return: an array of labels which perculate (touch top and bottom) except 0
        """
        if not self.analysed: self.hoshen_kopelman()
        top = self.labeled_network[0]
        bot = self.labeled_network[-1]
        if not self.fixed:
            for i in range(len(top)):
                top[i] = self.__resolve_label(top[i])
                bot[i] = self.__resolve_label(bot[i])
        perc = np.intersect1d(top, bot)
        return perc[perc != 0]

    def is_perculating(self):
        return len(self.get_perculations()) > 0

    def hoshen_kopelman(self):
        if self.analysed: return
        self.analysed = True
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
                        label = self.__resolve_label(label)
                        self.labeled_network[row-1][col-1] = label
                        self.N[label] += 1     
                    else: # both neighbors must be occupied -> conflict

                        resolved_label_left = self.__resolve_label(label_left)
                        resolved_label_above = self.__resolve_label(label_above)

                        if resolved_label_left == resolved_label_above: # left and above are the same -> append cell
                            self.labeled_network[row-1][col-1] = resolved_label_left
                            self.N[resolved_label_left] += 1
                            continue

                        label = resolved_label_left if resolved_label_left < resolved_label_above else resolved_label_above
                        other_label = resolved_label_left if resolved_label_left > resolved_label_above else resolved_label_above

                        self.labeled_network[row-1][col-1] = label
                        self.N[label] += 1
                        self.N[label] += self.N[other_label]
                        self.N[other_label] = -int(label)
                        self.fixed = False
            # end col loop
        # end row loop                    

    def cluster_sizes(self):
        return dict(zip(*np.unique(np.where(self.N > 0,  self.N, np.zeros(len(self.N))), return_counts=True)))

    # calculates the average cluster size of the analyzed network
    def average_cluster_size(self):

        if not self.analysed: self.hoshen_kopelman()    # check that network is analyzed
        first_moment = 0
        second_moment = 0
        cluster_sizes = self.cluster_sizes()
        for s in cluster_sizes:
            n_s = s * cluster_sizes[s] / (self.width * self.height)     # probability that a random tile belongs to a cluster of size s
            first_moment += s * n_s
            second_moment += (s ** 2) * n_s

        return second_moment / first_moment
