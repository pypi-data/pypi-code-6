# coding=utf-8
import requests

__author__ = 'Rob Derksen <rob.derksen@hubsec.eu>'
__version__ = '0.1.1'


class PyMapia:
    def __init__(self, api_key):
        """

        :param api_key:
            API key of your WikiMapia application
        :type api_key: str
        """
        self._base_url = 'http://api.wikimapia.org/?key={0}&format=json'.format(api_key)

    def get_place_by_id(self, id_, language=None, data_blocks=None, options=None):
        """
        Returns information about place. Place information is organized in data-blocks:
            * main: main information about place: url, title, description, categories, if place is a building, if it's
              a region. Also if it is deleted.
            * geometry: place geometry on map: polygon or rectangle
            * edit: user_id and name of last editor and timestamp. If the place is in deletion state this info will be
              in the edit block also
            * location: place location: lat/lon coordinates, north/south/east/west coordinates, zoom level, country,
              state, city id and name, WikiMapia Cityguide domain name, street id and name
            * attached: places attached to selected one or parent place of selected one, only basic info: url, title,
              categories. Also if child place is deleted.
            * photos: photos of current place: urls to thumb, big and fullsize photo, id, size, author id and name,
              date of photo uploading, last editor of this photo, photo status (deleted/active)
            * comments: place comments: number, language of comment, author id, his ip and name, comment text,
              positive and negative votes, moderator id, name, and date of deletion if the comment was removed
            * translate: languages available for selected place
            * similar_places, nearest_places, nearest_comments, nearest_streets, nearest_hotels: extra information
              about objects around selected one

        :param id_:
            The identifier of the object you want to get information about.
        :type id_: int
        :param language:
            The specified language in ISO 639-1 format
        :type language: str
        :param data_blocks:
            A list of strings specifying which blocks of data you want to return: main, geometry, edit,
            location, attached, photos, comments, translate, similar_places, nearest_places,
            nearest_comments, nearest_streets, nearest_hotels
        :type data_blocks: list
        :param options:
            A list of options:
                * mercator - all coordinates will be in the Mercator format instead of the default format.
        :type options: list
        """
        url = self._base_url + '&function=place.getbyid&id=' + str(id_)
        if language and isinstance(language, str):
            url += '&language=' + language
        if data_blocks and isinstance(data_blocks, list):
            url += '&data_blocks=' + ','.join(data_blocks)
        if options and isinstance(options, list):
            url += '&options=' + ','.join(options)

        return requests.get(url).json()

    def get_place_by_area(self, bbox=None, tile_coordinates=None, language=None, data_blocks=None, options=None,
                          count=5, page=1, category=None, category_or=None):
        """
        Returns all places in the given boundary box optionally filtered by category parameter. Only basic information
        is available: id, title, url, location and polygon of each place. Location and polygon fields can be turned off
        with data-block parameter.

        :param bbox:
            Bounding box as dict with the following keys: lon_min, lon_max, lat_min, lat_max
        :type bbox: dict
        :param tile_coordinates:
            Tile coordinates as dict with the following keys: x, y, z
        :type tile_coordinates: dict
        :param language:
            The specified language in ISO 639-1 format
        :type language: str
        :param data_blocks:
            A list of strings specifying which blocks of data you want to return: main, geometry, edit, location,
            attached, photos, comments, translate, similar_places, nearest_places, nearest_comments, nearest_streets,
            nearest_hotels
        :type data_blocks: list
        :param options:
            A list of options:
                * mercator - all coordinates will be in the Mercator format instead of the default format.
        :type options: list
        :param count:
            This is a variable that determines the number of results per page. 5 is default (5 min, 100 max).
        :type count: int
        :param page:
            The page number. 1 is default.
        :type page: int
        :param category:
            The WikiMapia category code as a list with category ids or text queries in UTF-8: School, Church, etc.
            Several comma-separated categories may be stated with "AND" logic. It means that only objects which have all
            listed categories together would be returned. If you need OR logic use ``category_or`` parameter.
        :type category: list
        :param category_or:
            The WikiMapia category code as a list with category ids or text queries in UTF-8: School, Church, etc.
            Several comma-separated categories may be stated with "OR" logic. All objects which have any category from
            this list would be returned. At first all places with any of ``category_or`` categories are selected and
            then only those which have all ``category`` categories are left.
        :type category_or: list
        """
        if not bbox and not tile_coordinates:
            raise AttributeError('You need to specify a bounding box or tile coordinates')
        if bbox and tile_coordinates:
            raise AttributeError('You need to choose between a bounding box and tile coordinates')
        if count < 5:
            count = 5
        if count > 100:
            count = 100

        url = self._base_url + '&function=place.getbyarea'

        if bbox:
            if not (bbox.get('lon_min') and bbox.get('lon_max') and bbox.get('lat_min') and bbox.get('lat_max')):
                raise AttributeError('Bounding box must be a dict with the keys lon_min, lon_max, lat_min and lat_max')
            url += '&bbox={0[lon_min]},{0[lat_min]},{0[lon_max]},{0[lat_max]}'.format(bbox)
        else:
            if not (tile_coordinates.get('x') and tile_coordinates.get('y') and tile_coordinates.get('z')):
                raise AttributeError('Tile coordinates must be a dict with the keys x, y, and z')
            url += '&x={0[x]}&y={0[y]}&z={0[z]}'.format(tile_coordinates)

        if language and isinstance(language, str):
            url += '&language=' + language
        if data_blocks and isinstance(data_blocks, list):
            url += '&data_blocks=' + ','.join(data_blocks)
        if options and isinstance(options, list):
            url += '&options=' + ','.join(options)
        if count != 5:
            url += '&count=' + str(count)
        if page != 1:
            url += '&page=' + str(page)
        if category and isinstance(category, list):
            url += '&category=' + ','.join(category)
        if category_or and isinstance(category_or, list):
            url += '&category_or' + ','.join(category_or)

        return requests.get(url).json()

    def get_nearest_place(self, lat, lon, language=None, data_blocks=None, options=None, page=1, count=5,
                          category=None):
        """
        Returns search results of objects, closest to the selected point. Optionally filtered by category parameter.
        Only basic information is available: id, title, url, location and polygon of each place and distance from
        selected coordinates to it. Location and polygon fields can be turned off with data-block parameter.

        :param lat:
            Coordinates of the "search point" as a float; lat means latitude (φ).
        :type lat: float
        :param lon:
            Coordinates of the "search point" as a float; lon means longitude (λ).
        :type lon: float
        :param language:
            The specified language in ISO 639-1 format
        :type language: str
        :param data_blocks:
            A list of strings specifying which blocks of data you want to return: main, geometry, edit, location,
            attached, photos, comments, translate, similar_places, nearest_places, nearest_comments, nearest_streets,
            nearest_hotels
        :type data_blocks: list
        :param options:
            A list of options:
                * mercator - all coordinates will be in the Mercator format instead of the default format.
        :type options: list
        :param page:
            The page number. 1 is default.
        :type page: int
        :param count:
            This is a variable that determines the number of results per page. 5 is default (5 min, 100 max).
        :type count: int
        :param category:
            The WikiMapia category code as a list with category ids or text queries in UTF-8: School, Church, etc.
            Several categories may be stated with "AND" logic. It means that only objects which have all listed
            categories together would be returned.
        :type category: list
        """
        url = self._base_url + '&function=place.getnearest&lat={0}&lon={1}'.format(lat, lon)

        if language and isinstance(language, str):
            url += '&language=' + language
        if data_blocks and isinstance(data_blocks, list):
            url += '&data_blocks=' + ','.join(data_blocks)
        if options and isinstance(options, list):
            url += '&options=' + ','.join(options)
        if count != 5:
            url += '&count=' + str(count)
        if page != 1:
            url += '&page=' + str(page)
        if category and isinstance(category, list):
            url += '&category=' + ','.join(category)

        return requests.get(url).json()

    def search_place(self, query, lat, lon, language=None, data_blocks=None, options=None, page=1, count=5,
                     category=None, category_or=None, distance=None):
        """
        Returns search results of a given query, optionally filtered by category. Only basic information is available:
        id, title, url, location and polygon of each place and distance from selected coordinates to it. The function
        is very close to ``get_nearest_place``.

        :param query:
            The query to search in WikiMapia (UTF-8).
        :type query: str
        :param lat:
            Coordinates of the "search point" as a float; lat means latitude (φ).
        :type lat: float
        :param lon:
            Coordinates of the "search point" as a float; lon means longitude (λ).
        :type lon: float
        :param language:
            The specified language in ISO 639-1 format
        :type language: str
        :param data_blocks:
            A list of strings specifying which blocks of data you want to return: main, geometry, edit, location,
            attached, photos, comments, translate, similar_places, nearest_places, nearest_comments, nearest_streets,
            nearest_hotels
        :type data_blocks: list
        :param options:
            A list of options:
                * mercator - all coordinates will be in the Mercator format instead of the default format.
        :type options: list
        :param count:
            This is a variable that determines the number of results per page. 5 is default (5 min, 100 max).
        :type count: int
        :param page:
            The page number. 1 is default.
        :type page: int
        :param category:
            The WikiMapia category code as a list with category ids or text queries in UTF-8: School, Church, etc.
            Several comma-separated categories may be stated with "AND" logic. It means that only objects which have
            all listed categories together would be returned. If you need OR logic use the ``category_or`` parameter.
        :type category: list
        :param category_or:
            The WikiMapia category code as a list with category ids or text queries in UTF-8: School, Church, etc.
            Several comma-separated categories may be stated with "OR" logic. All objects which have any category from
            this list would be returned. At first all places with any of ``category_or`` categories are selected and
            then only those which have all ``category`` categories are left.
        :type category_or: list
        :param distance:
            Search only places which are not farther from the requested point than distance. Float value in meters.
        :type distance: float
        """
        url = self._base_url + '&function=place.search&q={0}&lat={1}&lon={2}'.format(query, lat, lon)

        if language and isinstance(language, str):
            url += '&language=' + language
        if data_blocks and isinstance(data_blocks, list):
            url += '&data_blocks=' + ','.join(data_blocks)
        if options and isinstance(options, list):
            url += '&options=' + ','.join(options)
        if count != 5:
            url += '&count=' + str(count)
        if page != 1:
            url += '&page=' + str(page)
        if category and isinstance(category, list):
            url += '&category=' + ','.join(category)
        if category_or and isinstance(category_or, list):
            url += '&category_or' + ','.join(category_or)
        if distance and isinstance(distance, float):
            url += '&distance=' + str(distance)

        return requests.get(url).json()

    def update_place(self, polygons, language='en', title=None, description=None, wikipedia_url=None, is_building=False,
                     tags_ids=None, street_id=None, street_name=None, building_number=None, revision_comment=None):
        """
        Creates a new place or updates an existing one.
        This function is still in a stage of development now. The function works with WikiMapia Guest's privileges only:
        it is possible to create new but not to edit existing places.

        :param polygons:
            List of tuples with the geo-points: ``[(lat1, lon1), (lat2, lon2), ..., (lat_n, lon_n)]``
        :type polygons: list
        :param language:
            The specified language in ISO 639-1 format. Defaults to 'en'
        :type language: str
        :param title:
            The place title.
        :type title: str
        :param description:
            Place description.
        :type description: str
        :param wikipedia_url:
            A link to wikipedia article about the place.
        :type wikipedia_url: str
        :param is_building:
            Set the parameter to ``True`` if the place is a building (allow to attach places to this one).
            Defaults to ``False``
        :type is_building: bool
        :param tags_ids:
            The WikiMapia category code as a list with category ids
        :type tags_ids: list
        :param street_id:
            Street ID to set into place address field. Set this parameter to 0 to remove the place address or to
            create a new street (with the ``street_name`` parameter).
        :type street_id: int
        :param street_name:
            Create a new street with this name and set it as place address. Works if ``street_id`` is 0.
        :type street_name: str
        :param building_number:
            Building number, the part of place address. Works if ``street_id`` is 0.
        :type building_number: str
        :param revision_comment:
            A brief description of the committed changes.
        :type revision_comment: str
        """

        if not isinstance(polygons, list):
            raise AttributeError('Polygons must be a list of tuples with the geo-points')

        url = self._base_url + '&function=place.update'

        url += '&polygon=' + ','.join(['{0[0]},{0[1]}'.format(point) for point in polygons])
        url += '&language=' + language

        if title and isinstance(title, str):
            url += '&title=' + requests.utils.quote(title)
        if description and isinstance(title, str):
            url += '&description=' + requests.utils.quote(description)
        if wikipedia_url and isinstance(wikipedia_url, str):
            url += '&wikipedia=' + requests.utils.quote(wikipedia_url)
        if is_building:
            url += '&is_building=1'
        if tags_ids and isinstance(tags_ids, list):
            url += '&tags_ids=' + ','.join(tags_ids)
        if street_id and isinstance(street_id, int):
            url += '&street_id=' + str(street_id)
            if street_id == 0 and street_name and isinstance(street_name, str):
                url += '&street_name=' + str(street_name)
            if street_id == 0 and building_number and isinstance(building_number, str):
                url += '&building_number=' + building_number
        if revision_comment and isinstance(revision_comment, str):
            url += '&revision_comment=' + requests.utils.quote(revision_comment)

        return requests.get(url).json()

    def get_street_by_id(self, id_, language=None, data_blocks=None, options=None):

        """
        Returns information about street. Street information is organized in data-blocks:
            * main: main information about street: url, title, description. Also if it is deleted.
            * edit: user_id and name of last editor and timestamp. If the street is in deletion state this info will be
              in the edit block also
            * location: place location: lat/lon coordinates, north/south/east/west coordinates, zoom level, country,
              state, city id and name, WikiMapia Cityguide domain name
            * related: places related to the selected street, only basic info: url, title, categories.
            * photos: photos of current street: urls to thumb, big and fullsize photo, id, size, author id and name,
              date of photo uploading, last editor of this photo, photo status (deleted/active)
            * comments: street comments: number, language of comment, author id, his ip and name, comment text,
              positive and negative votes, moderator id, name, and date of deletion if the comment was removed
            * translate: languages available for selected street
            * similar_places, nearest_places, nearest_comments, nearest_streets, nearest_hotels: extra information
              about objects around selected street

        :param id_:
            The identifier of the object you want to get information about.
        :type id_: int
        :param language:
            The specified language in ISO 639-1 format
        :type language: str
        :param data_blocks:
            A list of strings specifying which blocks of data you want to return: main, geometry, edit, location,
            attached, photos, comments, translate, similar_places, nearest_places, nearest_comments, nearest_streets,
            nearest_hotels
        :type data_blocks: list
        :param options:
            A list of options:
                * mercator - all coordinates will be in the Mercator format instead of the default format.
        :type options: list
        """
        url = self._base_url + '&function=street.getbyid&id=' + str(id_)
        if language and isinstance(language, str):
            url += '&language=' + language
        if data_blocks and isinstance(data_blocks, list):
            url += '&data_blocks=' + ','.join(data_blocks)
        if options and isinstance(options, list):
            url += '&options=' + ','.join(options)

        return requests.get(url).json()

    def get_category_by_id(self, id_, language):
        """
        Returns all information about selected category.

        :param id_:
            The identifier of the category you want to get information about.
        :type id_: int
        :param language:
            This is specified language in ISO 639-1 format.
        :type language: str
        """
        url = self._base_url + '&function=category.getbyid&id=' + str(id_)

        if language and isinstance(language, str):
            url += '&language=' + language

        return requests.get(url).json()

    def get_all_categories(self, language=None, name=None, page=1, count=50):
        """
        Returns WikiMapia approved categories list. Optionally searches categories by name or a part of name.

        :param language:
            The specified language in ISO 639-1 format.
        :type language: str
        :param name:
            WikiMapia category name (or a part of it) in UTF-8: name=School, name=Church etc. or a part of it for
            searching
        :type name: str
        :param page:
            The page number. 1 is default.
        :type page: int
        :param count:
            This is a variable that determines the number of results per page. 50 is default (5 min, 100 max).
        :type count: int
        """
        url = self._base_url + '&function=category.getall'
        if language and isinstance(language, str):
            url += '&language=' + language
        if name and isinstance(name, str):
            url += '&language=' + name
        if count != 50:
            url += '&count=' + str(count)
        if page != 1:
            url += '&page=' + str(page)

        return requests.get(url).json()


__all__ = ['PyMapia']