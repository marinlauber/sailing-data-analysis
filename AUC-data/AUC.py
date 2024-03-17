#%%
import numpy as np
import matplotlib.pyplot as plt
import json
from mpl_toolkits.basemap import Basemap

def json_read(fname):
    with open(fname+'.json', 'r') as json_file:
        return json.load(json_file)

data = json_read("tracks")

def cm(x,y): 
    return (x/2.54,y/2.54)

# %%
# plot
fig = plt.figure(figsize=cm(20,20))
fig.subplots_adjust(left=0., right=1., bottom=0., top=0.9)

# add map with coastlines
ax = fig.add_subplot(121)
m = Basemap(projection='moll', llcrnrlat=-90, urcrnrlat=90,\
            llcrnrlon=0, urcrnrlon=360, resolution='c', lon_0=0)

#%%
skipper = ["Maxi Edmond de Rothschild","Banque Populaire XI","Actual Ultim 3",
           "Sodebo Ultim 3","SVR-Lazartigue","Adagio"]
col=["goldenrod","#1442D9","red","#4ab54a","#1486D9","#bc437f"]
time_all = []; track_all = []
for id in range(len(data["tracks"])-1):
    locForId = data["tracks"][id]["loc"]
    # add first point
    track = [[locForId[0][1]/100000,locForId[0][2]/100000]]
    time = []
    for i in range(len(locForId)-1):
        track.append([locForId[i+1][1]/100000 + track[i][0],
                      locForId[i+1][2]/100000 + track[i][1]])
        time.append((locForId[i+1][0])/100000)
    time_all.append(np.array(time))
    track = np.array(track)
    track_all.append(track)
    threshold = 90.0
    idx_wrap = np.nonzero(np.abs(np.diff(track[:,1])) > threshold)[0]+1
    idx_wrap = idx_wrap[0] if len(idx_wrap) > 0 else len(track)
    # plt.plot(track[:,1],track[:,0],lw=0.5,label=skipper[id])
    x, y = m(track[:idx_wrap,1],track[:idx_wrap,0])
    m.plot(x, y, col[id], lw=1., label=skipper[id])
    if len(track) > idx_wrap:
        x, y = m(track[idx_wrap:,1],track[idx_wrap:,0])
        m.plot(x, y, col[id], lw=1.)
m.drawcoastlines()
plt.legend(bbox_to_anchor=(1.05, 0.8))
plt.savefig("AUC.png",dpi=300)
plt.show()
# %%
fig,ax = plt.subplots(1,1,figsize=cm(20,10))
for i in range(len(time_all)):
    speed = np.linalg.norm(np.diff(track_all[i],axis=0),axis=1)/time_all[i]
    time = np.cumsum(time_all[i])
    # drop the index that crosses the 0-360 boundary
    idx_wrap = np.nonzero(np.abs(np.diff(track_all[i][:,1])) > threshold)[0]+1
    if len(idx_wrap) > 0: 
        speed = np.delete(speed,idx_wrap-1)
        time = np.delete(time,idx_wrap-1)
    # plot
    ax.plot(time,speed,label=skipper[i],alpha=0.5,color=col[i])
ax.set_ylim(0.0,50)
ax.set_xlabel("Time [Days]")
ax.set_ylabel("Speed [knots]")
plt.savefig("AUC_speed.png",dpi=300)
plt.show()
# %%
