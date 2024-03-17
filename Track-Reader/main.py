#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import branca.colormap as cm
import src.track_reader as tr
import folium
from src.maptiles import tiles

to_knots = lambda mps: mps / 0.5144


def figure_2():
    # get the acticity
    data = tr.get_data("activity/GS_1.tcx")

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

    fname = "GS-1.html"
    print("Saving map to : "+fname)
    fg_map.save(fname)


# figure_3()

# BOM M2 2022
# tr.show(["BOM-2022"],["2022-06-11T08:00:00.000"],
#         ["2022-06-12T02:00:00.000"], save_name="M2-BOM-2022")

# # # BOM 2021 and BOM 2022 together
# tr.show(["BOM-2021","GRG-2022"],["2021-06-12T08:00:00.000","2022-06-04T11:00:00.000"],
#         ["2021-06-12T21:06:34.000","2022-06-04T16:00:00.000"], save_name="M2-Both")

# # GRG 2023
# tr.show(["GRG-2023"],["2023-06-03T10:58:00.000"],
#         ["2023-06-03T16:18:00.000"], save_name="M2-GRG-2023")

# # SDS 2022
# tr.show(["SDS_2022_R3"],["2022-08-10T17:00:00.000"],["2022-08-10T18:19:00.000"],
#          save_name="SDS_2022_R3")

# BOM 2023
tr.show(["BOM-2023"],["2023-06-10T08:00:00.000"],["2023-06-11T03:20:00.000"],
         save_name="M2-BOM-2023")