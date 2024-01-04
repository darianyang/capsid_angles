"""
Make a plot of the hex and pent T188 distances.
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_angles(path, ax, color=None, label=None):
    """
    Plot oa 1 and 2 and c2.
    """
    #oa1 = np.loadtxt(f"{path}/o_angle.dat")[:,1]
    #oa2 = np.loadtxt(f"{path}/o_angle.dat")[:,2]
    #c2 = np.loadtxt(f"{path}/c2_angle.dat")[:,1]
    tt = np.loadtxt(f"{path}/tt_dist.dat")[:,1]

    #ax.scatter(oa1, tt, color=color, label=label, s=10)
    #ax.scatter(oa1, c2, color=color, label=label, s=10)
    ax.hist(tt, color=color, label=label, bins=20)

fig, ax = plt.subplots()
plot_angles("HEXNC", ax, "k", "HEX-HEX")
plot_angles("PENTNC", ax, "red", "PENT-HEX")
#ax.set_xlim(0, 70)
#ax.set_ylim(0, 70)
#ax.set_ylim(2, 18)
ax.set_xlim(2, 18)

#ax.scatter(29.5, 29.5, label="2KOD")
#ax.scatter(19.9, 19.9, label="1A43")
#ax.plot([0, 1], [0, 1], transform=ax.transAxes, color="grey", ls="--")
plt.legend()
plt.show()
#plt.savefig("o_angles.png", dpi=300, transparent=True)
