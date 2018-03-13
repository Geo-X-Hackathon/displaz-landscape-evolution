import sys
import numpy as np

# open one file to get dims
z = np.loadtxt(sys.argv[1], skiprows = 6)

# malloc empty array
z = np.zeros((len(sys.argv)-1, z.shape[0], z.shape[1]))

# read files one by one
for i in range(1, len(sys.argv)):
    z[i-1, :, :] = np.loadtxt(sys.argv[i], skiprows = 6)

np.save('elev.npy', z)
