#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import branca.colormap as cm
import src.track_reader as tr
from src.utils import calculate_compass_heading
import folium
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.patheffects as mpe
from matplotlib.colors import to_hex
from src.maptiles import tiles
from matplotlib.widgets import Slider, Button
from scipy.optimize import minimize
from matplotlib.patches import Rectangle, Arrow

def rotate(a,center,alpha):
    x = a-center; b=np.copy(x)
    b[0] = np.cos(alpha)*x[0]-np.sin(alpha)*x[1]
    b[1] = np.cos(alpha)*x[1]+np.sin(alpha)*x[0]
    return b + center

def to_mins(string):
    _,time = string.astype(str).split("T")
    h,m,s = time.split(":")
    return 60*float(h) + float(m) + float(s)/60.

to_knots = lambda mps: mps / 0.5144

starts= ["2022-06-26T10:51:00.000","2022-06-26T11:55:10.000","2022-06-26T12:38:30.000","2022-06-26T13:24:00.000","2022-06-26T14:00:00.000"]
stops = ["2022-06-26T11:27:00.000","2022-06-26T12:21:15.000","2022-06-26T13:08:00.000","2022-06-26T13:47:00.000","2022-06-26T14:18:10.000"]


print(rotate(np.array([1.,0.]),np.zeros(2),0.1))

for race,[start,stop] in enumerate(zip(starts,stops)):

    if race!=4: continue
    print(race)
    print(start)
    print(stop)
    # select only the race
    data = tr.get_data("activity/activity_9094378755.tcx")
    data = tr.cut(data, start=start, stop=stop)

    # prepare the colormap
    cmap = plt.cm.get_cmap("viridis")
   
    points = np.array([data.longitude.values.ravel(),
                       data.latitude.values.ravel()]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-2],points[1:-1],points[2:]], axis=1)
    TWD = np.mean(data.heading.values % 180)
    TWD = -2.0

    print("mean heading data", TWD)

    heading = -np.where(data.heading.values > 180, data.heading.values - 360, data.heading.values)
    TWA = heading - TWD

    # startboard 1 port 0
    Starboard = 0.5*(np.sign(TWA)+1)

    # acutal TWA
    TWA = abs(heading - TWD)
    vmg = np.cos(np.radians(TWA))*to_knots(data.speed)
    UpDown = 0.5*(np.sign(90-TWA)+1)
    stb_over_tot = sum(Starboard)/len(Starboard)
    print("Race partition stb/race", stb_over_tot)
    
    # fig, axs = plt.subplots()
    fig = plt.figure(1, figsize=(cm(21,16)), constrained_layout=False)
    gs = fig.add_gridspec(nrows=1, ncols=1)
    axs = fig.add_subplot(gs[:,:])
    # plt.subplots_adjust(left=0.25,bottom=0.15)
    fig.subplots_adjust(left=0.25,bottom=0.15)
    axfreq = plt.axes([0.15, 0.02, 0.7, 0.03])
    axtwd = plt.axes([0.1, 0.25, 0.0225, 0.63])

    outline=mpe.withStroke(linewidth=7, foreground='black')

    axs.plot(data.longitude.values, data.latitude.values, color="None", lw=3, path_effects=[outline],zorder=0)

    lc = LineCollection(segments, cmap=cmap, zorder=1)
    lc.set_array(data.gradheading)
    lc.set_linewidth(5)
    line = axs.add_collection(lc)

    l, = axs.plot(data.longitude.values[0], data.latitude.values[0], 'ok', ms=10)

    racetime = to_mins(data.time.values[-1])-to_mins(data.time.values[0])
    twd = Slider(axtwd, 'TWD', -180, 180, TWD, orientation="vertical")
    freq = Slider(axfreq, 'Time', -1, racetime, 0)

    # get the window extend
    sw = data[["latitude", "longitude"]].min().values.tolist()
    ne = data[["latitude", "longitude"]].max().values.tolist()
    dx = ne[1]- sw[1]
    dy = ne[0] - sw[0]
    x0 = np.mean(data.longitude)
    y0 = np.mean(data.latitude)

    # draw wind arrow
    length = 0.004
    dU, dW =-length*np.sin(np.radians(TWD)), -length*np.cos(np.radians(TWD))
    arrow=Arrow(x0-dU/2.,y0-dW/2.,
                 dU, dW,width=0.002,zorder=-1000,alpha=0.4)
    a = axs.add_patch(arrow)

    lp=[]; ls=[]
    for i in range(5):
        a_ = rotate(np.array([x0-dx/2,y0+(i-2)*dy/4]),np.array([x0,y0]),-np.radians(TWD-40))
        b_ = rotate(np.array([x0+dx/2,y0+(i-2)*dy/4]),np.array([x0,y0]),-np.radians(TWD-40))
        c_ = rotate(np.array([x0-dx/2,y0+(i-2)*dy/4]),np.array([x0,y0]),-np.radians(TWD+40))
        d_ = rotate(np.array([x0+dx/2,y0+(i-2)*dy/4]),np.array([x0,y0]),-np.radians(TWD+40))
        xi = [a_[0],b_[0]]
        yi = [a_[1],b_[1]]
        l1,=axs.plot(xi,yi,'--k',alpha=0.5,lw=0.5)
        xi = [c_[0],d_[0]]
        yi = [c_[1],d_[1]]
        l2,=axs.plot(xi,yi,'--k',alpha=0.5,lw=0.5)
        lp.append(l1)
        ls.append(l2)

    def update_twd(val):
        global a, line
        TWA = abs(heading - val)
        a.remove()
        dU, dW =-length*np.sin(np.radians(val)), -length*np.cos(np.radians(val))
        arrow=Arrow(x0-dU/2.,y0-dW/2.,dU, dW,width=0.002,zorder=-1000,alpha=0.4)
        a = axs.add_patch(arrow)
        vmg = np.cos(np.radians(TWA))*to_knots(data.speed)
        line.set_array(data.gradheading)
        for i in range(len(lp)):
            a_ = rotate(np.array([x0-dx/2,y0+(i-2)*dy/4]),np.array([x0,y0]),-np.radians(val-40))
            b_ = rotate(np.array([x0+dx/2,y0+(i-2)*dy/4]),np.array([x0,y0]),-np.radians(val-40))
            c_ = rotate(np.array([x0-dx/2,y0+(i-2)*dy/4]),np.array([x0,y0]),-np.radians(val+40))
            d_ = rotate(np.array([x0+dx/2,y0+(i-2)*dy/4]),np.array([x0,y0]),-np.radians(val+40))
            xi = [a_[0],b_[0]];yi = [a_[1],b_[1]]
            lp[i].set_xdata(xi); lp[i].set_ydata(yi)
            xi = [c_[0],d_[0]];yi = [c_[1],d_[1]]
            ls[i].set_xdata(xi); ls[i].set_ydata(yi)
        plt.pause(0.005)
        fig.canvas.draw_idle()

    def update(val):
        t = np.linspace(0,racetime,len(data.latitude))
        idx = np.argmin(abs(t-val))
        l.set_xdata(data.longitude.values[idx])
        l.set_ydata(data.latitude.values[idx])

    # Call update function when slider value is changed
    freq.on_changed(update)
    twd.on_changed(update_twd)

    axs.set_xlim(sw[1],ne[1])
    axs.set_ylim(sw[0],ne[0])
    axs.set_aspect("equal","datalim")
    fig.colorbar(line, ax=axs, label="Boat Speed (kts)")
    plt.show()

    lab = [r"$V_B$ (knots)", r"VMG (knots)", r"Leeway $\gamma$ ($^\circ$)",
           r"Flat", r"RED"]

    fig, ax = plt.subplots(1, 2, subplot_kw=dict(polar=True))
    for i,a in enumerate(ax):
        a.set_xticks(np.linspace(0, np.pi, 5,))
        a.set_theta_direction(-1)
        a.set_theta_offset(np.pi / 2.0)
        a.set_thetamin(0)
        a.set_thetamax(180)
        a.set_rmin(0.0)
        a.set_xlabel(r"TWA ($^\circ$)")
        a.set_ylabel(lab[i], labelpad=-40)
    TWA = TWA[data.tack==1]
    VB = data.speed[data.tack==1]
    ax[0].scatter(np.radians(TWA),to_knots(VB),
                  c=Starboard[data.tack==1],
                  alpha=0.5,cmap="RdYlGn_r")
    ax[1].scatter(np.radians(TWA),abs(vmg[data.tack==1]),
                  c=Starboard[data.tack==1],
                  alpha=0.5,cmap="RdYlGn_r")
    plt.show()
