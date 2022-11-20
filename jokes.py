import numpy as np

zapac = np.loadtxt("zapac.txt", dtype=int)
buga = np.zeros(len(zapac)).reshape(len(zapac), 1)
print(buga)