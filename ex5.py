import numpy as np
import network
import ex2b
import matplotlib.pyplot as plt
from scipy import stats

L = 1000  # size of simulated networks
num = 100  # number of tested probabilities
p_c = 0.593   # see ex 2

p_arr = np.linspace(0, p_c, num)    # array of simulated probabilities
ln_zeta = []
ln_dp = []
j = 0

for p in p_arr:

    # print simulation-progress
    print(str(j*100/num)+'%')
    j += 1

    net = network.Network(L, L, p)
    net.hoshen_kopelman()
    zeta = net.correlation_length()
    dp = abs(p - p_c)

    # exclude percolating systems (condition p < p_c) and special cases
    if dp > 0 and zeta > 0 and not net.is_perculating() :
        ln_zeta.append(np.log(zeta))
        ln_dp.append(np.log(dp))


# plotting and linear regression
ln_dp_interpolate = np.linspace(ln_dp[0], ln_dp[-1], num)
plt.scatter(ln_dp, ln_zeta, s=4, c='r', label='Simulation')
res = stats.linregress(ln_dp, ln_zeta)
plt.plot(ln_dp_interpolate, ln_dp_interpolate * res.slope + res.intercept, label=r'ln($\zeta$) = ('
        +str(round(res.slope, 2))+r'$ \pm '+str(round(res.stderr, 2))+r') \cdot \ln(|p-p_c|) + $('
        +str(round(res.intercept, 2))+r' $\pm $'+str(round(res.intercept_stderr, 2))+')', linewidth=2, color='black')

plt.legend()
plt.grid()
plt.xlabel(r'ln(|$p-p_c$|)')
plt.ylabel(r'ln($\zeta$)')
plt.savefig('testex5')
