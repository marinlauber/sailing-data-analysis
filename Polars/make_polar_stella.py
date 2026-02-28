
#%%
#!/opt/miniconda3/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

stl = [
    (0, ()),
    (0, (1.1, 1.1)),
    (0, (2.8, 1.1)),
    (0, (2.8, 1.1, 1.1, 1.1)),
    (0, (3, 1, 1, 1, 1, 1)),
    (0, (3, 1, 3, 1, 1, 1, 1, 1)),
    (0, (7, 1, 1, 1, 1, 1)),
]
cols = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]

# get the data
data = np.loadtxt("stella_data.txt", delimiter=",")
print(data)

# transform up/down targets into points
up = data[2,1:]/np.cos(np.radians(data[1,1:]))
down = data[11,1:]/np.cos(np.pi-np.radians(data[12,1:]))

# make start and en point array
vmg_data = np.zeros((11,9))

# make the plot
fig, ax = plt.subplots(1, 1, subplot_kw=dict(polar=True), figsize=(16 / 3 , 7.5))
ax = np.array([ax], dtype=object)
ax[0].set_xticks(np.linspace(0,np.pi,5,))
ax[0].set_theta_direction(-1)
ax[0].set_theta_offset(np.pi / 2.0)
ax[0].set_thetamin(0)
ax[0].set_thetamax(180)

# make big table for NKE5000
twa_nke5000 = np.radians(np.arange(20,190,10))
data_export = np.empty((9,len(twa_nke5000)))

# go over each windspeed
for i in range(9):
    # get the TWA from the array
    twa0 = np.radians(data[3:-2,0])
    # get boat speed
    vb0 = data[3:-2,i+1]
    # add the two vmg points and the min/max required by the NKE5000
    vmg_up,vmg_dn = np.radians(data[1,i+1]),np.radians(data[12,i+1]) 
    twa = np.concatenate((twa0, np.array([vmg_up, vmg_dn, np.radians(20), np.radians(180)])))
    up = data[2,i+1]/np.cos(np.radians(data[1,i+1]))
    dn = data[11,i+1]/np.cos(np.pi-np.radians(data[12,i+1]))
    vb = np.concatenate((vb0, np.array([up, dn, 0.6*up, 0.8*dn]))) # assumptions
    # make sure they are sorted
    idx = np.argsort(twa)
    # sort the arrays
    twa = twa[idx]
    vb = vb[idx]
    # fit on smooth line
    spl = CubicSpline(twa, vb)
    twas = np.linspace(twa[0], twa[-1], 100)
    # make the export data
    data_export[i,:] = spl(twa_nke5000)
    # plot the data
    ax[0].plot(twas, spl(twas), color=cols[i], label=f"{data[0,i]}")
    ax[0].plot(twa0[1:], vb0[1:], 'x', color=cols[i])
    ax[0].plot([vmg_up,vmg_dn], [up,dn], 'o', color=cols[i], mfc="none")

# ax[i].set_rorigin(-1)
ax[0].set_rmin(0.0)
ax[0].set_xlabel(r"TWA ($^\circ$)")
ax[0].set_ylabel(r"$V_B$ (knots)", labelpad=-40)
ax[0].legend(title=r"TWS (knots)", loc=1, bbox_to_anchor=(1.15, 1.05))
plt.savefig("polar_stella_augmented_smooth.png", dpi=300, bbox_inches="tight")

# save the data
np.savetxt("data_export_stella.txt", data_export, fmt='%.4f', delimiter=",")# %%
# %%
