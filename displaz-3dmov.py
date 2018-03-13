import sys
import numpy as np
from time import sleep
from matplotlib import pyplot as pl

# this requires the python bindings to displaz
# see https://github.com/c42f/displaz.git
import displaz

# load data and come up with coords
z = np.load('elev.npy')
zshape = (z.shape[1], z.shape[2])
x, y = np.meshgrid(np.arange(0, 10*zshape[1], 10), np.arange(0, 10*zshape[0], 10))

# get log diffs between DEMs
d = np.diff(z, axis = 0)
buf = np.log10(d[d > 0.0001])
d[d > 0.0001] = buf - buf.min()
buf = np.log10(-d[d < -0.0001])
d[d < -0.0001] = buf.min() - buf

# normalization const
dmax, dmin = d.max(), d.min()
if dmax < -dmin:
    dmax = -dmin

# load initial frame and wait 10s for the user to adjust
zi = z[1]
di = d[0]
mask = zi == -9999
xp = x[~mask]
yp = y[~mask]
zp = zi[~mask]
dp = di[~mask]
dp = (dp / dmax + 1) / 2.0
rgb = pl.cm.seismic(dp)
rgb = rgb[:, :3]
displaz.plot(np.transpose((xp, yp, zp)), color = rgb, label = 'dem')
sleep(10)

# display frame by frame
for i in range(1, z.shape[0]):
    # get i'th layer of DEM and log diffs
    zi = z[i]
    di = d[i-1]

    # mask
    mask = zi == -9999
    xp = x[~mask]
    yp = y[~mask]
    zp = zi[~mask]
    dp = di[~mask]

    # convert log diffs to rgb
    dp = (dp / dmax + 1) / 2.0
    rgb = pl.cm.seismic(dp)
    rgb = rgb[:, :3]

    # display frame and wait 100ms
    displaz.plot(np.transpose((xp, yp, zp)), color = rgb, label = 'dem')
    sleep(0.1)
