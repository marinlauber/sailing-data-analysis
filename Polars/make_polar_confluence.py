
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
data = np.loadtxt("confluence_polars.csv", delimiter=";", skiprows=2)
data_calc = np.loadtxt("Polaire calcul Mike SNIM.pol", skiprows=1)
print(data)
print(data_calc)

# # make start and en point array
# new_data = np.zeros((10,100))

# make the plot
fig, ax = plt.subplots(1, 1, subplot_kw=dict(polar=True), figsize=(16 / 3 , 7.5))
ax = np.array([ax], dtype=object)
ax[0].set_xticks(np.linspace(0,np.pi,5,))
ax[0].set_theta_direction(-1)
ax[0].set_theta_offset(np.pi / 2.0)
ax[0].set_thetamin(0)
ax[0].set_thetamax(180)

# labels
tws_labels = [4,6,8,10,12,14,16,20,24]

# # make big table for NKE5000
twa_qtvlm = np.linspace(np.radians(20), np.radians(180), 20)
data_qtvlm = np.empty((len(twa_qtvlm)+1,len(tws_labels)+1))

# first column is TWA in degrees
data_qtvlm[1:,0] = np.degrees(twa_qtvlm)
data_qtvlm[0,1:] = tws_labels

# go over each wind speed
for i in range(np.shape(data)[1]-1):
    # get the TWA from the array
    twa = np.radians(data[:,0])
    # get boat speed
    vb = data[:,i+1]
    # remove points that have no boat speed
    mask = vb!=0
    twa = twa[mask]
    vb = vb[mask]
    # add TWa=20 and TWA=180 to lose the polars
    twa = np.concatenate((twa, np.array([np.radians(20), np.radians(180)])))
    vb = np.concatenate((vb, np.array([0.6*vb[0], min(8.0,0.7*vb[-1])]))) # assumptions
    # if i>=7:
        # vb[-1] = 8.0
    # make sure they are sorted
    idx = np.argsort(twa)
    # sort the arrays
    twa = twa[idx]
    vb = vb[idx]
    # fit on smooth line
    spl = CubicSpline(twa, vb)
    # make the export data
    data_qtvlm[1:,i+1] = spl(twa_qtvlm)
    # plot the data
    ax[0].plot(twa_qtvlm, spl(twa_qtvlm), color=cols[i], label=f"{tws_labels[i]}")
    ax[0].plot(twa, vb, 'x', color=cols[i])

ax[0].set_rorigin(-1)
ax[0].set_rmin(0.0)
ax[0].set_xlabel(r"TWA ($^\circ$)")
ax[0].set_ylabel(r"$V_B$ (knots)", labelpad=-40)
ax[0].legend(title=r"TWS (knots)", loc=1, bbox_to_anchor=(1.15, 1.05))
plt.savefig("polar_confluence_augmented_smooth.png", dpi=300, bbox_inches="tight")
plt.show()
# save the data
np.savetxt("polar_confluence.txt", data_qtvlm, fmt='%.4f', delimiter=";")# %%
# # %%

# %%
