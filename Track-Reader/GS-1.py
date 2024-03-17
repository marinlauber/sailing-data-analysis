
def figure():
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

if __name__=="__main__":
    figure()