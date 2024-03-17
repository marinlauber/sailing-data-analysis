"""Some functions for parsing a GPX file (specifically, a GPX file
downloaded from Strava, which was generated based on data recorded by a
Garmin vívoactive 3) and creating a Pandas DataFrame with the data.
"""

from typing import Dict, Union
from datetime import datetime

import gpxpy
import pandas as pd

from src.utils import calculate_compass_heading


# The XML namespaces used by the GPX file for extensions, used when parsing the extensions
NAMESPACES = {'garmin_tpe': 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1'}

# The names of the columns we will use in our DataFrame
COLUMN_NAMES = ['latitude', 'longitude', 'elevation', 'time', 'heart_rate', 'cadence', 'speed', 'heading']

def get_gpx_point_data(point: gpxpy.gpx.GPXTrackPoint) -> Dict[str, Union[float, datetime, int]]:
        """Return a tuple containing some key data about `point`."""
        
        data = {
            'latitude': point.latitude,
            'longitude': point.longitude,
            'elevation': point.elevation,
            'time': point.time
        }
    
        # Parse extensions for heart rate and cadence data, if available
        try:
            elem = point.extensions[0]  # Assuming we know there is only one extension
            try:
                data['heart_rate'] = int(elem.find('garmin_tpe:hr', NAMESPACES).text)
            except AttributeError:
                # "text" attribute not found, so data not available
                pass
                
            try:
                data['cadence'] = int(elem.find('garmin_tpe:cad', NAMESPACES).text)
            except AttributeError:
                pass

        except IndexError:
            # "text" attribute not found, so data not available
            pass

        return data

def get_dataframe_from_gpx(fname: str) -> pd.DataFrame:
    """Takes the path to a GPX file (as a string) and returns a Pandas
    DataFrame.
    """
    with open(fname) as f:
        gpx = gpxpy.parse(f)
    segment = gpx.tracks[0].segments[0]  # Assuming we know that there is only one track and one segment
    data = [get_gpx_point_data(point) for point in segment.points]
    for idx in range(len(segment.points)):
        data[idx]['speed'] = float(segment.get_speed(idx))
    df = pd.DataFrame(data, columns=COLUMN_NAMES)
    df.heading = calculate_compass_heading(df.latitude.values,
                                           df.longitude.values)
    return df

if __name__ == '__main__':
    
    from sys import argv
    fname = argv[1]  # Path to GPX file to be given as first argument to script
    df = get_dataframe_from_gpx(fname)
    print(df)
    