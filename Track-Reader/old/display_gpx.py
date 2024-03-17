#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import branca.colormap as cm
import parse_tcx
import parse_gpx
import folium
from src.maptiles import tiles

to_knots = lambda mps: mps / 0.5144


# tcx = tcxparser.TCXParser('BOM2021.tcx')
# print(tcx.position_values())
# print(tcx.speed_values())
# gpx = gpxpy.parse(open('BOM2021.gpx'))
# print("{} track(s)".format(len(gpx.tracks)))
# track = gpx.tracks[0]
# print("{} segment(s)".format(len(track.segments)))
# segment = track.segments[0]
# print("{} point(s)".format(len(segment.points)))
# data = []
# segment_length = segment.length_3d()
# for point_idx, point in enumerate(segment.points):
#     data.append([point.longitude, point.latitude,
#                  point.elevation, point.time, to_knots(segment.get_speed(point_idx))])
# columns = ['Longitude', 'Latitude', 'Altitude', 'Time', 'Speed']
# df = DataFrame(data, columns=columns)
# df = df[(df['Time'] > '2021-06-12T08:00:00.000')]
# df = df[(df['Time'] < '2021-06-12T21:06:34.000')]
# print(df.Speed.max())
# position = np.array(tcx.position_values())
# speed = to_knots(np.array(tcx.speed_values()))
# 

data = parse_gpx.get_dataframe_from_gpx('activity_6955131280.gpx')
# data = parse_tcx.get_dataframe_from_tcx('activity_6955131280.tcx')

viridis = plt.cm.get_cmap('viridis')
cmap = cm.LinearColormap(colors=viridis.colors,
                         vmin=0, vmax=max(to_knots(data.speed)),
                         caption='Boat Speed (knots)')


tile = tiles['esri_natgeo']
fg_map = folium.Map(location=[np.mean(data.latitude), np.mean(data.longitude)],
                    tiles=tile.url, attr=tile.attr)
points = np.array([data.latitude,data.longitude]).T.reshape(-1, 2)
folium.ColorLine(points, colors=to_knots(data.speed),
                 colormap=cmap, nb_steps=21,
                 weight=5).add_to(fg_map)

sw = data[['latitude', 'longitude']].min().values.tolist()
ne = data[['latitude', 'longitude']].max().values.tolist()
# sw = (min(position[:,0]),min(position[:,1]))
# ne = (max(position[:,0]),max(position[:,1]))

fg_map.fit_bounds([sw, ne]) 

fg_map.add_child(cmap)
fname = 'M2-BOM-2021.html'
print('Saving map to : '+fname)
fg_map.save(fname)
