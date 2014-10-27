from datatypes.core import unicoded

sample_geojson_polygon = unicoded({
    "type": "Feature",

    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:EPSG::27700"
        }
    },

    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [530857.01, 181500.00],
                [530857.00, 181500.00],
                [530857.00, 181500.00],
                [530857.00, 181500.00],
                [530857.01, 181500.00]
            ]
        ]
    },
    "properties": {
        'foo': 'bar',
        'bang': 'boom'
    }
})

sample_geojson_from_migration = unicoded({
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [508220.47000000003, 221784.46],
                [508216.4, 221786.99],
                [508211.82, 221789.84],
                [508200.75, 221796.74],
                [508205.62, 221802.23],
                [508207.56, 221800.58000000002],
                [508217.63, 221792.66],
                [508224.31, 221787.24],
                [508221.95, 221785.55000000002],
                [508220.47000000003, 221784.46]
            ]
        ]
    },

    "properties": {
        "title_number": "BD161871",
        "source": "title_plan_extent"
    },

    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:EPSG::27700"
        }
    }
})

sample_invalid_geojson = unicoded({
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [508220, 123]
            ]
        ]
    },

    "properties": {
        "title_number": "BD161871",
        "source": "title_plan_extent"
    },

    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:EPSG::27700"
        }
    }
})

sample_lincolns_inn_fields = unicoded({
    "type": "Feature",
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:EPSG::27700"
        }
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [
                    530707.00,
                    181399.00
                ],
                [
                    530739.00,
                    181313.00
                ],
                [
                    530864.00,
                    181369.00
                ],
                [
                    530808.00,
                    181431.00
                ],
                [
                    530707.00,
                    181399.00
                ]
            ]
        ]
    },
    "properties": {
        "name": "Lincoln's Inn Fields Easement"
    }
})

sample_invalid_point = unicoded({
    "type": "Feature",

    "geometry": {
        "type": "Point",
        "coordinates": [125.6, 10.1]
    },

    "properties": {
        "name": "Dinagat Islands"
    }
})
