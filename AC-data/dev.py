import os
import numpy as np
import json
import pickle
import struct
from datetime import datetime
from pyproj import CRS, Transformer
import matplotlib.pyplot as plt
from processed_data import read_events
from matplotlib.collections import LineCollection

DATA_KEYS = ["headingIntep","heelInterp","pitchInterp","speedInterp","elevInterp", 
             "twsInterp","twdInterp","vmgInterp","leftFoilPosition","rightFoilPosition"]


def cm(x, y): return (x/2.56, y/2.56)

def read_race(event, i):
    path = f"{event}/{i}"
    boats = read_boats(f"raw/{path}")

    crs_utm = CRS.from_epsg(27260)
    # Web mercator
    crs_wm = CRS.from_epsg(3857)
    tr = Transformer.from_crs(crs_utm, crs_wm)

    # store new boat
    for b in boats:
        print(b.keys())
        new_boat = {"Id": b["teamId"]}
        boat_lat = []
        boat_lon = []
        lon_y_raw = [i[0] for i in b["coordIntep"]["xCerp"]["valHistory"]]
        lat_y_raw = [i[0] for i in b["coordIntep"]["yCerp"]["valHistory"]]
        time = [i[1] for i in b["coordIntep"]["xCerp"]["valHistory"]]
        new_boat["time"] = time
        for i, (lon, lat) in enumerate(zip(lon_y_raw, lat_y_raw)):
            lon, lat = tr.transform(lon, lat)
            boat_lon.append(lon)
            boat_lat.append(lat)
        new_boat["lat"] = lat_y_raw
        new_boat["lon"] = lon_y_raw
        for key in DATA_KEYS:
            # interpolate on identical time array
            x = [i[1] for i in b[key]["valHistory"]] # time
            y = [i[0] for i in b[key]["valHistory"]] # variable
            new_boat[key] = np.interp(time, x, y)
    return new_boat


def read_boats(path):
    print("Reading boats")
    if not "boat1.json" in os.listdir(path) and not "boat2.json" in os.listdir(path):
        raise FileNotFoundError
    with open(f"{path}/boat1.json", "rb") as f:
        boat1 = json.load(f)
    with open(f"{path}/boat2.json", "rb") as f:
        boat2 = json.load(f)
    return boat1, boat2


all_keys = ["coordIntep","headingIntep","heelInterp","pitchInterp","dtlInterp","speedInterp","elevInterp", 
             "penaltyCountInterp","protestInterp","statusInterp","sowInterp","vmgInterp","twsInterp","twdInterp",
             "legInterp","legProgressInterp","rankInterp","leftFoilState","rightFoilState","leftFoilPosition", 
             "rightFoilPosition","ruddleAngle","foilMoveTime","boatId","teamId"]

# path = "raw/ac2021/1/"
# with open(f"{path}/boat1.json", "rb") as f:
    # boat1 = json.load(f)

# print(boat1.keys())
# # for key in data_keys:
# #     print(key)
# #     print(boat1[key]["xCerp"]["valHistory"])

#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def cm(x, y): return (x/2.6, y/2.56)

def polar(ax):
    ax.set_xticks(np.linspace(0, np.pi, 5,))
    ax.set_theta_direction(-1)
    ax.set_theta_offset(np.pi / 2.0)
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    ax.set_rmin(0.0)
    ax.set_xlabel(r"TWA ($^\circ$)")
    ax.set_ylabel(r"$V_B$ (knots)", labelpad=-40)
    return ax


# data = read_events(["ac2021"])
# print(data)

data = read_race("ac2021", "1")

fig, ax = plt.subplots(3,4, figsize=cm(20,14))
ax = ax.ravel()
ax[0].plot(data["lon"], data["lat"])
for a, key in zip(ax[1:],DATA_KEYS):
    a.plot(data[key])
    a.set_title(key)
plt.show()

fig = plt.figure(figsize=cm(18,14), constrained_layout=False)
gs = fig.add_gridspec(2, 4)
ax1 = fig.add_subplot(gs[:2,:3])
ax2 = fig.add_subplot(gs[0,3], polar=True)
ax2 = polar(ax2)
ax3 = fig.add_subplot(gs[1,3])

# track of boat
lon = data["lon"]
lat = data["lat"]
ax1.plot(lon, lat)
ax1.set_aspect('equal')
points = np.array([lon, lat]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
norm = plt.Normalize(data["speedInterp"].min(), data["speedInterp"].max())
lc = LineCollection(segments, cmap='viridis', norm=norm)
lc.set_array(data["speedInterp"])
lc.set_linewidth(2)
line = ax1.add_collection(lc)
fig.colorbar(line, ax=ax1)

twa = np.arccos(np.array(data["vmgInterp"])/np.array(data["speedInterp"]))
# abs(np.array(data["twdInterp"]) - np.array(data["headingIntep"]))
ax2.plot(twa, data["speedInterp"])

ax3.plot(twa, data["time"])
plt.show()




# path = "ac36data/ac2021/1/"
# with open(f"{path}/boats.bin", "rb") as f:
#     data = pickle.load(f)
# for key in data:
#     print(len(data[key]))
# print(data.keys())
