#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import branca.colormap as cm
import src.track_reader as tr
import folium

from src.maptiles import tiles

to_knots = lambda mps: mps / 0.5144

def figure_1():
    for event in ["Ypso"]:

        data = tr.get_data("activity/%s.gpx" % event)

        # prepare the colormap
        cmap = plt.cm.get_cmap("viridis")
        cmap = cm.LinearColormap(colors=cmap.colors,
                                vmin=0, vmax=max(to_knots(data.speed)),
                                caption="Boat Speed (knots)")

        # plot the track on the map
        tile = tiles["osm"]
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
        fg_map.fit_bounds([sw, ne]) 

        # plot and save
        fg_map.add_child(cmap)

        fname = "Ypso-BOM-22.html"
        print("Saving map to : "+fname)
        fg_map.save(fname)

def figure_2():

    data = tr.get_data("activity/Roberto.gpx")

    # prepare the colormap
    cmap = plt.cm.get_cmap("viridis")
    cmap = cm.LinearColormap(colors=cmap.colors,
                            vmin=0, vmax=10,
                            caption="Boat Speed (knots)")

    # plot the track on the map
    tile = tiles["osm"]
    fg_map = folium.Map(location=[np.mean(data.latitude), np.mean(data.longitude)], tiles=None)
    folium.TileLayer(tiles=tile.url, attr=tile.attr,name="Open Street Map",control=True).add_to(fg_map)
    tile = tiles["esri_aerial"]
    folium.TileLayer(tiles=tile.url, attr=tile.attr,name="Nat Geo Map",control=True).add_to(fg_map)

    points = np.array([data.latitude,data.longitude]).T.reshape(-1, 2)
    folium.ColorLine(points, colors=to_knots(data.speed),
                     colormap=cmap, nb_steps=21,
                     weight=10,name="Roberto").add_to(fg_map)
    
    # second set of data
    data = tr.get_data("activity/Little-Nemo-II.gpx")
    points = np.array([data.latitude,data.longitude]).T.reshape(-1, 2)
    folium.ColorLine(points, colors=to_knots(data.speed),
                     colormap=cmap, nb_steps=21,
                     weight=10,name="Little-Nemo-II").add_to(fg_map)

    # get the window extend
    sw = data[["latitude", "longitude"]].min().values.tolist()
    ne = data[["latitude", "longitude"]].max().values.tolist()

    # set zoom bounsd
    fg_map.fit_bounds([sw, ne]) 

    # plot and save
    fg_map.add_child(cmap)
    folium.LayerControl(collapsed=True).add_to(fg_map)

    fname = "Roberto-BOM-22.html"
    print("Saving map to : "+fname)
    fg_map.save(fname)

# figure_1()
figure_2()
