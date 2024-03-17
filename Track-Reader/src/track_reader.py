#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import branca.colormap as cm
import src.parse_tcx as parse_tcx
import src.parse_gpx as parse_gpx
import folium
import pandas as pd
from src.maptiles import tiles
from typing import Dict, Optional, Any, Union, Tuple

to_knots = lambda mps: mps / 0.5144


def get_data(fname: str) -> Optional[pd.DataFrame]:
    if fname[-3:]=='tcx':
        _, data = parse_tcx.get_dataframe_from_tcx(fname)
    if fname[-3:]=='gpx':
        data = parse_gpx.get_dataframe_from_gpx(fname)
    data = data.assign(gradheading=np.gradient(data.heading.values))
    data = data.assign(tack=np.where(abs(data.gradheading)<10,1,0))
    return data


def cut(df: pd.DataFrame, start: str, stop: str) -> pd.DataFrame:
    df = df[(df['time'] > start)]
    df = df[(df['time'] < stop)]
    return df

def show(events, starts=None, stops=None, save_name="None") -> None:
    for event,start,stop in zip(events,
                                starts,
                                stops):
        print("Reading event: %s" % event)
        data = get_data("activity/%s.tcx" % event)

        # select only the race
        data = cut(data, start=start, stop=stop)

        # prepare the colormap
        if event==events[0]:
            cmap = plt.cm.get_cmap("viridis")
        else:
            cmap = plt.cm.get_cmap("inferno")
        cmap = cm.LinearColormap(colors=cmap.colors,
                                 vmin=0, vmax=max(to_knots(data.speed)),
                                 caption="Boat Speed (knots)")

        # plot the track on the map
        tile = tiles["osm"]
        if event==events[0]:
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
        if event==events[0]:
            fg_map.fit_bounds([sw, ne]) 

        # plot and save
        fg_map.add_child(cmap)
        fname = "%s.html" % event
    if save_name!="None":
        fname = save_name+".html"
    print("Saving map to : "+fname)
    fg_map.save(fname)

    return None