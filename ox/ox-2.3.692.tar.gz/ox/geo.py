# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2008
from __future__ import with_statement, print_function

import math

__all__ = ['get_country', 'get_country_name', 'normalize_country_name']

def update_countries():
    '''
        to update list of countries run the following command in python-ox
        echo "import ox.geo;ox.geo.update_countries()" | python
    '''
    import re
    import json
    from .net import read_url

    COUNTRIES = json.loads(read_url('http://oxjs.org/source/Ox.Geo/json/Ox.Geo.json'))
    countries = {}
    for country in COUNTRIES:
        #only existing countres have 2 codes
        if True or len(country['code']) == 2:
            countries[country['code']] = {
                "name": country['name'],
                "region": country['region'],
                "continent": country['continent'],
            }
            for key in ('googleName', 'imdbName'):
                if key in country:
                    if not 'aliases' in countries[country['code']]:
                        countries[country['code']]['aliases'] = []
                    if country[key] not in countries[country['code']]['aliases']:
                        countries[country['code']]['aliases'].append(country[key])

    data = json.dumps(countries, indent=4, ensure_ascii=False).encode('utf-8')
    with open('ox/geo.py') as f:
        pydata = f.read()
    pydata = re.sub(
        re.compile('\nCOUNTRIES = {.*?}\n\n', re.DOTALL),
        '\nCOUNTRIES = %s\n\n' % data, pydata)

    with open('ox/geo.py', 'w') as f:
        f.write(pydata)
    print('ox/geo.py updated')

COUNTRIES = {
    u"GE-AB": {
        u"region": u"Western Asia", 
        u"name": u"Abkhazia", 
        u"continent": u"Asia"
    }, 
    u"CW": {
        u"region": u"Caribbean", 
        u"name": u"Curaçao", 
        u"continent": u"South America"
    }, 
    u"GW": {
        u"region": u"Western Africa", 
        u"name": u"Guinea-Bissau", 
        u"continent": u"Africa"
    }, 
    u"GU": {
        u"region": u"Micronesia", 
        u"name": u"Guam", 
        u"continent": u"Oceania"
    }, 
    u"GT": {
        u"region": u"Central America", 
        u"name": u"Guatemala", 
        u"continent": u"South America"
    }, 
    u"GS": {
        u"region": u"Antarctica", 
        u"name": u"South Georgia and the South Sandwich Islands", 
        u"continent": u"Antarctica"
    }, 
    u"GR": {
        u"region": u"Southern Europe", 
        u"name": u"Greece", 
        u"continent": u"Europe"
    }, 
    u"GQ": {
        u"region": u"Middle Africa", 
        u"name": u"Equatorial Guinea", 
        u"continent": u"Africa"
    }, 
    u"GP": {
        u"region": u"Caribbean", 
        u"name": u"Guadeloupe", 
        u"continent": u"South America"
    }, 
    u"KAKH": {
        u"region": u"South-Eastern Asia", 
        u"name": u"Kampuchea", 
        u"continent": u"Asia"
    }, 
    u"GY": {
        u"region": u"Southern America", 
        u"name": u"Guyana", 
        u"continent": u"South America"
    }, 
    u"GG": {
        u"region": u"Northern Europe", 
        u"name": u"Guernsey", 
        u"continent": u"Europe"
    }, 
    u"BYAA": {
        u"region": u"Eastern Europe", 
        u"name": u"Byelorussian Soviet Socialist Republic", 
        u"continent": u"Europe"
    }, 
    u"GE": {
        u"region": u"Western Asia", 
        u"name": u"Georgia", 
        u"continent": u"Asia"
    }, 
    u"GD": {
        u"region": u"Caribbean", 
        u"name": u"Grenada", 
        u"continent": u"South America"
    }, 
    u"GB": {
        u"region": u"Northern Europe", 
        u"aliases": [
            u"UK"
        ], 
        u"name": u"United Kingdom", 
        u"continent": u"Europe"
    }, 
    u"GA": {
        u"region": u"Middle Africa", 
        u"name": u"Gabon", 
        u"continent": u"Africa"
    }, 
    u"YEYE": {
        u"region": u"Western Asia", 
        u"name": u"North Yemen", 
        u"continent": u"Asia"
    }, 
    u"GN": {
        u"region": u"Western Africa", 
        u"name": u"Guinea", 
        u"continent": u"Africa"
    }, 
    u"GM": {
        u"region": u"Western Africa", 
        u"aliases": [
            u"The Gambia"
        ], 
        u"name": u"Gambia", 
        u"continent": u"Africa"
    }, 
    u"GL": {
        u"region": u"Northern America", 
        u"name": u"Greenland", 
        u"continent": u"North America"
    }, 
    u"GI": {
        u"region": u"Southern Europe", 
        u"name": u"Gibraltar", 
        u"continent": u"Europe"
    }, 
    u"GH": {
        u"region": u"Western Africa", 
        u"name": u"Ghana", 
        u"continent": u"Africa"
    }, 
    u"SUHH": {
        u"region": u"Eastern Europe", 
        u"name": u"Soviet Union", 
        u"continent": u"Europe"
    }, 
    u"JTUM": {
        u"region": u"Polynesia", 
        u"name": u"Johnston Island", 
        u"continent": u"Oceania"
    }, 
    u"EH": {
        u"region": u"Northern Africa", 
        u"aliases": [
            u"Western Sahara"
        ], 
        u"name": u"Sahrawi", 
        u"continent": u"Africa"
    }, 
    u"ANHH": {
        u"region": u"Caribbean", 
        u"name": u"Netherlands Antilles", 
        u"continent": u"South America"
    }, 
    u"AE-RK": {
        u"region": u"Western Asia", 
        u"name": u"Ras al-Khaimah", 
        u"continent": u"Asia"
    }, 
    u"ZA": {
        u"region": u"Southern Africa", 
        u"name": u"South Africa", 
        u"continent": u"Africa"
    }, 
    u"GB-WLS": {
        u"region": u"Northern Europe", 
        u"name": u"Wales", 
        u"continent": u"Europe"
    }, 
    u"ZW": {
        u"region": u"Eastern Africa", 
        u"name": u"Zimbabwe", 
        u"continent": u"Africa"
    }, 
    u"YUCS": {
        u"region": u"Southern Europe", 
        u"aliases": [
            u"Federal Republic of Yugoslavia"
        ], 
        u"name": u"Yugoslavia", 
        u"continent": u"Europe"
    }, 
    u"ME": {
        u"region": u"Southern Europe", 
        u"name": u"Montenegro", 
        u"continent": u"Europe"
    }, 
    u"MD": {
        u"region": u"Eastern Europe", 
        u"name": u"Moldova", 
        u"continent": u"Europe"
    }, 
    u"MG": {
        u"region": u"Eastern Africa", 
        u"name": u"Madagascar", 
        u"continent": u"Africa"
    }, 
    u"MF": {
        u"region": u"Caribbean", 
        u"aliases": [
            u"Saint Martin (French part)"
        ], 
        u"name": u"Saint Martin", 
        u"continent": u"South America"
    }, 
    u"MA": {
        u"region": u"Northern Africa", 
        u"name": u"Morocco", 
        u"continent": u"Africa"
    }, 
    u"MC": {
        u"region": u"Western Europe", 
        u"name": u"Monaco", 
        u"continent": u"Europe"
    }, 
    u"MM": {
        u"region": u"South-Eastern Asia", 
        u"aliases": [
            u"Burma"
        ], 
        u"name": u"Myanmar", 
        u"continent": u"Asia"
    }, 
    u"ML": {
        u"region": u"Western Africa", 
        u"name": u"Mali", 
        u"continent": u"Africa"
    }, 
    u"MO": {
        u"region": u"Eastern Asia", 
        u"aliases": [
            u"Macao"
        ], 
        u"name": u"Macau", 
        u"continent": u"Asia"
    }, 
    u"MN": {
        u"region": u"Eastern Asia", 
        u"name": u"Mongolia", 
        u"continent": u"Asia"
    }, 
    u"AE-UQ": {
        u"region": u"Western Asia", 
        u"name": u"Umm al-Quwain", 
        u"continent": u"Asia"
    }, 
    u"MH": {
        u"region": u"Micronesia", 
        u"name": u"Marshall Islands", 
        u"continent": u"Oceania"
    }, 
    u"MK": {
        u"region": u"Southern Europe", 
        u"aliases": [
            u"Former Yugoslav Republic of Macedonia", 
            u"Republic of Macedonia"
        ], 
        u"name": u"Macedonia", 
        u"continent": u"Europe"
    }, 
    u"MU": {
        u"region": u"Eastern Africa", 
        u"name": u"Mauritius", 
        u"continent": u"Africa"
    }, 
    u"MT": {
        u"region": u"Southern Europe", 
        u"name": u"Malta", 
        u"continent": u"Europe"
    }, 
    u"MW": {
        u"region": u"Eastern Africa", 
        u"name": u"Malawi", 
        u"continent": u"Africa"
    }, 
    u"MV": {
        u"region": u"Southern Asia", 
        u"name": u"Maldives", 
        u"continent": u"Asia"
    }, 
    u"MQ": {
        u"region": u"Caribbean", 
        u"name": u"Martinique", 
        u"continent": u"South America"
    }, 
    u"MP": {
        u"region": u"Micronesia", 
        u"name": u"Northern Mariana Islands", 
        u"continent": u"Oceania"
    }, 
    u"MS": {
        u"region": u"Caribbean", 
        u"name": u"Montserrat", 
        u"continent": u"South America"
    }, 
    u"MR": {
        u"region": u"Western Africa", 
        u"name": u"Mauritania", 
        u"continent": u"Africa"
    }, 
    u"MY": {
        u"region": u"South-Eastern Asia", 
        u"name": u"Malaysia", 
        u"continent": u"Asia"
    }, 
    u"MX": {
        u"region": u"Central America", 
        u"name": u"Mexico", 
        u"continent": u"South America"
    }, 
    u"MZ": {
        u"region": u"Eastern Africa", 
        u"name": u"Mozambique", 
        u"continent": u"Africa"
    }, 
    u"FR": {
        u"region": u"Western Europe", 
        u"name": u"France", 
        u"continent": u"Europe"
    }, 
    u"ZRCD": {
        u"region": u"Middle Africa", 
        u"name": u"Zaire", 
        u"continent": u"Africa"
    }, 
    u"ZA-BO": {
        u"region": u"Southern Africa", 
        u"name": u"Bophuthatswana", 
        u"continent": u"Africa"
    }, 
    u"FI": {
        u"region": u"Northern Europe", 
        u"name": u"Finland", 
        u"continent": u"Europe"
    }, 
    u"FJ": {
        u"region": u"Melanesia", 
        u"name": u"Fiji", 
        u"continent": u"Oceania"
    }, 
    u"FK": {
        u"region": u"Southern America", 
        u"name": u"Falkland Islands", 
        u"continent": u"South America"
    }, 
    u"FM": {
        u"region": u"Micronesia", 
        u"aliases": [
            u"Federated States of Micronesia"
        ], 
        u"name": u"Micronesia", 
        u"continent": u"Oceania"
    }, 
    u"FO": {
        u"region": u"Northern Europe", 
        u"name": u"Faroe Islands", 
        u"continent": u"Europe"
    }, 
    u"SITH": {
        u"region": u"South-Eastern Asia", 
        u"name": u"Siam", 
        u"continent": u"Asia"
    }, 
    u"NHVU": {
        u"region": u"Melanesia", 
        u"name": u"New Hebrides", 
        u"continent": u"Oceania"
    }, 
    u"AR-AQ": {
        u"region": u"Antarctica", 
        u"name": u"Argentine Antarctica", 
        u"continent": u"Antarctica"
    }, 
    u"FR-AQ": {
        u"region": u"Antarctica", 
        u"name": u"Adélie Land", 
        u"continent": u"Antarctica"
    }, 
    u"NHVU-VE": {
        u"region": u"Melanesia", 
        u"name": u"Vemerana", 
        u"continent": u"Oceania"
    }, 
    u"SZ": {
        u"region": u"Southern Africa", 
        u"name": u"Swaziland", 
        u"continent": u"Africa"
    }, 
    u"SY": {
        u"region": u"Western Asia", 
        u"name": u"Syria", 
        u"continent": u"Asia"
    }, 
    u"SX": {
        u"region": u"Caribbean", 
        u"name": u"Sint Maarten", 
        u"continent": u"South America"
    }, 
    u"SS": {
        u"region": u"Northern Africa", 
        u"name": u"South Sudan", 
        u"continent": u"Africa"
    }, 
    u"SR": {
        u"region": u"Southern America", 
        u"name": u"Suriname", 
        u"continent": u"South America"
    }, 
    u"SV": {
        u"region": u"Central America", 
        u"name": u"El Salvador", 
        u"continent": u"South America"
    }, 
    u"ST": {
        u"region": u"Middle Africa", 
        u"aliases": [
            u"Sao Tome and Principe"
        ], 
        u"name": u"São Tomé and Príncipe", 
        u"continent": u"Africa"
    }, 
    u"SK": {
        u"region": u"Eastern Europe", 
        u"name": u"Slovakia", 
        u"continent": u"Europe"
    }, 
    u"SJ": {
        u"region": u"Northern Europe", 
        u"name": u"Svalbard and Jan Mayen", 
        u"continent": u"Europe"
    }, 
    u"SI": {
        u"region": u"Southern Europe", 
        u"name": u"Slovenia", 
        u"continent": u"Europe"
    }, 
    u"SH": {
        u"region": u"Western Africa", 
        u"aliases": [
            u"Saint Helena"
        ], 
        u"name": u"Saint Helena, Ascension and Tristan da Cunha", 
        u"continent": u"Africa"
    }, 
    u"SO": {
        u"region": u"Eastern Africa", 
        u"name": u"Somalia", 
        u"continent": u"Africa"
    }, 
    u"SN": {
        u"region": u"Western Africa", 
        u"name": u"Senegal", 
        u"continent": u"Africa"
    }, 
    u"SM": {
        u"region": u"Southern Europe", 
        u"name": u"San Marino", 
        u"continent": u"Europe"
    }, 
    u"SL": {
        u"region": u"Western Africa", 
        u"name": u"Sierra Leone", 
        u"continent": u"Africa"
    }, 
    u"SC": {
        u"region": u"Eastern Africa", 
        u"name": u"Seychelles", 
        u"continent": u"Africa"
    }, 
    u"SB": {
        u"region": u"Melanesia", 
        u"name": u"Solomon Islands", 
        u"continent": u"Oceania"
    }, 
    u"SA": {
        u"region": u"Western Asia", 
        u"name": u"Saudi Arabia", 
        u"continent": u"Asia"
    }, 
    u"SG": {
        u"region": u"South-Eastern Asia", 
        u"name": u"Singapore", 
        u"continent": u"Asia"
    }, 
    u"SE": {
        u"region": u"Northern Europe", 
        u"name": u"Sweden", 
        u"continent": u"Europe"
    }, 
    u"SD": {
        u"region": u"Northern Africa", 
        u"name": u"Sudan", 
        u"continent": u"Africa"
    }, 
    u"YE": {
        u"region": u"Western Asia", 
        u"name": u"Yemen", 
        u"continent": u"Asia"
    }, 
    u"YT": {
        u"region": u"Eastern Africa", 
        u"name": u"Mayotte", 
        u"continent": u"Africa"
    }, 
    u"LB": {
        u"region": u"Western Asia", 
        u"name": u"Lebanon", 
        u"continent": u"Asia"
    }, 
    u"LC": {
        u"region": u"Caribbean", 
        u"name": u"Saint Lucia", 
        u"continent": u"South America"
    }, 
    u"LA": {
        u"region": u"South-Eastern Asia", 
        u"name": u"Laos", 
        u"continent": u"Asia"
    }, 
    u"ZA-TR": {
        u"region": u"Southern Africa", 
        u"name": u"Transkei", 
        u"continent": u"Africa"
    }, 
    u"LK": {
        u"region": u"Southern Asia", 
        u"name": u"Sri Lanka", 
        u"continent": u"Asia"
    }, 
    u"LI": {
        u"region": u"Western Europe", 
        u"name": u"Liechtenstein", 
        u"continent": u"Europe"
    }, 
    u"LV": {
        u"region": u"Northern Europe", 
        u"name": u"Latvia", 
        u"continent": u"Europe"
    }, 
    u"LT": {
        u"region": u"Northern Europe", 
        u"name": u"Lithuania", 
        u"continent": u"Europe"
    }, 
    u"LU": {
        u"region": u"Western Europe", 
        u"name": u"Luxembourg", 
        u"continent": u"Europe"
    }, 
    u"PG-NSA": {
        u"region": u"Melanesia", 
        u"name": u"Bougainville", 
        u"continent": u"Oceania"
    }, 
    u"LS": {
        u"region": u"Southern Africa", 
        u"name": u"Lesotho", 
        u"continent": u"Africa"
    }, 
    u"LY": {
        u"region": u"Northern Africa", 
        u"name": u"Libya", 
        u"continent": u"Africa"
    }, 
    u"DEDE": {
        u"region": u"Western Europe", 
        u"name": u"West Germany", 
        u"continent": u"Europe"
    }, 
    u"GF": {
        u"region": u"Southern America", 
        u"name": u"French Guiana", 
        u"continent": u"South America"
    }, 
    u"AU-CS": {
        u"region": u"Australia and New Zealand", 
        u"name": u"Coral Sea Islands", 
        u"continent": u"Oceania"
    }, 
    u"WKUM": {
        u"region": u"Micronesia", 
        u"name": u"Wake Island", 
        u"continent": u"Oceania"
    }, 
    u"UAUA": {
        u"region": u"Eastern Europe", 
        u"name": u"Ukrainian Soviet Socialist Republic", 
        u"continent": u"Europe"
    }, 
    u"CTKI": {
        u"region": u"Micronesia", 
        u"name": u"Canton and Enderbury Islands", 
        u"continent": u"Oceania"
    }, 
    u"RU": {
        u"region": u"Eastern Europe", 
        u"name": u"Russia", 
        u"continent": u"Europe"
    }, 
    u"RW": {
        u"region": u"Eastern Africa", 
        u"name": u"Rwanda", 
        u"continent": u"Africa"
    }, 
    u"RS": {
        u"region": u"Southern Europe", 
        u"name": u"Serbia", 
        u"continent": u"Europe"
    }, 
    u"RE": {
        u"region": u"Eastern Africa", 
        u"name": u"Réunion", 
        u"continent": u"Africa"
    }, 
    u"LR": {
        u"region": u"Western Africa", 
        u"name": u"Liberia", 
        u"continent": u"Africa"
    }, 
    u"RO": {
        u"region": u"Eastern Europe", 
        u"name": u"Romania", 
        u"continent": u"Europe"
    }, 
    u"PK-NA": {
        u"region": u"Southern Asia", 
        u"name": u"Gilgit-Baltistan", 
        u"continent": u"Asia"
    }, 
    u"GG-HE": {
        u"region": u"Northern Europe", 
        u"name": u"Herm", 
        u"continent": u"Europe"
    }, 
    u"CSXX": {
        u"region": u"Southern Europe", 
        u"name": u"Serbia and Montenegro", 
        u"continent": u"Europe"
    }, 
    u"AU-AC": {
        u"region": u"Australia and New Zealand", 
        u"name": u"Ashmore and Cartier Islands", 
        u"continent": u"Oceania"
    }, 
    u"AU-AQ": {
        u"region": u"Antarctica", 
        u"name": u"Australian Antarctic Territory", 
        u"continent": u"Antarctica"
    }, 
    u"TPTL": {
        u"region": u"South-Eastern Asia", 
        u"name": u"East Timor", 
        u"continent": u"Asia"
    }, 
    u"GEKI": {
        u"region": u"Micronesia", 
        u"name": u"Gilbert Islands", 
        u"continent": u"Oceania"
    }, 
    u"NQAQ": {
        u"region": u"Antarctica", 
        u"name": u"Queen Maud Land", 
        u"continent": u"Antarctica"
    }, 
    u"EE": {
        u"region": u"Northern Europe", 
        u"name": u"Estonia", 
        u"continent": u"Europe"
    }, 
    u"EG": {
        u"region": u"Northern Africa", 
        u"name": u"Egypt", 
        u"continent": u"Africa"
    }, 
    u"EA": {
        u"region": u"Northern Africa", 
        u"name": u"Ceuta and Melilla", 
        u"continent": u"Africa"
    }, 
    u"EC": {
        u"region": u"Southern America", 
        u"name": u"Ecuador", 
        u"continent": u"South America"
    }, 
    u"EU": {
        u"region": u"Western Europe", 
        u"name": u"European Union", 
        u"continent": u"Europe"
    }, 
    u"ET": {
        u"region": u"Eastern Africa", 
        u"name": u"Ethiopia", 
        u"continent": u"Africa"
    }, 
    u"ES": {
        u"region": u"Southern Europe", 
        u"name": u"Spain", 
        u"continent": u"Europe"
    }, 
    u"ER": {
        u"region": u"Eastern Africa", 
        u"name": u"Eritrea", 
        u"continent": u"Africa"
    }, 
    u"RU-CE": {
        u"region": u"Eastern Europe", 
        u"name": u"Chechnia", 
        u"continent": u"Europe"
    }, 
    u"VU": {
        u"region": u"Melanesia", 
        u"name": u"Vanuatu", 
        u"continent": u"Oceania"
    }, 
    u"AIDJ": {
        u"region": u"Eastern Africa", 
        u"name": u"French Afar and Issas", 
        u"continent": u"Africa"
    }, 
    u"IN": {
        u"region": u"Southern Asia", 
        u"name": u"India", 
        u"continent": u"Asia"
    }, 
    u"XK": {
        u"region": u"Southern Europe", 
        u"aliases": [
            u"Kosova (Kosovo)"
        ], 
        u"name": u"Kosovo", 
        u"continent": u"Europe"
    }, 
    u"PK-JK": {
        u"region": u"Southern Asia", 
        u"name": u"Azad Kashmir", 
        u"continent": u"Asia"
    }, 
    u"BUMM": {
        u"region": u"South-Eastern Asia", 
        u"name": u"Burma", 
        u"continent": u"Asia"
    }, 
    u"NR": {
        u"region": u"Micronesia", 
        u"name": u"Nauru", 
        u"continent": u"Oceania"
    }, 
    u"KG": {
        u"region": u"Central Asia", 
        u"name": u"Kyrgyzstan", 
        u"continent": u"Asia"
    }, 
    u"KE": {
        u"region": u"Eastern Africa", 
        u"name": u"Kenya", 
        u"continent": u"Africa"
    }, 
    u"KI": {
        u"region": u"Micronesia", 
        u"name": u"Kiribati", 
        u"continent": u"Oceania"
    }, 
    u"KH": {
        u"region": u"South-Eastern Asia", 
        u"name": u"Cambodia", 
        u"continent": u"Asia"
    }, 
    u"KN": {
        u"region": u"Caribbean", 
        u"name": u"Saint Kitts and Nevis", 
        u"continent": u"South America"
    }, 
    u"KM": {
        u"region": u"Eastern Africa", 
        u"name": u"Comoros", 
        u"continent": u"Africa"
    }, 
    u"KR": {
        u"region": u"Eastern Asia", 
        u"name": u"South Korea", 
        u"continent": u"Asia"
    }, 
    u"KP": {
        u"region": u"Eastern Asia", 
        u"name": u"North Korea", 
        u"continent": u"Asia"
    }, 
    u"KW": {
        u"region": u"Western Asia", 
        u"name": u"Kuwait", 
        u"continent": u"Asia"
    }, 
    u"KZ": {
        u"region": u"Central Asia", 
        u"name": u"Kazakhstan", 
        u"continent": u"Asia"
    }, 
    u"KY": {
        u"region": u"Caribbean", 
        u"name": u"Cayman Islands", 
        u"continent": u"South America"
    }, 
    u"DO": {
        u"region": u"Caribbean", 
        u"name": u"Dominican Republic", 
        u"continent": u"South America"
    }, 
    u"DM": {
        u"region": u"Caribbean", 
        u"name": u"Dominica", 
        u"continent": u"South America"
    }, 
    u"DJ": {
        u"region": u"Eastern Africa", 
        u"name": u"Djibouti", 
        u"continent": u"Africa"
    }, 
    u"DK": {
        u"region": u"Northern Europe", 
        u"name": u"Denmark", 
        u"continent": u"Europe"
    }, 
    u"DG": {
        u"region": u"Southern Asia", 
        u"name": u"Diego Garcia", 
        u"continent": u"Asia"
    }, 
    u"DE": {
        u"region": u"Western Europe", 
        u"name": u"Germany", 
        u"continent": u"Europe"
    }, 
    u"DZ": {
        u"region": u"Northern Africa", 
        u"name": u"Algeria", 
        u"continent": u"Africa"
    }, 
    u"BQAQ": {
        u"region": u"Antarctica", 
        u"name": u"British Antarctic Territory", 
        u"continent": u"Antarctica"
    }, 
    u"ZA-CI": {
        u"region": u"Southern Africa", 
        u"name": u"Ciskei", 
        u"continent": u"Africa"
    }, 
    u"GB-SL": {
        u"region": u"Northern Europe", 
        u"name": u"Sealand", 
        u"continent": u"Europe"
    }, 
    u"MD-SN": {
        u"region": u"Eastern Europe", 
        u"name": u"Transnistria", 
        u"continent": u"Europe"
    }, 
    u"SKIN": {
        u"region": u"Southern Asia", 
        u"name": u"Sikkim", 
        u"continent": u"Asia"
    }, 
    u"FXFR": {
        u"region": u"Western Europe", 
        u"name": u"Metropolitan France", 
        u"continent": u"Europe"
    }, 
    u"AE-FU": {
        u"region": u"Western Asia", 
        u"name": u"Fujairah", 
        u"continent": u"Asia"
    }, 
    u"QA": {
        u"region": u"Western Asia", 
        u"name": u"Qatar", 
        u"continent": u"Asia"
    }, 
    u"WF": {
        u"region": u"Polynesia", 
        u"name": u"Wallis and Futuna", 
        u"continent": u"Oceania"
    }, 
    u"JP": {
        u"region": u"Eastern Asia", 
        u"name": u"Japan", 
        u"continent": u"Asia"
    }, 
    u"JM": {
        u"region": u"Caribbean", 
        u"name": u"Jamaica", 
        u"continent": u"South America"
    }, 
    u"JO": {
        u"region": u"Western Asia", 
        u"name": u"Jordan", 
        u"continent": u"Asia"
    }, 
    u"WS": {
        u"region": u"Polynesia", 
        u"name": u"Samoa", 
        u"continent": u"Oceania"
    }, 
    u"JE": {
        u"region": u"Northern Europe", 
        u"name": u"Jersey", 
        u"continent": u"Europe"
    }, 
    u"KM-M": {
        u"region": u"Eastern Africa", 
        u"name": u"Mohéli", 
        u"continent": u"Africa"
    }, 
    u"KM-A": {
        u"region": u"Eastern Africa", 
        u"name": u"Anjouan", 
        u"continent": u"Africa"
    }, 
    u"PZPA": {
        u"region": u"Central America", 
        u"name": u"Panama Canal Zone", 
        u"continent": u"South America"
    }, 
    u"MIUM": {
        u"region": u"Polynesia", 
        u"name": u"Midway Islands", 
        u"continent": u"Oceania"
    }, 
    u"GEHH": {
        u"region": u"Micronesia", 
        u"name": u"Gilbert and Ellice Islands", 
        u"continent": u"Oceania"
    }, 
    u"NZ-AQ": {
        u"region": u"Antarctica", 
        u"name": u"Ross Dependency", 
        u"continent": u"Antarctica"
    }, 
    u"HVBF": {
        u"region": u"Western Africa", 
        u"name": u"Upper Volta", 
        u"continent": u"Africa"
    }, 
    u"GB-AD": {
        u"region": u"Western Asia", 
        u"name": u"Akrotiri and Dhekelia", 
        u"continent": u"Asia"
    }, 
    u"UG-RW": {
        u"region": u"Eastern Africa", 
        u"name": u"Rwenzururu", 
        u"continent": u"Africa"
    }, 
    u"ZM": {
        u"region": u"Eastern Africa", 
        u"name": u"Zambia", 
        u"continent": u"Africa"
    }, 
    u"NTHH": {
        u"region": u"Western Asia", 
        u"name": u"Neutral Zone", 
        u"continent": u"Asia"
    }, 
    u"PR": {
        u"region": u"Caribbean", 
        u"name": u"Puerto Rico", 
        u"continent": u"South America"
    }, 
    u"PS": {
        u"region": u"Western Asia", 
        u"aliases": [
            u"Palestinian Territories", 
            u"Occupied Palestinian Territory"
        ], 
        u"name": u"Palestine", 
        u"continent": u"Asia"
    }, 
    u"PW": {
        u"region": u"Micronesia", 
        u"name": u"Palau", 
        u"continent": u"Oceania"
    }, 
    u"PT": {
        u"region": u"Southern Europe", 
        u"name": u"Portugal", 
        u"continent": u"Europe"
    }, 
    u"PY": {
        u"region": u"Southern America", 
        u"name": u"Paraguay", 
        u"continent": u"South America"
    }, 
    u"PA": {
        u"region": u"Central America", 
        u"name": u"Panama", 
        u"continent": u"South America"
    }, 
    u"PF": {
        u"region": u"Polynesia", 
        u"name": u"French Polynesia", 
        u"continent": u"Oceania"
    }, 
    u"PG": {
        u"region": u"Melanesia", 
        u"name": u"Papua New Guinea", 
        u"continent": u"Oceania"
    }, 
    u"PE": {
        u"region": u"Southern America", 
        u"name": u"Peru", 
        u"continent": u"South America"
    }, 
    u"PK": {
        u"region": u"Southern Asia", 
        u"name": u"Pakistan", 
        u"continent": u"Asia"
    }, 
    u"PH": {
        u"region": u"South-Eastern Asia", 
        u"name": u"Philippines", 
        u"continent": u"Asia"
    }, 
    u"PN": {
        u"region": u"Polynesia", 
        u"aliases": [
            u"Pitcairn"
        ], 
        u"name": u"Pitcairn Islands", 
        u"continent": u"Oceania"
    }, 
    u"PL": {
        u"region": u"Eastern Europe", 
        u"name": u"Poland", 
        u"continent": u"Europe"
    }, 
    u"PM": {
        u"region": u"Northern America", 
        u"name": u"Saint Pierre and Miquelon", 
        u"continent": u"North America"
    }, 
    u"VDVN": {
        u"region": u"South-Eastern Asia", 
        u"name": u"North Vietnam", 
        u"continent": u"Asia"
    }, 
    u"NO-PI": {
        u"region": u"Antarctica", 
        u"name": u"Peter I Island", 
        u"continent": u"Antarctica"
    }, 
    u"KOJP": {
        u"region": u"Eastern Asia", 
        u"name": u"Korea", 
        u"continent": u"Asia"
    }, 
    u"GBBZ": {
        u"region": u"Central America", 
        u"name": u"British Honduras", 
        u"continent": u"South America"
    }, 
    u"RHZW-ZR": {
        u"region": u"Eastern Africa", 
        u"name": u"Zimbabwe Rhodesia", 
        u"continent": u"Africa"
    }, 
    u"GB-NIR": {
        u"region": u"Northern Europe", 
        u"name": u"Northern Ireland", 
        u"continent": u"Europe"
    }, 
    u"NG-BI": {
        u"region": u"Western Africa", 
        u"name": u"Biafra", 
        u"continent": u"Africa"
    }, 
    u"CK": {
        u"region": u"Polynesia", 
        u"name": u"Cook Islands", 
        u"continent": u"Oceania"
    }, 
    u"CI": {
        u"region": u"Western Africa", 
        u"aliases": [
            u"Ivory Coast"
        ], 
        u"name": u"Côte d'Ivoire", 
        u"continent": u"Africa"
    }, 
    u"CH": {
        u"region": u"Western Europe", 
        u"name": u"Switzerland", 
        u"continent": u"Europe"
    }, 
    u"CO": {
        u"region": u"Southern America", 
        u"name": u"Colombia", 
        u"continent": u"South America"
    }, 
    u"CN": {
        u"region": u"Eastern Asia", 
        u"name": u"China", 
        u"continent": u"Asia"
    }, 
    u"CM": {
        u"region": u"Middle Africa", 
        u"name": u"Cameroon", 
        u"continent": u"Africa"
    }, 
    u"CL-AQ": {
        u"region": u"Antarctica", 
        u"name": u"Chilean Antarctic Territory", 
        u"continent": u"Antarctica"
    }, 
    u"CC": {
        u"region": u"South-Eastern Asia", 
        u"aliases": [
            u"Cocos (Keeling) Islands"
        ], 
        u"name": u"Cocos Islands", 
        u"continent": u"Asia"
    }, 
    u"CA": {
        u"region": u"Northern America", 
        u"name": u"Canada", 
        u"continent": u"North America"
    }, 
    u"CG": {
        u"region": u"Middle Africa", 
        u"aliases": [
            u"Congo"
        ], 
        u"name": u"Republic of the Congo", 
        u"continent": u"Africa"
    }, 
    u"CF": {
        u"region": u"Middle Africa", 
        u"name": u"Central African Republic", 
        u"continent": u"Africa"
    }, 
    u"CD": {
        u"region": u"Middle Africa", 
        u"aliases": [
            u"Democratic Republic of Congo"
        ], 
        u"name": u"Democratic Republic of the Congo", 
        u"continent": u"Africa"
    }, 
    u"CZ": {
        u"region": u"Eastern Europe", 
        u"name": u"Czech Republic", 
        u"continent": u"Europe"
    }, 
    u"CY": {
        u"region": u"Western Asia", 
        u"name": u"Cyprus", 
        u"continent": u"Asia"
    }, 
    u"CX": {
        u"region": u"South-Eastern Asia", 
        u"name": u"Christmas Island", 
        u"continent": u"Asia"
    }, 
    u"CR": {
        u"region": u"Central America", 
        u"name": u"Costa Rica", 
        u"continent": u"South America"
    }, 
    u"CP": {
        u"region": u"Central America", 
        u"name": u"Clipperton Island", 
        u"continent": u"South America"
    }, 
    u"VNVN": {
        u"region": u"South-Eastern Asia", 
        u"name": u"South Vietnam", 
        u"continent": u"Asia"
    }, 
    u"CV": {
        u"region": u"Western Africa", 
        u"name": u"Cape Verde", 
        u"continent": u"Africa"
    }, 
    u"CU": {
        u"region": u"Caribbean", 
        u"name": u"Cuba", 
        u"continent": u"South America"
    }, 
    u"AO-CAB": {
        u"region": u"Middle Africa", 
        u"name": u"Cabinda", 
        u"continent": u"Africa"
    }, 
    u"GBKN": {
        u"region": u"Caribbean", 
        u"name": u"Saint Christopher-Nevis-Anguilla", 
        u"continent": u"South America"
    }, 
    u"LKLK": {
        u"region": u"Southern Asia", 
        u"name": u"Ceylon", 
        u"continent": u"Asia"
    }, 
    u"CSHH": {
        u"region": u"Eastern Europe", 
        u"name": u"Czechoslovakia", 
        u"continent": u"Europe"
    }, 
    u"AE-AZ": {
        u"region": u"Western Asia", 
        u"name": u"Abu Dhabi", 
        u"continent": u"Asia"
    }, 
    u"SO-SO": {
        u"region": u"Eastern Africa", 
        u"name": u"Somaliland", 
        u"continent": u"Africa"
    }, 
    u"AE-AJ": {
        u"region": u"Western Asia", 
        u"name": u"Ajman", 
        u"continent": u"Asia"
    }, 
    u"VA": {
        u"region": u"Southern Europe", 
        u"aliases": [
            u"Holy See (Vatican City State)"
        ], 
        u"name": u"Vatican City", 
        u"continent": u"Europe"
    }, 
    u"VC": {
        u"region": u"Caribbean", 
        u"name": u"Saint Vincent and the Grenadines", 
        u"continent": u"South America"
    }, 
    u"VE": {
        u"region": u"Southern America", 
        u"name": u"Venezuela", 
        u"continent": u"South America"
    }, 
    u"VG": {
        u"region": u"Caribbean", 
        u"name": u"British Virgin Islands", 
        u"continent": u"South America"
    }, 
    u"IQ": {
        u"region": u"Western Asia", 
        u"name": u"Iraq", 
        u"continent": u"Asia"
    }, 
    u"VI": {
        u"region": u"Caribbean", 
        u"aliases": [
            u"US Virgin Islands"
        ], 
        u"name": u"United States Virgin Islands", 
        u"continent": u"South America"
    }, 
    u"IS": {
        u"region": u"Northern Europe", 
        u"name": u"Iceland", 
        u"continent": u"Europe"
    }, 
    u"IR": {
        u"region": u"Southern Asia", 
        u"name": u"Iran", 
        u"continent": u"Asia"
    }, 
    u"IT": {
        u"region": u"Southern Europe", 
        u"name": u"Italy", 
        u"continent": u"Europe"
    }, 
    u"VN": {
        u"region": u"South-Eastern Asia", 
        u"name": u"Vietnam", 
        u"continent": u"Asia"
    }, 
    u"IM": {
        u"region": u"Northern Europe", 
        u"name": u"Isle of Man", 
        u"continent": u"Europe"
    }, 
    u"IL": {
        u"region": u"Western Asia", 
        u"name": u"Israel", 
        u"continent": u"Asia"
    }, 
    u"IO": {
        u"region": u"Southern Asia", 
        u"name": u"British Indian Ocean Territory", 
        u"continent": u"Asia"
    }, 
    u"NHVU-TF": {
        u"region": u"Melanesia", 
        u"name": u"Tafea", 
        u"continent": u"Oceania"
    }, 
    u"IC": {
        u"region": u"Northern Africa", 
        u"name": u"Canary Islands", 
        u"continent": u"Africa"
    }, 
    u"IE": {
        u"region": u"Northern Europe", 
        u"name": u"Ireland", 
        u"continent": u"Europe"
    }, 
    u"ID": {
        u"region": u"South-Eastern Asia", 
        u"name": u"Indonesia", 
        u"continent": u"Asia"
    }, 
    u"NHVU-TN": {
        u"region": u"Melanesia", 
        u"name": u"Tanna", 
        u"continent": u"Oceania"
    }, 
    u"GB-ENG": {
        u"region": u"Northern Europe", 
        u"name": u"England", 
        u"continent": u"Europe"
    }, 
    u"GG-AL": {
        u"region": u"Northern Europe", 
        u"name": u"Alderney", 
        u"continent": u"Europe"
    }, 
    u"BD": {
        u"region": u"Southern Asia", 
        u"name": u"Bangladesh", 
        u"continent": u"Asia"
    }, 
    u"BE": {
        u"region": u"Western Europe", 
        u"name": u"Belgium", 
        u"continent": u"Europe"
    }, 
    u"BF": {
        u"region": u"Western Africa", 
        u"name": u"Burkina Faso", 
        u"continent": u"Africa"
    }, 
    u"BG": {
        u"region": u"Eastern Europe", 
        u"name": u"Bulgaria", 
        u"continent": u"Europe"
    }, 
    u"BA": {
        u"region": u"Southern Europe", 
        u"name": u"Bosnia and Herzegovina", 
        u"continent": u"Europe"
    }, 
    u"BB": {
        u"region": u"Caribbean", 
        u"name": u"Barbados", 
        u"continent": u"South America"
    }, 
    u"AE-SH": {
        u"region": u"Western Asia", 
        u"name": u"Sharjah", 
        u"continent": u"Asia"
    }, 
    u"BL": {
        u"region": u"Caribbean", 
        u"name": u"Saint Barthélemy", 
        u"continent": u"South America"
    }, 
    u"BM": {
        u"region": u"Northern America", 
        u"name": u"Bermuda", 
        u"continent": u"North America"
    }, 
    u"BN": {
        u"region": u"South-Eastern Asia", 
        u"aliases": [
            u"Brunei Darussalam"
        ], 
        u"name": u"Brunei", 
        u"continent": u"Asia"
    }, 
    u"BO": {
        u"region": u"Southern America", 
        u"name": u"Bolivia", 
        u"continent": u"South America"
    }, 
    u"BH": {
        u"region": u"Western Asia", 
        u"name": u"Bahrain", 
        u"continent": u"Asia"
    }, 
    u"BI": {
        u"region": u"Eastern Africa", 
        u"name": u"Burundi", 
        u"continent": u"Africa"
    }, 
    u"BJ": {
        u"region": u"Western Africa", 
        u"name": u"Benin", 
        u"continent": u"Africa"
    }, 
    u"BT": {
        u"region": u"Southern Asia", 
        u"name": u"Bhutan", 
        u"continent": u"Asia"
    }, 
    u"BV": {
        u"region": u"Antarctica", 
        u"name": u"Bouvet Island", 
        u"continent": u"Antarctica"
    }, 
    u"BW": {
        u"region": u"Southern Africa", 
        u"name": u"Botswana", 
        u"continent": u"Africa"
    }, 
    u"BQ": {
        u"region": u"Caribbean", 
        u"name": u"Bonaire, Sint Eustatius and Saba", 
        u"continent": u"South America"
    }, 
    u"BR": {
        u"region": u"Southern America", 
        u"name": u"Brazil", 
        u"continent": u"South America"
    }, 
    u"BS": {
        u"region": u"Caribbean", 
        u"aliases": [
            u"The Bahamas"
        ], 
        u"name": u"Bahamas", 
        u"continent": u"South America"
    }, 
    u"BY": {
        u"region": u"Eastern Europe", 
        u"name": u"Belarus", 
        u"continent": u"Europe"
    }, 
    u"BZ": {
        u"region": u"Central America", 
        u"name": u"Belize", 
        u"continent": u"South America"
    }, 
    u"DYBJ": {
        u"region": u"Western Africa", 
        u"name": u"Dahomey", 
        u"continent": u"Africa"
    }, 
    u"IN-JK": {
        u"region": u"Southern Asia", 
        u"name": u"Jammu and Kashmir", 
        u"continent": u"Asia"
    }, 
    u"GG-SA": {
        u"region": u"Northern Europe", 
        u"name": u"Sark", 
        u"continent": u"Europe"
    }, 
    u"CY-NC": {
        u"region": u"Western Asia", 
        u"name": u"Northern Cyprus", 
        u"continent": u"Asia"
    }, 
    u"ML-AZ": {
        u"region": u"Western Africa", 
        u"name": u"Azawad", 
        u"continent": u"Africa"
    }, 
    u"OM": {
        u"region": u"Western Asia", 
        u"name": u"Oman", 
        u"continent": u"Asia"
    }, 
    u"DDDE": {
        u"region": u"Western Europe", 
        u"name": u"East Germany", 
        u"continent": u"Europe"
    }, 
    u"PCHH": {
        u"region": u"Micronesia", 
        u"name": u"Pacific Islands", 
        u"continent": u"Oceania"
    }, 
    u"HR": {
        u"region": u"Southern Europe", 
        u"name": u"Croatia", 
        u"continent": u"Europe"
    }, 
    u"AC": {
        u"region": u"Western Africa", 
        u"name": u"Ascension", 
        u"continent": u"Africa"
    }, 
    u"HT": {
        u"region": u"Caribbean", 
        u"name": u"Haiti", 
        u"continent": u"South America"
    }, 
    u"FQHH": {
        u"region": u"Antarctica", 
        u"name": u"French Southern and Antarctic Territories", 
        u"continent": u"Antarctica"
    }, 
    u"HK": {
        u"region": u"Eastern Asia", 
        u"name": u"Hong Kong", 
        u"continent": u"Asia"
    }, 
    u"HN": {
        u"region": u"Central America", 
        u"name": u"Honduras", 
        u"continent": u"South America"
    }, 
    u"HM": {
        u"region": u"Antarctica", 
        u"name": u"Heard Island and McDonald Islands", 
        u"continent": u"Antarctica"
    }, 
    u"PUUM": {
        u"region": u"Polynesia", 
        u"name": u"United States Miscellaneous Pacific Islands", 
        u"continent": u"Oceania"
    }, 
    u"GETV": {
        u"region": u"Polynesia", 
        u"name": u"Ellice Islands", 
        u"continent": u"Oceania"
    }, 
    u"ZA-VE": {
        u"region": u"Southern Africa", 
        u"name": u"Venda", 
        u"continent": u"Africa"
    }, 
    u"GBAE": {
        u"region": u"Western Asia", 
        u"name": u"Trucial States", 
        u"continent": u"Asia"
    }, 
    u"KHKA": {
        u"region": u"South-Eastern Asia", 
        u"name": u"Khmer Republic", 
        u"continent": u"Asia"
    }, 
    u"UY": {
        u"region": u"Southern America", 
        u"name": u"Uruguay", 
        u"continent": u"South America"
    }, 
    u"UZ": {
        u"region": u"Central Asia", 
        u"name": u"Uzbekistan", 
        u"continent": u"Asia"
    }, 
    u"US": {
        u"region": u"Northern America", 
        u"aliases": [
            u"USA"
        ], 
        u"name": u"United States", 
        u"continent": u"North America"
    }, 
    u"UM": {
        u"region": u"Polynesia", 
        u"name": u"United States Minor Outlying Islands", 
        u"continent": u"Oceania"
    }, 
    u"UK": {
        u"region": u"Northern Europe", 
        u"aliases": [
            u"UK"
        ], 
        u"name": u"United Kingdom", 
        u"continent": u"Europe"
    }, 
    u"AU": {
        u"region": u"Australia and New Zealand", 
        u"name": u"Australia", 
        u"continent": u"Oceania"
    }, 
    u"UG": {
        u"region": u"Eastern Africa", 
        u"name": u"Uganda", 
        u"continent": u"Africa"
    }, 
    u"UA": {
        u"region": u"Eastern Europe", 
        u"name": u"Ukraine", 
        u"continent": u"Europe"
    }, 
    u"RHZW-RH": {
        u"region": u"Eastern Africa", 
        u"name": u"Rhodesia", 
        u"continent": u"Africa"
    }, 
    u"NI": {
        u"region": u"Central America", 
        u"name": u"Nicaragua", 
        u"continent": u"South America"
    }, 
    u"NL": {
        u"region": u"Western Europe", 
        u"name": u"Netherlands", 
        u"continent": u"Europe"
    }, 
    u"NO": {
        u"region": u"Northern Europe", 
        u"name": u"Norway", 
        u"continent": u"Europe"
    }, 
    u"NA": {
        u"region": u"Southern Africa", 
        u"name": u"Namibia", 
        u"continent": u"Africa"
    }, 
    u"NC": {
        u"region": u"Melanesia", 
        u"name": u"New Caledonia", 
        u"continent": u"Oceania"
    }, 
    u"NE": {
        u"region": u"Western Africa", 
        u"name": u"Niger", 
        u"continent": u"Africa"
    }, 
    u"NF": {
        u"region": u"Australia and New Zealand", 
        u"name": u"Norfolk Island", 
        u"continent": u"Oceania"
    }, 
    u"NG": {
        u"region": u"Western Africa", 
        u"name": u"Nigeria", 
        u"continent": u"Africa"
    }, 
    u"NZ": {
        u"region": u"Australia and New Zealand", 
        u"name": u"New Zealand", 
        u"continent": u"Oceania"
    }, 
    u"NP": {
        u"region": u"Southern Asia", 
        u"name": u"Nepal", 
        u"continent": u"Asia"
    }, 
    u"AZ-NK": {
        u"region": u"Western Asia", 
        u"name": u"Nagorno-Karabakh", 
        u"continent": u"Asia"
    }, 
    u"NU": {
        u"region": u"Polynesia", 
        u"name": u"Niue", 
        u"continent": u"Oceania"
    }, 
    u"HU": {
        u"region": u"Eastern Europe", 
        u"name": u"Hungary", 
        u"continent": u"Europe"
    }, 
    u"RHZW": {
        u"region": u"Eastern Africa", 
        u"name": u"Southern Rhodesia", 
        u"continent": u"Africa"
    }, 
    u"AE-DU": {
        u"region": u"Western Asia", 
        u"name": u"Dubai", 
        u"continent": u"Asia"
    }, 
    u"GB-SCT": {
        u"region": u"Northern Europe", 
        u"name": u"Scotland", 
        u"continent": u"Europe"
    }, 
    u"TZ": {
        u"region": u"Eastern Africa", 
        u"name": u"Tanzania", 
        u"continent": u"Africa"
    }, 
    u"TV": {
        u"region": u"Polynesia", 
        u"name": u"Tuvalu", 
        u"continent": u"Oceania"
    }, 
    u"TW": {
        u"region": u"Eastern Asia", 
        u"name": u"Taiwan", 
        u"continent": u"Asia"
    }, 
    u"TT": {
        u"region": u"Caribbean", 
        u"name": u"Trinidad and Tobago", 
        u"continent": u"South America"
    }, 
    u"CL": {
        u"region": u"Southern America", 
        u"name": u"Chile", 
        u"continent": u"South America"
    }, 
    u"TR": {
        u"region": u"Western Asia", 
        u"name": u"Turkey", 
        u"continent": u"Asia"
    }, 
    u"TN": {
        u"region": u"Northern Africa", 
        u"name": u"Tunisia", 
        u"continent": u"Africa"
    }, 
    u"TO": {
        u"region": u"Polynesia", 
        u"name": u"Tonga", 
        u"continent": u"Oceania"
    }, 
    u"TL": {
        u"region": u"South-Eastern Asia", 
        u"name": u"Timor-Leste", 
        u"continent": u"Asia"
    }, 
    u"TM": {
        u"region": u"Central Asia", 
        u"name": u"Turkmenistan", 
        u"continent": u"Asia"
    }, 
    u"TJ": {
        u"region": u"Central Asia", 
        u"name": u"Tajikistan", 
        u"continent": u"Asia"
    }, 
    u"TK": {
        u"region": u"Polynesia", 
        u"name": u"Tokelau", 
        u"continent": u"Oceania"
    }, 
    u"TH": {
        u"region": u"South-Eastern Asia", 
        u"name": u"Thailand", 
        u"continent": u"Asia"
    }, 
    u"TF": {
        u"region": u"Antarctica", 
        u"name": u"French Southern Territories", 
        u"continent": u"Antarctica"
    }, 
    u"TG": {
        u"region": u"Western Africa", 
        u"name": u"Togo", 
        u"continent": u"Africa"
    }, 
    u"TD": {
        u"region": u"Middle Africa", 
        u"name": u"Chad", 
        u"continent": u"Africa"
    }, 
    u"TC": {
        u"region": u"Caribbean", 
        u"name": u"Turks and Caicos Islands", 
        u"continent": u"South America"
    }, 
    u"TA": {
        u"region": u"Western Africa", 
        u"name": u"Tristan da Cunha", 
        u"continent": u"Africa"
    }, 
    u"GE-SK": {
        u"region": u"Western Asia", 
        u"name": u"South Ossetia", 
        u"continent": u"Asia"
    }, 
    u"AE": {
        u"region": u"Western Asia", 
        u"name": u"United Arab Emirates", 
        u"continent": u"Asia"
    }, 
    u"AD": {
        u"region": u"Southern Europe", 
        u"name": u"Andorra", 
        u"continent": u"Europe"
    }, 
    u"AG": {
        u"region": u"Caribbean", 
        u"name": u"Antigua and Barbuda", 
        u"continent": u"South America"
    }, 
    u"AF": {
        u"region": u"Southern Asia", 
        u"name": u"Afghanistan", 
        u"continent": u"Asia"
    }, 
    u"AI": {
        u"region": u"Caribbean", 
        u"name": u"Anguilla", 
        u"continent": u"South America"
    }, 
    u"AM": {
        u"region": u"Western Asia", 
        u"name": u"Armenia", 
        u"continent": u"Asia"
    }, 
    u"AL": {
        u"region": u"Southern Europe", 
        u"name": u"Albania", 
        u"continent": u"Europe"
    }, 
    u"AO": {
        u"region": u"Middle Africa", 
        u"name": u"Angola", 
        u"continent": u"Africa"
    }, 
    u"AQ": {
        u"region": u"Antarctica", 
        u"name": u"Antarctica", 
        u"continent": u"Antarctica"
    }, 
    u"AS": {
        u"region": u"Polynesia", 
        u"name": u"American Samoa", 
        u"continent": u"Oceania"
    }, 
    u"AR": {
        u"region": u"Southern America", 
        u"name": u"Argentina", 
        u"continent": u"South America"
    }, 
    u"EGEG": {
        u"region": u"Northern Africa", 
        u"name": u"United Arab Republic", 
        u"continent": u"Africa"
    }, 
    u"AT": {
        u"region": u"Western Europe", 
        u"name": u"Austria", 
        u"continent": u"Europe"
    }, 
    u"AW": {
        u"region": u"Caribbean", 
        u"name": u"Aruba", 
        u"continent": u"South America"
    }, 
    u"AX": {
        u"region": u"Northern Europe", 
        u"name": u"Åland Islands", 
        u"continent": u"Europe"
    }, 
    u"AZ": {
        u"region": u"Western Asia", 
        u"name": u"Azerbaijan", 
        u"continent": u"Asia"
    }, 
    u"YDYE": {
        u"region": u"Western Asia", 
        u"name": u"South Yemen", 
        u"continent": u"Asia"
    }
}

# See http://en.wikipedia.org/wiki/WGS-84
EARTH_RADIUS = 6378137

def crosses_dateline(west, east):
    return west['lng'] > east['lng']

def get_area(southwest, northeast):
    def radians(point):
        return {
            'lat': math.radians(point['lat']),
            'lng': math.radians(point['lng'])
        }
    if crosses_dateline(southwest, northeast):
        northeast['lng'] += 360
    southwest = radians(southwest)
    northeast = radians(northeast)
    return math.pow(EARTH_RADIUS, 2) * abs(
        math.sin(southwest['lat']) - math.sin(northeast['lat'])
    ) * abs(southwest['lng'] - northeast['lng']);

def get_country(code_or_name):
    if isinstance(code_or_name, bytes):
        code_or_name = code_or_name.decode('utf-8')
    if len(code_or_name) == 2:
        code_or_name = code_or_name.upper()
        return COUNTRIES[code_or_name] if code_or_name in COUNTRIES else {}
    else:
        for code, country in COUNTRIES.items():
            if code_or_name == country['name'] or (
                'aliases' in country and code_or_name in country['aliases']
            ):
                return country
    return {}

def get_country_name(country_code):
    country_code = country_code.upper()
    return COUNTRIES[country_code]['name'] if country_code in COUNTRIES else ''

def normalize_country_name(country_name):
    if isinstance(country_name, bytes):
        country_name = country_name.decode('utf-8')
    name = None
    for code, country in COUNTRIES.items():
        if country_name == country['name'] or (
            'aliases' in country and country_name in country['aliases']
        ):
            name = country['name']
            break
    return name

def split_geoname(geoname):
    if isinstance(geoname, bytes):
        geoname = geoname.decode('utf-8')
    countries = [
        u'Bonaire, Sint Eustatius and Saba',
        u'Saint Helena, Ascension and Tristan da Cunha'
    ]
    for country in countries:
        if geoname.endswith(country):
            geoname = geoname.replace(country, country.replace(', ', '; '))
    split = geoname.split(', ')
    for country in countries:
        if geoname.endswith(country.replace(', ', '; ')):
            split[-1] = country
    return split
