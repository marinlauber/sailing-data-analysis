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

def to_mins(string):
    _,time = string.astype(str).split("T")
    h,m,s = time.split(":")
    return 60*float(h) + float(m) + float(s)/60.

to_knots = lambda mps: mps / 0.5144

starts= ["2022-06-26T10:51:00.000","2022-06-26T11:55:10.000","2022-06-26T12:38:30.000","2022-06-26T13:24:00.000","2022-06-26T14:00:00.000"]
stops = ["2022-06-26T11:27:00.000","2022-06-26T12:21:15.000","2022-06-26T13:08:00.000","2022-06-26T13:47:00.000","2022-06-26T14:18:10.000"]


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
    # cmap = cm.LinearColormap(colors=cmap.colors,
    #                         vmin=0, vmax=max(to_knots(data.speed)),
    #                         caption="Boat Speed (knots)")
    # cmap = cm.LinearColormap(colors=cmap.colors,
    #                         vmin=0, vmax=1,
    #                         caption="Tack")

    # plot the track on the map
    # tile = tiles["osm"]
    # fg_map = folium.Map(location=[np.mean(data.latitude), np.mean(data.longitude)],
    #                     tiles=tile.url, attr=tile.attr)
    points = np.array([data.longitude.values.ravel(),
                       data.latitude.values.ravel()]).T.reshape(-1, 1, 2)
    # folium.ColorLine(points, colors=to_knots(data.speed),
    #                 colormap=cmap, nb_steps=21,
    #                 weight=10).add_to(fg_map)
    # folium.ColorLine(points, colors=data.tack,
    #                  colormap=cmap, nb_steps=2,
    #                  weight=10).add_to(fg_map)

    # segments = np.concatenate([points[:-1], points[1:]], axis=1)
    segments = np.concatenate([points[:-2],points[1:-1], points[2:]], axis=1)
    TWD = np.mean(data.heading.values % 180)
    TWD = 15
    print("mean heading data", TWD)
    TWA = np.where((data.heading.values - TWD) > 180., 360 - data.heading.values - TWD, data.heading.values - TWD)
    print(TWA)
    fig, axs = plt.subplots()
    plt.subplots_adjust(bottom=0.15)
    axfreq = plt.axes([0.15, 0.05, 0.7, 0.03])

    outline=mpe.withStroke(linewidth=7, foreground='black')

    axs.plot(data.longitude.values, data.latitude.values, color="None", lw=3, path_effects=[outline],zorder=0)

    lc = LineCollection(segments, cmap=cmap, zorder=1)
    # print(lc)
    # # Set the values used for colormapping
    # lc.set_array(to_knots(data.speed))
    # lc.set_array(data.heading.values)
    lc.set_array(abs(TWA))
    lc.set_linewidth(5)
    line = axs.add_collection(lc)
    # print(line)

    l, = axs.plot(data.longitude.values[0], data.latitude.values[0], 'ok', ms=10)

    racetime = to_mins(data.time.values[-1])-to_mins(data.time.values[0])
    freq = Slider(axfreq, 'Time', -1, racetime, 0)
    
    def update(val):
        t = np.linspace(0,racetime,len(data.latitude))
        idx = np.argmin(abs(t-val))
        l.set_xdata(data.longitude.values[idx])
        l.set_ydata(data.latitude.values[idx])

    # Call update function when slider value is changed
    freq.on_changed(update)

    # get the window extend
    sw = data[["latitude", "longitude"]].min().values.tolist()
    ne = data[["latitude", "longitude"]].max().values.tolist()
    length = 0.004
    axs.arrow(np.mean(data.longitude),np.mean(data.latitude),
              -length*np.sin(np.radians(TWD)),-length*np.cos(np.radians(TWD)),
              width=0.0008,zorder=-1000,alpha=0.2)
    axs.set_xlim(sw[1],ne[1])
    axs.set_ylim(sw[0],ne[0])
    axs.set_aspect("equal","datalim")
    fig.colorbar(line, ax=axs, label="Boat Speed (kts)")
    plt.show()
    # set zoom bounsd
    # fg_map.fit_bounds([sw, ne]) 

    # plot and save
    # fg_map.add_child(cmap)

    # fname = "M2-GPVersoix2022-R%d.html" % (race+1)
    # print("Saving map to : "+fname)
    # fg_map.save(fname)
