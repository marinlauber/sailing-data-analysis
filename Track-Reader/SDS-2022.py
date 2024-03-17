

def figure():
    # get the acticity
    data = tr.get_data("activity/SDS_2022_R3.tcx")

    # select only the race CET=UTC-2
    starts = "2022-08-10T17:00:00.000"
    stops = "2022-08-10T18:19:00.000"
    data = tr.cut(data, start=starts, stop=stops)

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

    fname = "SDS_2022_R3.html"
    print("Saving map to : "+fname)
    fg_map.save(fname)


if __name__=="__main__":
    figure()