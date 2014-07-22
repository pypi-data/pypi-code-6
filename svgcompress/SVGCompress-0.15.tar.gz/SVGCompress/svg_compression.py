import vector_utils
import numpy
import svg.path
import xml.etree.ElementTree as ET
import os
import copy
import warnings

'''
Compress svg figure through a variety of methods
'''

class Compress:
    def __init__(self, svg_file):
        self.filename, self.extension = svg_file.split('.') # Get filename and extension
        assert self.extension == 'svg', 'File must be an svg'
        self.figure_data = ET.parse(svg_file) # Parse svg data as xml
        self.root = self.figure_data.getroot() # Root object in svg
        self.reportString = '----------- REPORT -----------' # String used to generate reports
        self.initial_kb = self._get_kb(svg_file) # Get the uncompressed file size in KBytes
    
    def find_paths(self):
        '''
        Find and parse nodes in the xml that correspond to paths in the svg
        '''
        tag_prefix = self._get_tag_prefix()
        self.path_nodes = self.root.findall('.//%spath' %(tag_prefix))
        self.path_parents = self.root.findall('.//%spath/..' %(tag_prefix))
        self.paths = list()
#         for p in self.path_nodes:
#             try:
#                 self.paths.append(svg.path.parse_path(p.attrib['d']))
#             except KeyError, e:
#                 # Items such as clipping paths have no coordinates
#                 warnings.warn('Detected path with no coordinates: e.message')
#                 pass
        self.paths = [svg.path.parse_path(p.attrib.get('d', 'M 0,0 z')) for p in self.path_nodes]
        
    def linearize_paths(self, curve_fidelity = 10):
        '''
        Turn svg paths into discrete lines
        Inputs:
            curve_fidelity(int) - number of lines with which to approximate curves
                in svg. Higher values necessitates longer computation time.
        '''
        self.linear_coords = [vector_utils.linearize(p, curve_fidelity) for p in self.paths]
        
    def compress_by_deletion(self, criteria, threshold, search_within = None):
        '''
        Remove paths from svg that fail the given criteria
        '''
        deletion_index = self.search_polygons(criteria, threshold, search_within)
        self._delete_paths(deletion_index)
        # Add record of what happened to reportString
        n_total = len(self.path_nodes)
        n_deleted = len(deletion_index)
        self._append_report('Deleted %s polygons out of %s' %(n_deleted, n_total))
        
    def search_polygons(self, criteria, threshold, search_within = None):
        '''
        Find indices of polygons that fail given criteria
        Inputs:
            search_within(ndarray) - array of indices within which to search
        '''
        polygons = self._coord2polygon(self.linear_coords)
        criteria2func = {'bboxarea': self._select_by_bboxarea,
                         'circumference': self._select_by_circumference}
        results_index = criteria2func[criteria](polygons, threshold)
        if search_within is not None:
            results_index = self._get_searchintersect(results_index, search_within)
        n_results = len(results_index)
        self._append_report('Found %d polygons with %s less than %s' %(n_results, criteria, threshold))
        return results_index
    
    def _get_searchintersect(self, indices_1, indices_2):
        '''
        Return indices from indices_1 that are contained in indices_2
        '''
        return numpy.intersect1d(indices_1, indices_2, assume_unique = True)
    
    def _select_by_bboxarea(self, polygons, threshold = 500):
        '''
        Return indices of polygons that are smaller than a threshold bounding box area
        '''
        bbox_areas = numpy.array([p.bbox_area() for p in polygons])
        # OPTIONAL LINE: gets rid of annoying warning
        bbox_areas[numpy.isnan(bbox_areas)] = 2*threshold # Just to make sure nans<threshold evaluates to False
        return numpy.where(bbox_areas < threshold)[0]
    
    def _select_by_circumference(self, polygons, threshold = 100):
        '''
        Return indices of polygons that are smaller than a threshold circumference
        '''
        circumferences = numpy.array([p.circumference() for p in polygons])
        # OPTIONAL LINE: gets rid of annoying warning
        circumferences[numpy.isnan(circumferences)] = 2*threshold # Just to make sure nans<threshold evaluates to False
        return numpy.where(circumferences < threshold)[0]
    
    def _delete_paths(self, deletion_index):
        '''
        Delete paths in svg corresponding to deletion_index
        '''
        for parent in self.path_parents:
            for index in deletion_index:
                try:
                    parent.remove(self.path_nodes[index])
                except ValueError:
                    pass
    
    def _coord2polygon(self, coords):
        '''
        Convert a list or array of coordinates into a polygon object
        '''
        return [vector_utils.Polygon(coord) for coord in coords]
    
    def compress_by_simplification(self, epsilon = 0.5, search_within = None):
        '''
        Simplify polygons in the svg using the Ramer-Douglas-Peucker algorithm
        Inputs:
            search_within(ndarray) - indices of paths to simplify
        '''
        replace_coords = numpy.array(self.linear_coords)
        replacement_index = numpy.arange(len(self.path_nodes))
        if search_within is not None:
            replace_coords = replace_coords[search_within]
            replacement_index = search_within
        polygons = self._coord2polygon(replace_coords)
        simple_paths = [polygon.rdp(epsilon) for polygon in polygons]
        simple_svgstr = [vector_utils.poly2svgstring(sp) for sp in simple_paths]
        self._replace_paths(replacement_index, simple_svgstr)
    
    def overlap_list(self, poly, polyarray, search_index):
        '''
        Return list of polygons in an array that intersect with poly
        '''
        overlapList = list()
        indexList = list()
        for a, i in zip(polyarray, search_index):
            if a.overlaps(poly):
                overlapList.append(a)
                indexList.append(i)
        return overlapList, indexList
    
    def recursive_intersect(self, poly, pArray, intersectList = [], intersectIndex = [], search_index = [], 
                            nterminate = numpy.Inf, bufferDistance = None):
        if bufferDistance is not None:
            poly.buffer(bufferDistance)
        childeren, childeren_index = self.overlap_list(poly, pArray, search_index)
        for child, index in zip(childeren, childeren_index):
            try: # Child may already have been removed from another node
                pArray.remove(child)
                search_index.remove(index)
                intersectList.append(child)
                intersectIndex.append(index)
                intersectList, pArray = self.recursive_intersect(child, pArray, intersectList, intersectIndex, 
                                                                 search_index, bufferDistance)
            except:
                pass
            if len(intersectList) > nterminate: break # Optional limit to computational complexity
        return (intersectList, pArray, intersectIndex, search_index)
    
    def _merge(self, polygon, intersect):
        '''
        Append polygon by cascading union
        '''
        polygon.cascading_union(intersect[1:])
        
    def _hull(self, polygon, intersect):
        '''
        Append polygon by convex hull
        '''
        polygon.hull(intersect[1:])
    
    def compress_by_merging(self, search_within = None, epsilon = 1, nterminate = numpy.Inf, group_by_color = True, bufferDistance = None,
                            operation_key = 'merge'):
        get_operation = {'merge': self._merge,
                         'hull': self._hull}
        operation = get_operation[operation_key]
        color_groupings = [range(len(self.path_nodes))]
        n_deleted = 0 # Reporting variable for number of polygons unified
        if group_by_color:
            nullstyle = 'fill:#zzzzzz;fill-opacity:-1' # Some paths (e.g. clipping paths) don't have styles
            styles = [vector_utils.parse_style(p.attrib.get('style', nullstyle)) for p in self.path_nodes]
            self.colors = numpy.array([style.get('fill', '#zzzzzz') for style in styles])
            color_str = numpy.unique(self.colors)
            color_groupings = [numpy.where(self.colors == c)[0] for c in color_str]
        for color in color_groupings:
            if search_within is None:
                search_within = numpy.arange(len(self.path_nodes))
            search_space = numpy.intersect1d(search_within, color, assume_unique = True)
            search_coords = numpy.array(self.linear_coords)[search_space]
            search_index = list(search_space)
            polygons = self._coord2polygon(search_coords)
            while len(polygons)>0:
                p1 = polygons.pop()
                p1_copy = copy.deepcopy(p1)
                p_index = search_index.pop()
                intersect, remainder, intersect_index, remainder_index = self.recursive_intersect(p1_copy, polygons, list([p1_copy]), 
                                                                                                  list([p_index]), search_index, 
                                                                                                  nterminate = nterminate,
                                                                                                  bufferDistance = bufferDistance)
                for d_index in intersect_index[1:]:
                    self._delete_paths((d_index,))
                    n_deleted += 1 # Account for things that p1 intersects with
                polygons = remainder
                search_index = remainder_index
                operation(p1, intersect)
                n_deleted += len(intersect) > 1 # Account for p1 if it intersected with anything
                simple_path = numpy.array(p1.rdp(epsilon = epsilon))
                poly1_svgstr = vector_utils.poly2svgstring(simple_path)
                self._replace_paths((p_index,), (poly1_svgstr,))
        self._append_report('Merged %s out of %s polygons' %(n_deleted, len(search_within)))
        
        
    def _replace_paths(self, replacement_index, replacement_str):
        for index, path in zip(replacement_index, replacement_str):
#             self.path_nodes[index].set('d', 'M 50,50 50,100 100,100 100,50 50,50 z') # debug
            self.path_nodes[index].set('d', path)
            
    def write(self, outputfile = None):
        '''
        Write compressed svg to file
        Inputs:
            outputfile - filename to write to (e.g. 'output.svg'). If not given,
                will write to 'originalfilename_compressed.svg'
        '''
        if outputfile == None:
            outputfile = '%s_compressed.svg' %(self.filename)
        self.figure_data.write(outputfile)
        final_kb = self._get_kb(outputfile) # Get the compressed size in KBytes
        self._append_report('Compressed %sKB to %sKB' %(self.initial_kb, final_kb))
        self._append_report('Saved to %s' %(outputfile))
    
    def report(self):
        '''
        Print a report of how well the compression worked
        '''
        print self.reportString

    def _append_report(self, new_text):
        self.reportString = '\n'.join((self.reportString, new_text))
    
    def _get_tag_prefix(self):
        '''
        Return the string that prefixes all tags, 
        e.g. if the root tag is '{http://www.w3.org/2000/svg}svg', all other tags 
        in the xml are probably prefixed by '{http://www.w3.org/2000/svg}'
        '''
        prefix_endindex = self.root.tag.rindex('}')
        return self.root.tag[:(prefix_endindex + 1)]
    
    def _get_kb(self, filename):
        return os.path.getsize(filename)/1000.0

def compress_by_method(filename, compression_type, curve_fidelity = 10, outputfile = None,
                       pre_select = False, selection_tuple = ('', ''), **kwargs):
    '''
    Convenience method for one-pass compression
    See compress_by_merging, compress_by_deletion, and compress_by_simplification in Compress
    for kwargs.
    '''
    def compression_options(compress_instance, option_key, **kwargs):
        compression_options = {'merge': compress_instance.compress_by_merging,
                               'delete': compress_instance.compress_by_deletion,
                               'simplify': compress_instance.compress_by_simplification}
        compression_options[option_key](**kwargs)

    test_compression = Compress(filename)
    test_compression.find_paths()
    test_compression.linearize_paths(curve_fidelity = curve_fidelity)
    pre_selection = None
    if pre_select:
        criteria, threshold = selection_tuple
        pre_selection = test_compression.search_polygons(criteria, threshold)
    compression_options(test_compression, compression_type, search_within = pre_selection, **kwargs)
    test_compression.write(outputfile = outputfile)
    test_compression.report()

def test(filename, thresholds = (5, 2), epsilon = 0.5, curve_fidelity = 10, 
         criterias = ('bboxarea', 'circumference'), buffer_distance = 10):
    '''
    Demonstration routine for package 'compress'
    '''
    filestr, extension = filename.split('.')
    ## Compress by deletion:
    for criteria, threshold in zip(criterias, thresholds):
        outputfile = ''.join((filestr, '_truncby%s.' %(criteria), extension))
        compress_by_method(filename, 'delete',  curve_fidelity, outputfile, criteria = criteria,
                           threshold = threshold)

    ## Compress by simplification:
    outputfile = ''.join((filestr, '_simplified.', extension))
    compress_by_method(filename, 'simplify', curve_fidelity, outputfile, pre_select = True, 
                       selection_tuple = (criterias[0], thresholds[0]), epsilon = epsilon)

    ## Compress by unification:
    outputfile = ''.join((filestr, '_merged.', extension))
    compress_by_method(filename, 'merge', curve_fidelity, outputfile, pre_select = True, 
                       selection_tuple = (criterias[0], thresholds[0]), epsilon = epsilon,
                       group_by_color = False)

    ## Compress by convex hull:
    outputfile = ''.join((filestr, '_hull.', extension))
    compress_by_method(filename, 'merge', curve_fidelity, outputfile, pre_select = True, 
                       selection_tuple = (criterias[0], thresholds[0]), epsilon = epsilon, 
                       bufferDistance = buffer_distance, operation_key = 'hull', group_by_color = False)
    
    ## Lastly, see if uncompressed file is same as original:
    # TODO: Find out why wierdly, it never is.
    test_compression = Compress(filename)
    outputfile = ''.join((filestr, '_uncompressed.', extension))
    test_compression.write(outputfile = outputfile)
    test_compression.report()

if __name__ == '__main__':
    # Demonstrate all functions with pre-prepared test vector
    test(filename = 'test/test_vector.svg', thresholds = (300, 150), epsilon = 5, buffer_distance = 10)
    # Demonstrate all functions with sample map
    test(filename = 'test/map_test.svg', thresholds = (6, 3), epsilon = 30, buffer_distance = 20)
    # Demonstrate with a plot constructed in matplotlib
    test(filename = 'test/matplotlib_test.svg', thresholds = (1000, 100), epsilon = 2, buffer_distance = 200)
