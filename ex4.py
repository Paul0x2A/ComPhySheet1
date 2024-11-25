import numpy as np
import network
import matplotlib.pyplot as plt
from scipy import stats

L = 4000  # size of simulated networks
num = 1000  # number of tested probabilities
p_c = 0.592   # see ex 2

p_arr = np.linspace(0, p_c, num)    # array of simulated probabilities
ln_S = []
ln_dp = []
j = 0

for p in p_arr:

    # print simulation-progress
    print(str(j*100/num)+'%')
    j += 1

    net = network.Network(L, L, p)
    net.hoshen_kopelman()
    S = net.average_cluster_size()
    dp = abs(p - p_c)

    # exclude percolating systems (condition p < p_c) and special cases
    if dp > 0 and 0 < S < p_c * L * L and not net.is_perculating() :
        ln_S.append(np.log(S))
        ln_dp.append(np.log(dp))


# plotting and linear regression
print(ln_dp)
print(ln_dp[-1])
ln_dp_interpolate = np.linspace(ln_dp[0], ln_dp[-1], num)
plt.scatter(ln_dp, ln_S, s=4, c='r', label='Simulation')
res = stats.linregress(ln_dp, ln_S)
plt.plot(ln_dp_interpolate, ln_dp_interpolate * res.slope + res.intercept, label='ln(S) = ('
        +str(round(res.slope, 2))+'$ \pm '+str(round(res.stderr, 2))+') \cdot \ln(|p-p_c|) + $('
        +str(round(res.intercept, 2))+' $\pm $'+str(round(res.intercept_stderr, 2))+')', linewidth=2, color='black')

plt.legend()
plt.grid()
plt.xlabel('ln(|$p-p_c$|)')
plt.ylabel('ln($S$)')
plt.savefig('testex4-6')
