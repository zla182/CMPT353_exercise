import math
import sys
from xml.dom.minidom import parse, parseString
import pandas as pd
from math import cos, asin, sqrt, pi
import numpy as np
from pykalman import KalmanFilter
def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')

# https://docs.python.org/3/library/xml.dom.minidom.html
def get_data(file):
    file_gpx = parse(file)
    lat_long = file_gpx.getElementsByTagName('trkpt')
    lat = []
    lon = []
    for item in lat_long:
        lat.append(item.getAttribute('lat'))
        lon.append(item.getAttribute('lon'))
    points = pd.DataFrame()
    points['lat'] = lat
    points['lon'] = lon
    points['lat'] = points['lat'].astype(float)
    points['lon'] = points['lon'].astype(float)
    return points


# https://newbedev.com/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def deg2rad(deg):
    return deg*(math.pi/180)
def haversinecalc(lat, lon, lat2, lon2):
    R = 6371
    dlat = np.deg2rad(lat2-lat)
    dlong = np.deg2rad(lon2-lon)
    a = np.sin((dlat)/2.0)**2 + np.cos(np.deg2rad(lat)) * np.cos(np.deg2rad(lat2)) * np.sin((dlong)/2.0)**2
    return R * np.arcsin(np.sqrt(a)) * 2 * 1000

def distance(points):
    data = points.copy()
    data['lat2'] = data['lat'].shift(periods = 1)
    data['lon2'] = data['lon'].shift(periods = 1)
    data['dist'] = data.apply(lambda x: haversinecalc(x['lat'], x['lon'], x['lat2'], x['lon2']), axis = 1)
    return data['dist'].sum()

def smooth(points):
    initial_value_guess = points.iloc[0]
    observation_covariance = np.diag([0.85, 0.85]) ** 2
    transition_covariance = np.diag([0.5, 0.5]) ** 2
    transition_matrix = [[1, 0], [0, 1]]
    kf = KalmanFilter(initial_state_mean=initial_value_guess,
                initial_state_covariance=observation_covariance,
                observation_covariance=observation_covariance,
                transition_covariance=transition_covariance,
                transition_matrices=transition_matrix)
    kalman_smoothed, _ = kf.smooth(points)
    result = pd.DataFrame(kalman_smoothed,columns=['lat','lon'])
    return result


def main():
    points = get_data(sys.argv[1])
    print('Unfiltered distance: %0.2f' % (distance(points),))
    
    smoothed_points = smooth(points)
    print('Filtered distance: %0.2f' % (distance(smoothed_points),))
    output_gpx(smoothed_points, 'out.gpx')
if __name__ == '__main__':
    main()