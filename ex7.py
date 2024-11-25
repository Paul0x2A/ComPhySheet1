import numpy as np
import matplotlib.pyplot as plt
import network


def get_relative_size_of_largest_percolating_cluster(net: network.Network):
    return net.N[net.get_largest_percolating_cluster()] / net.get_total_occupied_spots()


num_p = 200
beta = 5 / 36
nu = 4 / 3
p_c = 0.593
L_arr = [10, 50, 100, 200, 500, 1000]
num_L = len(L_arr)
p_arr = np.linspace(p_c - 0.1, p_c + 0.3, num_p)

x = []
y = []

for i in range(len(L_arr)):

    x_L = []
    y_L = []
    for j in range(len(p_arr)):

        # print progress
        print(str(round(100 * (i * num_p + j) / (num_p * num_L), 1))+'%')

        L = L_arr[i]
        p = p_arr[j]
        net = network.Network(L, L, p)
        net.hoshen_kopelman()

        if not net.is_percolating():
            continue

        y_L.append(((L ** (beta / nu)) * get_relative_size_of_largest_percolating_cluster(net)))
        x_L.append(((p - p_c) * (L ** (1 / nu))))

    x.append(x_L)
    y.append(y_L)

for i in range(len(x)):
    plt.scatter(x[i], y[i], label='L = '+str(L_arr[i]), s=6)

plt.legend()
plt.grid()
plt.xlabel(r'$(p - p_c) L^{1/\nu}$')
plt.ylabel(r'$P_L L^{\beta / \nu}$')
plt.savefig('ex7')
