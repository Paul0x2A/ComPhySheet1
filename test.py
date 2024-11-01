
import numpy as np

height = 4
width = 2
a = np.hstack((np.ones((height + 1, 1)), np.vstack((np.ones((1, width)), np.random.uniform(0, 1, (height, width))))))
print(a)
print(a <= 0.3)
print(np.array([a1[1:] for a1 in a[1:]]))

b = np.array([2, 0, 6, 9, -5, -1, 1])
print(np.sum(b, where=b>0))
