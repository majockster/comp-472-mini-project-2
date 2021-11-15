import numpy as np
#x = np.arange(9).reshape((3,3))
x = [[0, 1, 2],
 [3, 4, 5],
 [6, 7, 8]]

print(x)
print("\n")
print(np.fliplr(x))
print("\n")
#for i in range(-(3-2), 3-1):
print(np.diag(np.fliplr(x), k = -1))
