#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import branca.colormap as cm
import src.track_reader as tr
import folium
# from matplotlib.colors import to_hex
# from matplotlib.collections import LineCollection
# from matplotlib.colors import ListedColormap, BoundaryNorm
from src.maptiles import tiles

to_knots = lambda mps: mps / 0.5144

def figure():
    for event,starts,stops in zip(["BOM-2022"],
                                ["2022-06-11T08:00:00.000"],
                                ["2022-06-12T02:00:00.000"]):

        data = tr.get_data("activity/%s.tcx" % event)

        # select only the race
        data = tr.cut(data, start=starts, stop=stops)

        # prepare the colormap
        if event[0]=="B":
            cmap = plt.cm.get_cmap("viridis")
        else:
            cmap = plt.cm.get_cmap("inferno")
        cmap = cm.LinearColormap(colors=cmap.colors,
                                vmin=0, vmax=max(to_knots(data.speed)),
                                caption="Boat Speed (knots)")

        # plot the track on the map
        tile = tiles["osm"]
        if event[0]=="B":
            fg_map = folium.Map(location=[np.mean(data.latitude), np.mean(data.longitude)],
                                tiles=tile.url, attr=tile.attr)
        points = np.array([data.latitude,data.longitude]).T.reshape(-1, 2)
        folium.ColorLine(points, colors=to_knots(data.speed),
                        colormap=cmap, nb_steps=21,
                        weight=10).add_to(fg_map)

        # get the window extend
        sw = data[["latitude", "longitude"]].min().values.tolist()
        ne = data[["latitude", "longitude"]].max().values.tolist()

        # set zoom bounsd
        if event[0]=="B":
            fg_map.fit_bounds([sw, ne]) 

        # plot and save
        fg_map.add_child(cmap)

        fname = "M2-%s.html" % event
        print("Saving map to : "+fname)
        fg_map.save(fname)

if __name__=="__main__":
    figure()
