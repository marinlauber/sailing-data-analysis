import math
import numpy as np

def calculate_compass_heading(latitudes, longitudes):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    headings = np.zeros(len(latitudes))
    lat1 = np.radians(latitudes)
    lat2 = lat1[ 1:]
    lat1 = lat1[:-1]

    diffLong = np.radians(longitudes[1:]-longitudes[:-1])
    
    x = np.sin(diffLong) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - (np.sin(lat1)
                     * np.cos(lat2) * np.cos(diffLong))
    
    # compute bearing
    initial_heading = np.arctan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_heading = np.degrees(initial_heading)
    headings[1:] = (initial_heading + 360) % 360

    return headings