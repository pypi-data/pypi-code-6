from lxml import etree


__all__ = [
    'getParser',
    'ParseError',
]


class ParseError(Exception):
    pass


class XMLParser(object):
    def __init__(self):
        pass

    def __call__(self, xml):
        """
        @type xml: unicode object
        """
        assert isinstance(xml, unicode), u"xml should be a unicode object"

        res = []
        response = etree.XML(xml.encode('utf-8'))

        if response[0].tag == 'error':
            raise ParseError(
                response.xpath('//errorCode')[0],
                response.xpath('//errorMsg')[0]
            )

        items = response.xpath('locationList')[0].xpath('item')
        for item in items:
            # coherence indicate the presence of some tags
            coherence_street = item.xpath('coherenceDegree/street')[0].text
            coherence_city = item.xpath('coherenceDegree/city')[0].text

            # location supplies informations as lat/long, street, zip_code...
            location = item.xpath('location')[0]

            # Xpath all entries
            type_response = item.xpath('type')
            streetLabel = location.xpath('streetLabel')
            city = location.xpath('city')
            postalCode = location.xpath('postalCode')
            countryLabel = location.xpath('countryLabel')
            countryOfficial = location.xpath('countryOfficial')
            formattedAddressLine = location.xpath('formattedAddressLine')
            formattedCityLine = location.xpath('formattedCityLine')
            area = location.xpath('area')

            # Save all we can get, other are None

            data = {
                'type': type_response[0].text if type_response else u"",
                'streetLabel': streetLabel[0].text if streetLabel else u"",
                'city': city[0].text if city else u"",
                'postalCode': postalCode[0].text if postalCode else u"",
                'countryLabel': countryLabel[0].text if countryLabel else u"",
                'countryOfficial': (
                    countryOfficial[0].text
                    if countryOfficial
                    else u""
                ),
                'formattedAddressLine': (
                    formattedAddressLine[0].text
                    if formattedAddressLine
                    else u""
                ),
                'formattedCityLine': (
                    formattedCityLine[0].text
                    if formattedCityLine
                    else u""
                ),
                'area': area[0].text if area else u"",
                'latitude': location.xpath('coords/lat')[0].text,
                'longitude': location.xpath('coords/lon')[0].text,
                'coherence_street': coherence_street,
                'coherence_city': coherence_city,
            }

            res.append(data)

        return res


def getParser(parser_type):
    if parser_type == 'xml':
        return XMLParser()
    return None
