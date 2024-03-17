#%%
import numpy as np
import matplotlib.pyplot as plt
import json

def json_read(fname):
    with open(fname+'.json', 'r') as json_file:
        return json.load(json_file)

data = json_read("tracks-TJV")

# %%
for id in range(len(data["tracks"])):
    locForId = data["tracks"][id]["loc"]
    # lastLocDatetime = locForId[0][0]
    # add first point
    track = [[locForId[0][1]/100000,locForId[0][2]/100000]]
    for i in range(len(locForId)-1):
        # lastLocDatetime += locForId[i+1][0]
        track.append([locForId[i+1][1]/100000 + track[i][0],
                        locForId[i+1][2]/100000 + track[i][1]])
    track = np.array(track)
    plt.plot(track[:,1],track[:,0],lw=0.5)
plt.savefig("TJV.png",dpi=300)
plt.show()

# %%
