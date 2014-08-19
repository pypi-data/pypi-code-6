import math
import re
import pyproj

'''
Methods for representing geographic coordinates (latitude and longitude)
Features:
    Convert lat/lon strings from any format into a LatLon object
    Automatically store decimal degrees, decimal minutes, and degree, minute, second
      information in a LatLon object
    Output lat/lon information into a formatted string
    Project lat/lon coordinates into some other proj projection
    Calculate distances between lat/lon pairs using either the FAI or WGS84 approximation
Written July 22, 2014
Author: Gen Del Raye
'''

class GeoCoord:
    '''
    Object representing geographic coordinates (i.e. latitude or longitude)
    '''
    def __init__(self, degree = 0, minute = 0, second = 0):
        '''
        Initialize a GeoCoord object
        Inputs:
            degree (scalar) - integer or decimal degrees. If decimal degrees are given (e.g. 5.83),
              the fractional values (0.83) will be added to the minute and second variables.
            minute (scalar) - integer or decimal minutes. If decimal minutes are given (e.g. 49.17),
              the fractional values (0.17) will be added to the second variable.
            second (scalar) - decimal minutes.
        '''
        self.degree = degree
        self.minute = minute
        self.second = second
        self._update() # Clean up each variable and make them consistent
        
    def set_minute(self, minute):
        self.minute = float(minute)
        
    def set_second(self, second):
        self.second = float(second)
    
    def set_degree(self, degree):
        self.degree = float(degree)
            
    def _update(self):
        '''
        Given degree, minute, and second information, clean up the variables and make them
        consistent (for example, if minutes > 60, add extra to degrees, or if degrees is
        a decimal, add extra to minutes).
        '''
        self.decimal_degree = self.degree + self.minute/60. + self.second/3600.
        sign = cmp(self.decimal_degree, 0) # Store whether the coordinate is negative or positive
        decimal_degree = abs(self.decimal_degree)
        self.degree = decimal_degree//1 # Truncate degree to be an integer
        self.decimal_minute = (decimal_degree - self.degree)*60. # Calculate the decimal minutes
        self.minute = self.decimal_minute//1 # Truncate minute to be an integer
        self.second = (self.decimal_minute - self.minute)*60. # Calculate the decimal seconds
        # Finally, re-impose the appropriate sign
        self.degree = self.degree*sign
        self.minute = self.minute*sign
        self.second = self.second*sign
    
    def get_hemisphere(self):
        '''
        Dummy method, used in child classes such as Latitude and Longitude
        '''
        pass
    
    def set_hemisphere(self):
        '''
        Dummy method, used in child classes such as Latitude and Longitude
        '''
        pass
    
    def to_string(self, format_str):
        '''
        Output lat, lon coordinates as string in chosen format
        Inputs:
            format (str) - A string of the form A%B%C where A, B and C are identifiers.
              Unknown identifiers (e.g. ' ', ', ' or '_' will be inserted as separators 
              in a position corresponding to the position in format.
        Examples:
            >> palmyra = LatLon(5.8833, -162.0833)
            >> palmyra.to_string('D') # Degree decimal output
            ('5.8833', '-162.0833')
            >> palmyra.to_string('H% %D')
            ('N 5.8833', 'W 162.0833')
            >> palmyra.to_string('d%_%M')
            ('5_52.998', '-162_4.998')
        '''
        format2value = {'H': self.get_hemisphere(),
                        'M': abs(self.decimal_minute),
                        'm': int(abs(self.minute)),
                        'd': int(self.degree),
                        'D': self.decimal_degree,
                        'S': abs(self.second)}
        format_elements = format_str.split('%')
        coord_list = [str(format2value.get(element, element)) for element in format_elements]
        coord_str = ''.join(coord_list)
        if 'H' in format_elements: # No negative values when hemispheres are indicated
            coord_str = coord_str.replace('-', '')
        return coord_str
    
    def __cmp__(self, other):
        return cmp(self.decimal_degree, other.decimal_degree)
    
    def __neg__(self):
        self.degree = -self.degree
        self.minute = -self.minute
        self.second = -self.second
        self._update()
    
    def __pos__(self):
        self.degree = abs(self.degree)
        self.minute = abs(self.minute)
        self.second = abs(self.second)
        self._update()
        
    def __abs__(self):
        self.__pos__()
    
    def __floor__(self):
        self.minute = 0
        self.second = 0
        self._update()
    
    def __round__(self):
        if self.second >= 30:
            self.minute += 1
            self.second = 0
        if self.minute >= 30: 
            self.degree += 1
            self.minute = 0
        self._update()
        
    def __ceil__(self):
        if self.second > 0:
            self.second = 0
            self.minute += 1
        if self.minute > 0:
            self.minute = 0
            self.degree += 1
        self._update()
        
    def __int__(self):
        return self.degree
    
    def __float__(self):
        return self.decimal_degree
    
    def __str__(self):
        return str(self.decimal_degree)

class Latitude(GeoCoord):
    '''
    Coordinate object specific for latitude coordinates
    '''
    def get_hemisphere(self):
        '''
        Returns the hemisphere identifier for the current coordinate
        '''
        if self.decimal_degree < 0: return 'S'
        else: return 'N'
        
    def set_hemisphere(self, hemi_str):
        '''
        Given a hemisphere identifier, set the sign of the coordinate to match that hemisphere
        '''
        if hemi_str == 'S':
            self.degree = abs(self.degree)*-1
            self.minute = abs(self.minute)*-1
            self.second = abs(self.second)*-1
            self._update()
        elif hemi_str == 'N':
            self.degree = abs(self.degree)
            self.minute = abs(self.minute)
            self.second = abs(self.second)
            self._update()
        else:
            raise ValueError('Hemisphere identifier for latitudes must be N or S')

class Longitude(GeoCoord):
    '''
    Coordinate object specific for longitude coordinates
    '''
    def get_hemisphere(self):
        '''
        Returns the hemisphere identifier for the current coordinate
        '''
        if self.decimal_degree < 0: return 'W'
        else: return 'E'

    def set_hemisphere(self, hemi_str):
        '''
        Given a hemisphere identifier, set the sign of the coordinate to match that hemisphere
        '''
        if hemi_str == 'W':
            self.degree = abs(self.degree)*-1
            self.minute = abs(self.minute)*-1
            self.second = abs(self.second)*-1
            self._update()
        elif hemi_str == 'E':
            self.degree = abs(self.degree)
            self.minute = abs(self.minute)
            self.second = abs(self.second)
            self._update()
        else:
            raise(ValueError, 'Hemisphere identifier for longitudes must be E or W')

def string2geocoord(coord_str, coord_class, format_str = 'D'):
    '''
    Create a GeoCoord object (e.g. Latitude or Longitude) from a string.
    Inputs:
        coord_str (str) - a string representation of a geographic coordinate (e.g. '5.083 N'). Each 
          section of the string must be separated by some kind of a separator character ('5.083N' is
          invalid).
        coord_class (class) - a class inheriting from GeoCoord that includes a set_hemisphere method.
          Can be either Latitude or Longitude
        format_str (str) - a string representation of the sections of coord_str. Possible letter values 
        correspond to the keys of the dictionary format2value, where
              'H' is a hemisphere identifier (e.g. N, S, E or W)
              'D' is a coordinate in decimal degrees notation
              'd' is a coordinate in degrees notation
              'M' is a coordinate in decimal minutes notaion
              'm' is a coordinate in minutes notation
              'S' is a coordinate in seconds notation
              Any other characters (e.g. ' ' or ', ') will be treated as a separator between the above components.
          All components should be separated by the '%' character. For example, if the coord_str is 
          '5, 52, 59.88_N', the format_str would be 'd%, %m%, %S%_%H'
    Returns:
        GeoCoord object initialized with the coordinate information from coord_str
    '''
    new_coord = coord_class()
    # Dictionary of functions for setting variables in the coordinate class:
    format2value = {'H': new_coord.set_hemisphere,
                    'M': new_coord.set_minute,
                    'm': new_coord.set_minute,
                    'd': new_coord.set_degree,
                    'D': new_coord.set_degree,
                    'S': new_coord.set_second}
    if format_str[0] == 'H':
        ''' Having the hemisphere identifier at the beginning is problematic for ensuring that
        the final coordinate value will be negative. Instead, change the identifier and the
        format string so that the hemisphere is identified at the end:'''
        new_coord_start = re.search('\d', coord_str).start() # Find the beginning of the coordinate
        new_format_start = re.search('[a-gi-zA-GI-Z]', format_str).start() # Find the first non-hemisphere identifier
        format_str = '% %'.join((format_str[new_format_start:], format_str[0])) # Move hemisphere identifier to the back
        coord_str = ' '.join((coord_str[new_coord_start:], coord_str[0])) # Move hemisphere identifier to the back
    format_elements = format_str.split('%')
    separators = [sep for sep in format_elements if sep not in format2value.keys()] # E.g. ' ', '_' or ', ' characters
    separators.append('%') # Dummy separator for the final part of the coord_str
    formatters = [form for form in format_elements if form in format2value.keys()] # E.g. 'D', 'm', or 'S' characters
    for form, sep in zip(formatters, separators):
        coord_elements = coord_str.split(sep)
        format2value[form](coord_elements[0]) # Set the coordinate variable (e.g. 'self.degree' with the coordinate substring (e.g. '5')
        coord_str = sep.join(coord_elements[1:]) # Get rid of parts of the substring that have already been done
    new_coord._update() # Change all of the variables in the coordinate class so they are consistent with each other
    return new_coord

class LatLon:
    '''
    Object representing lat/lon pairs
    '''
    def __init__(self, lat, lon, name = None):
        '''
        Input:
            lat (class instance) - an instance of class Latitude. Can be specified directly in
              the __init__ call for example by calling LatLon(Latitude(5.8), Longitude(162.5))
            lon (class instance) - an instance of class Longitude
            name (str) - an identifier
        '''
        self.lat = lat
        self.lon = lon
        self.name = name
    
    def project(self, projection):
        '''
        Return coordinates transformed to a given projection
        Projection should be a basemap or pyproj projection object or similar
        '''
        x, y = projection(self.lon.decimal_degree, self.lat.decimal_degree)
        return (y, x)
    
    def complex(self):
        '''
        Return lat/lon pairs as complex coordinates
        '''
        return self.lat.decimal_degree + 1j * self.lon.decimal_degree
    
    def __add__(self, other):
        self.lat += other.lat
        self.lon += other.lon
    
    def __sub__(self, other):
        self.lat -= other.lat
        self.lon -= other.lon
        
    def distance(self, other, ellipse = 'WGS84'):
        '''
        Returns great circle distance between two lat/lon coordinates in km
        using the WGS84 ellipsoid
        '''
        lat1, lon1 = self.lat.decimal_degree, self.lon.decimal_degree
        lat2, lon2 = other.lat.decimal_degree, other.lon.decimal_degree
        g = pyproj.Geod(ellps = ellipse)
        return g.inv(lon1, lat1, lon2, lat2)[2]/1000.0
        
    def distance_sphere(self, other, radius = 6371.0):
        '''
        Returns great circle distance between two lat/lon coordinates on a sphere
        using the Haversine formula. The default radius corresponds to the FAI sphere
        with units in km.
        '''
        lat1, lon1 = self.lat.decimal_degree, self.lon.decimal_degree
        lat2, lon2 = other.lat.decimal_degree, other.lon.decimal_degree
        pi = math.pi/180.
        # phi is 90 - latitude
        phi1 = (90. - lat1)*pi
        phi2 = (90. - lat2)*pi
        # theta is longitude
        theta1 = lon1*pi
        theta2 = lon2 *pi
        cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
               math.cos(phi1)*math.cos(phi2))
        arc = math.acos(cos)
        return arc*radius
    
    def to_string(self, formatter = 'D'):
        '''
        Return string representation of lat and lon as a 2-element tuple
        using the format specified by formatter
        '''
        return (self.lat.to_string(formatter), self.lon.to_string(formatter))

def string2latlon(lat_str, lon_str, format_str):
    '''
    Create a LatLon object from a pair of strings.
    Inputs:
        lat_str (str) - string representation of a latitude (e.g. '5 52 59.88 N')
        lon_str (str) - string representation of a longitude (e.g. '162 4 59.88 W')
        format_str (str) - format in which the coordinate strings are given (e.g. 
          for the above examples this would be 'd% %m% %S% %H'). See function 
          string2geocoord for a detailed explanation on how to specify formats.
    Returns:
        A LatLon object initialized with coordinate data from lat_str and lon_str
    '''
    lat = string2geocoord(lat_str, Latitude, format_str)
    lon = string2geocoord(lon_str, Longitude, format_str)
    new_latlon = LatLon(lat = lat, lon = lon)
    return new_latlon

def test():
    palmyra = LatLon(Latitude(5.8833), Longitude(-162.0833)) # Simplest case - initialize from decimal degrees
    print palmyra.to_string('d% %m% %S% %H') # Print coordinates to degree minute second (returns ('5 52 59.88 N', '162 4 59.88 W'))
    palmyra = string2latlon('5 52 59.88 N', '162 4 59.88 W', 'd% %m% %S% %H') # Initialize from more complex string
    print palmyra.to_string('d%_%M') # Print coordinates as degree minutes separated by underscore (returns ('5_52.998', '-162_4.998'))
    palmyra = string2latlon('N 5, 52.998', 'W 162, 4.998', 'H% %d%, %M') # An alternative complex string
    print palmyra.to_string('D') # Print coordinate to decimal degrees (returns ('5.8833', '-162.0833'))
    honolulu = LatLon(Latitude(21.3), Longitude(-157.8167))
    print palmyra.distance(honolulu) # WGS84 distance is 1766.69130376 km
    print palmyra.distance_sphere(honolulu) # FAI distance is 1774.77188181 km

if __name__ == '__main__':
    test()
        