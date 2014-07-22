import numpy
import shapely.geometry
import shapely.ops
import warnings
import rdp

'''
Methods for working with path and style data from svg files
'''

class nullpoly():
    '''
    An 'null' polygon type
    '''
    def __init__(self, emptyvalue = numpy.nan, *args, **kwargs):
        self.emptyvalue = emptyvalue
        self.bounds = (emptyvalue, emptyvalue, emptyvalue, emptyvalue)
        self.length = emptyvalue
    def area(self):
        return self.emptyvalue
    def overlaps(self, other):
        return False
    def coords(self):
        return None

class Polygon:
    def __init__(self, coords, null_polygon = nullpoly):
        '''
        Create the polygon object as a shapely polygon
        If not a valid polygon (e.g. is a line rather than a closed loop)
        ignore it by replacing with a 'null' polygon.
        '''
        try:
            self.poly = shapely.geometry.Polygon(coords)
            if not self.poly.is_valid:
                # Ensure that polygons with invalid geometries (e.g. inner ring
                # contacting outer ring along more than one point) won't crash
                # the code.
                warnings.warn('Detected invalid polygon, setting to null')
                self.poly = null_polygon()
        except ValueError, e:
            # Ensures that paths that are lines instead of closed shapes
            # (i.e. invalid polygons) won't crash the code.
            warnings.warn('Detected Shapely Error: %s, setting to null' %(e.message))
            self.poly = nullpoly()
            
    def bbox(self):
        '''
        Return coordinate tuple (minx, miny, maxx, maxy)
        describing the bounding box of the polygon
        '''
        return self.poly.bounds
    
    def bbox_area(self):
        '''
        Return the area of the bounding box of the polygon
        '''
        minx, miny, maxx, maxy = self.bbox()
        return (maxx - minx)*(maxy - miny)
    
    def area(self):
        '''
        Return the area of the polygon
        '''
        return self.poly.area
    
    def circumference(self):
        '''
        Return the circumference of the polygon
        '''
        return self.poly.length
    
    def overlaps(self, other):
        '''
        Return whether the interior of a polygon intersects with the interior of another
        See discussion on object.touches() in the Shapely User Manual 
        (http://toblerity.org/shapely/manual.html) for more details.
        '''
        return self.poly.intersects(other.poly) and not self.poly.touches(other.poly)
#         return self.poly.overlaps(other.poly)
    
    def union(self, other):
        '''
        Return intersection between polygon and other
        '''
        self.poly = self.poly.union(other.poly)
        
    def cascading_union(self, other_list):
        poly_list = [o.poly for o in other_list]
        poly_list.append(self.poly)
        self.poly = shapely.ops.cascaded_union(poly_list)
        
    def coords(self):
        try:
            return list(self.poly.exterior.coords)
        except AttributeError, e:
            # In case poly has become a MultiPolygon
            if type(self.poly).__name__ == 'MultiPolygon':
                warnings.warn('%s: Returning coordinates of only 1 polygon in a MultiPolygon object' %(e.message))
                return list(self.poly[0].exterior.coords)
        
    def buffer(self, distance):
        self.poly = self.poly.buffer(distance)
    
    def hull(self, other_list):
        poly_coords = self.coords()
        for o in other_list:
            poly_coords.extend(o.coords())
        all_points = shapely.geometry.MultiPoint(poly_coords)
        self.poly = all_points.convex_hull
        
    def rdp(self, epsilon = 0.5, preserve_topology = False):
        '''
        Simplify using Ramer Douglas Peucker algorithm
        The rdp package is used instead of shapely's built in 'simplify' method because Shapely seems
        to be strongly biased toward turning polygons into points
        '''
#         simple_poly = self.poly.simplify(tolerance = epsilon, preserve_topology = preserve_topology)
#         if simple_poly.is_empty:
#             # If the simplification deletes the polygon, treat the polygon as a point
#             return (self.coords()[0])
#         return self.coords()
        return rdp.rdp(self.coords(), epsilon = epsilon)

def complex2coord(complexnum):
    '''
    Turn complex coordinates into coordinate tuple where 
    x coordinate is num.real and y coordinate is num.imag
    e.g. complex2coord((300 + 500j,)) returns (300, 500) 
    '''
    return (complexnum.real, complexnum.imag)

def linearize_line(segment, n_interpolate = None):
    '''
    Turn svg line into set of coordinates by returning
    start and end coordinates of the line segment.
    n_interpolate is only used for consistency of use
    with linearize_curve()
    '''
    return numpy.array([segment.start, segment.end])

def linearize_curve(segment, n_interpolate = 10):
    '''
    Estimate svg curve (e.g. Bezier, Arc, etc.) using
    a set of n discrete lines. n_interpolate sets the
    number of discrete lines per curve.
    '''
    interpolation_pts = numpy.linspace(0, 1, n_interpolate, endpoint = False)[1:]
    interpolated = numpy.zeros(n_interpolate + 1, dtype = complex)
    interpolated[0] = segment.start
    interpolated[-1] = segment.end
    for i, pt in enumerate(interpolation_pts):
        interpolated[i + 1] = segment.point(pt)
    return interpolated

segmenttype2func = {'CubicBezier': linearize_curve,
                    'Line': linearize_line,
                    'QuadraticBezier': linearize_curve,
                    'Arc': linearize_curve}

def linearize(path, n_interpolate = 10):
    '''
    More sophisticated linearization option
    compared to endpts2line().
    Turn svg path into discrete coordinates
    with number of coordinates per curve set
    by n_interpolate. i.e. if n_interpolate
    is 100, each curve is approximated by
    100 discrete lines.
    '''
    segments = path._segments
    complex_coords = list()
    for segment in segments:
        # Output coordinates for each segment, minus last point (because
        # point is same as first point of next segment)
        segment_type = type(segment).__name__
        segment_linearize = segmenttype2func[segment_type]
        linearized = segment_linearize(segment, n_interpolate)
        complex_coords.extend(linearized[:-1])
    # Append last point of final segment to close the polygon
    complex_coords.append(linearized[-1])
    return [complex2coord(complexnum) for complexnum in complex_coords] # Output list of (x, y) tuples

def endpts2line(path):
    '''
    Simplist linearization routine. Simply
    outputs start and end points of each 
    segment as a coordinate array.
    '''
    segments = path._segments
    coords = [complex2coord(segment.start) for segment in segments]
    coords.append(complex2coord(segment.end))
    return coords

def poly2svgstring(coord_array):
    '''
    Turn any array of coordinates (shape n_coords x 2) into an svg string
    e.g. poly2svgstring(numpy.array([(1,1), (2,2), (2,1), (1,1)])) returns
    'M 1,1 2,2 2,1 1,1 z'
    Only handles polygons (i.e. no curves, arcs, or beziers, only moveto)
    '''
    svgstring = [','.join(c) for c in numpy.array(coord_array, dtype = str)]
    svgstring.insert(0, 'M')
    svgstring.append('z')
    return ' '.join(svgstring)

def parse_style(stylestr):
    '''
    Parse style attribute string of svg into a dictionary
    e.g. if stylestr = 'fill:#a28f65;fill-opacity:1', returns
    {'fill': '#a28f65', 'fill-opacity': '1'}
    '''
    stylestr = stylestr.split(';') # Split by entry
    styledict = dict([(s.split(':')[0], s.split(':')[-1]) for s in stylestr])
    return styledict