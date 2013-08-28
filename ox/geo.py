# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2008

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
    print 'ox/geo.py updated'

COUNTRIES = {
    "GE-AB": {
        "region": "Western Asia", 
        "name": "Abkhazia", 
        "continent": "Asia"
    }, 
    "CW": {
        "region": "Caribbean", 
        "name": "Curaçao", 
        "continent": "South America"
    }, 
    "GW": {
        "region": "Western Africa", 
        "name": "Guinea-Bissau", 
        "continent": "Africa"
    }, 
    "GU": {
        "region": "Micronesia", 
        "name": "Guam", 
        "continent": "Oceania"
    }, 
    "GT": {
        "region": "Central America", 
        "name": "Guatemala", 
        "continent": "South America"
    }, 
    "GS": {
        "region": "Antarctica", 
        "name": "South Georgia and the South Sandwich Islands", 
        "continent": "Antarctica"
    }, 
    "GR": {
        "region": "Southern Europe", 
        "name": "Greece", 
        "continent": "Europe"
    }, 
    "GQ": {
        "region": "Middle Africa", 
        "name": "Equatorial Guinea", 
        "continent": "Africa"
    }, 
    "GP": {
        "region": "Caribbean", 
        "name": "Guadeloupe", 
        "continent": "South America"
    }, 
    "KAKH": {
        "region": "South-Eastern Asia", 
        "name": "Kampuchea", 
        "continent": "Asia"
    }, 
    "GY": {
        "region": "Southern America", 
        "name": "Guyana", 
        "continent": "South America"
    }, 
    "GG": {
        "region": "Northern Europe", 
        "name": "Guernsey", 
        "continent": "Europe"
    }, 
    "BYAA": {
        "region": "Eastern Europe", 
        "name": "Byelorussian Soviet Socialist Republic", 
        "continent": "Europe"
    }, 
    "GE": {
        "region": "Western Asia", 
        "name": "Georgia", 
        "continent": "Asia"
    }, 
    "GD": {
        "region": "Caribbean", 
        "name": "Grenada", 
        "continent": "South America"
    }, 
    "GB": {
        "region": "Northern Europe", 
        "aliases": [
            "UK"
        ], 
        "name": "United Kingdom", 
        "continent": "Europe"
    }, 
    "GA": {
        "region": "Middle Africa", 
        "name": "Gabon", 
        "continent": "Africa"
    }, 
    "YEYE": {
        "region": "Western Asia", 
        "name": "North Yemen", 
        "continent": "Asia"
    }, 
    "GN": {
        "region": "Western Africa", 
        "name": "Guinea", 
        "continent": "Africa"
    }, 
    "GM": {
        "region": "Western Africa", 
        "aliases": [
            "The Gambia"
        ], 
        "name": "Gambia", 
        "continent": "Africa"
    }, 
    "GL": {
        "region": "Northern America", 
        "name": "Greenland", 
        "continent": "North America"
    }, 
    "GI": {
        "region": "Southern Europe", 
        "name": "Gibraltar", 
        "continent": "Europe"
    }, 
    "GH": {
        "region": "Western Africa", 
        "name": "Ghana", 
        "continent": "Africa"
    }, 
    "SUHH": {
        "region": "Eastern Europe", 
        "name": "Soviet Union", 
        "continent": "Europe"
    }, 
    "JTUM": {
        "region": "Polynesia", 
        "name": "Johnston Island", 
        "continent": "Oceania"
    }, 
    "EH": {
        "region": "Northern Africa", 
        "aliases": [
            "Western Sahara"
        ], 
        "name": "Sahrawi", 
        "continent": "Africa"
    }, 
    "ANHH": {
        "region": "Caribbean", 
        "name": "Netherlands Antilles", 
        "continent": "South America"
    }, 
    "AE-RK": {
        "region": "Western Asia", 
        "name": "Ras al-Khaimah", 
        "continent": "Asia"
    }, 
    "ZA": {
        "region": "Southern Africa", 
        "name": "South Africa", 
        "continent": "Africa"
    }, 
    "GB-WLS": {
        "region": "Northern Europe", 
        "name": "Wales", 
        "continent": "Europe"
    }, 
    "ZW": {
        "region": "Eastern Africa", 
        "name": "Zimbabwe", 
        "continent": "Africa"
    }, 
    "YUCS": {
        "region": "Southern Europe", 
        "aliases": [
            "Federal Republic of Yugoslavia"
        ], 
        "name": "Yugoslavia", 
        "continent": "Europe"
    }, 
    "ME": {
        "region": "Southern Europe", 
        "name": "Montenegro", 
        "continent": "Europe"
    }, 
    "MD": {
        "region": "Eastern Europe", 
        "name": "Moldova", 
        "continent": "Europe"
    }, 
    "MG": {
        "region": "Eastern Africa", 
        "name": "Madagascar", 
        "continent": "Africa"
    }, 
    "MF": {
        "region": "Caribbean", 
        "aliases": [
            "Saint Martin (French part)"
        ], 
        "name": "Saint Martin", 
        "continent": "South America"
    }, 
    "MA": {
        "region": "Northern Africa", 
        "name": "Morocco", 
        "continent": "Africa"
    }, 
    "MC": {
        "region": "Western Europe", 
        "name": "Monaco", 
        "continent": "Europe"
    }, 
    "MM": {
        "region": "South-Eastern Asia", 
        "aliases": [
            "Burma"
        ], 
        "name": "Myanmar", 
        "continent": "Asia"
    }, 
    "ML": {
        "region": "Western Africa", 
        "name": "Mali", 
        "continent": "Africa"
    }, 
    "MO": {
        "region": "Eastern Asia", 
        "aliases": [
            "Macao"
        ], 
        "name": "Macau", 
        "continent": "Asia"
    }, 
    "MN": {
        "region": "Eastern Asia", 
        "name": "Mongolia", 
        "continent": "Asia"
    }, 
    "AE-UQ": {
        "region": "Western Asia", 
        "name": "Umm al-Quwain", 
        "continent": "Asia"
    }, 
    "MH": {
        "region": "Micronesia", 
        "name": "Marshall Islands", 
        "continent": "Oceania"
    }, 
    "MK": {
        "region": "Southern Europe", 
        "aliases": [
            "Former Yugoslav Republic of Macedonia", 
            "Republic of Macedonia"
        ], 
        "name": "Macedonia", 
        "continent": "Europe"
    }, 
    "MU": {
        "region": "Eastern Africa", 
        "name": "Mauritius", 
        "continent": "Africa"
    }, 
    "MT": {
        "region": "Southern Europe", 
        "name": "Malta", 
        "continent": "Europe"
    }, 
    "MW": {
        "region": "Eastern Africa", 
        "name": "Malawi", 
        "continent": "Africa"
    }, 
    "MV": {
        "region": "Southern Asia", 
        "name": "Maldives", 
        "continent": "Asia"
    }, 
    "MQ": {
        "region": "Caribbean", 
        "name": "Martinique", 
        "continent": "South America"
    }, 
    "MP": {
        "region": "Micronesia", 
        "name": "Northern Mariana Islands", 
        "continent": "Oceania"
    }, 
    "MS": {
        "region": "Caribbean", 
        "name": "Montserrat", 
        "continent": "South America"
    }, 
    "MR": {
        "region": "Western Africa", 
        "name": "Mauritania", 
        "continent": "Africa"
    }, 
    "MY": {
        "region": "South-Eastern Asia", 
        "name": "Malaysia", 
        "continent": "Asia"
    }, 
    "MX": {
        "region": "Central America", 
        "name": "Mexico", 
        "continent": "South America"
    }, 
    "MZ": {
        "region": "Eastern Africa", 
        "name": "Mozambique", 
        "continent": "Africa"
    }, 
    "FR": {
        "region": "Western Europe", 
        "name": "France", 
        "continent": "Europe"
    }, 
    "ZRCD": {
        "region": "Middle Africa", 
        "name": "Zaire", 
        "continent": "Africa"
    }, 
    "ZA-BO": {
        "region": "Southern Africa", 
        "name": "Bophuthatswana", 
        "continent": "Africa"
    }, 
    "FI": {
        "region": "Northern Europe", 
        "name": "Finland", 
        "continent": "Europe"
    }, 
    "FJ": {
        "region": "Melanesia", 
        "name": "Fiji", 
        "continent": "Oceania"
    }, 
    "FK": {
        "region": "Southern America", 
        "name": "Falkland Islands", 
        "continent": "South America"
    }, 
    "FM": {
        "region": "Micronesia", 
        "aliases": [
            "Federated States of Micronesia"
        ], 
        "name": "Micronesia", 
        "continent": "Oceania"
    }, 
    "FO": {
        "region": "Northern Europe", 
        "name": "Faroe Islands", 
        "continent": "Europe"
    }, 
    "SITH": {
        "region": "South-Eastern Asia", 
        "name": "Siam", 
        "continent": "Asia"
    }, 
    "NHVU": {
        "region": "Melanesia", 
        "name": "New Hebrides", 
        "continent": "Oceania"
    }, 
    "AR-AQ": {
        "region": "Antarctica", 
        "name": "Argentine Antarctica", 
        "continent": "Antarctica"
    }, 
    "FR-AQ": {
        "region": "Antarctica", 
        "name": "Adélie Land", 
        "continent": "Antarctica"
    }, 
    "NHVU-VE": {
        "region": "Melanesia", 
        "name": "Vemerana", 
        "continent": "Oceania"
    }, 
    "SZ": {
        "region": "Southern Africa", 
        "name": "Swaziland", 
        "continent": "Africa"
    }, 
    "SY": {
        "region": "Western Asia", 
        "name": "Syria", 
        "continent": "Asia"
    }, 
    "SX": {
        "region": "Caribbean", 
        "name": "Sint Maarten", 
        "continent": "South America"
    }, 
    "SS": {
        "region": "Northern Africa", 
        "name": "South Sudan", 
        "continent": "Africa"
    }, 
    "SR": {
        "region": "Southern America", 
        "name": "Suriname", 
        "continent": "South America"
    }, 
    "SV": {
        "region": "Central America", 
        "name": "El Salvador", 
        "continent": "South America"
    }, 
    "ST": {
        "region": "Middle Africa", 
        "aliases": [
            "Sao Tome and Principe"
        ], 
        "name": "São Tomé and Príncipe", 
        "continent": "Africa"
    }, 
    "SK": {
        "region": "Eastern Europe", 
        "name": "Slovakia", 
        "continent": "Europe"
    }, 
    "SJ": {
        "region": "Northern Europe", 
        "name": "Svalbard and Jan Mayen", 
        "continent": "Europe"
    }, 
    "SI": {
        "region": "Southern Europe", 
        "name": "Slovenia", 
        "continent": "Europe"
    }, 
    "SH": {
        "region": "Western Africa", 
        "aliases": [
            "Saint Helena"
        ], 
        "name": "Saint Helena, Ascension and Tristan da Cunha", 
        "continent": "Africa"
    }, 
    "SO": {
        "region": "Eastern Africa", 
        "name": "Somalia", 
        "continent": "Africa"
    }, 
    "SN": {
        "region": "Western Africa", 
        "name": "Senegal", 
        "continent": "Africa"
    }, 
    "SM": {
        "region": "Southern Europe", 
        "name": "San Marino", 
        "continent": "Europe"
    }, 
    "SL": {
        "region": "Western Africa", 
        "name": "Sierra Leone", 
        "continent": "Africa"
    }, 
    "SC": {
        "region": "Eastern Africa", 
        "name": "Seychelles", 
        "continent": "Africa"
    }, 
    "SB": {
        "region": "Melanesia", 
        "name": "Solomon Islands", 
        "continent": "Oceania"
    }, 
    "SA": {
        "region": "Western Asia", 
        "name": "Saudi Arabia", 
        "continent": "Asia"
    }, 
    "SG": {
        "region": "South-Eastern Asia", 
        "name": "Singapore", 
        "continent": "Asia"
    }, 
    "SE": {
        "region": "Northern Europe", 
        "name": "Sweden", 
        "continent": "Europe"
    }, 
    "SD": {
        "region": "Northern Africa", 
        "name": "Sudan", 
        "continent": "Africa"
    }, 
    "YE": {
        "region": "Western Asia", 
        "name": "Yemen", 
        "continent": "Asia"
    }, 
    "YT": {
        "region": "Eastern Africa", 
        "name": "Mayotte", 
        "continent": "Africa"
    }, 
    "LB": {
        "region": "Western Asia", 
        "name": "Lebanon", 
        "continent": "Asia"
    }, 
    "LC": {
        "region": "Caribbean", 
        "name": "Saint Lucia", 
        "continent": "South America"
    }, 
    "LA": {
        "region": "South-Eastern Asia", 
        "name": "Laos", 
        "continent": "Asia"
    }, 
    "ZA-TR": {
        "region": "Southern Africa", 
        "name": "Transkei", 
        "continent": "Africa"
    }, 
    "LK": {
        "region": "Southern Asia", 
        "name": "Sri Lanka", 
        "continent": "Asia"
    }, 
    "LI": {
        "region": "Western Europe", 
        "name": "Liechtenstein", 
        "continent": "Europe"
    }, 
    "LV": {
        "region": "Northern Europe", 
        "name": "Latvia", 
        "continent": "Europe"
    }, 
    "LT": {
        "region": "Northern Europe", 
        "name": "Lithuania", 
        "continent": "Europe"
    }, 
    "LU": {
        "region": "Western Europe", 
        "name": "Luxembourg", 
        "continent": "Europe"
    }, 
    "PG-NSA": {
        "region": "Melanesia", 
        "name": "Bougainville", 
        "continent": "Oceania"
    }, 
    "LS": {
        "region": "Southern Africa", 
        "name": "Lesotho", 
        "continent": "Africa"
    }, 
    "LY": {
        "region": "Northern Africa", 
        "name": "Libya", 
        "continent": "Africa"
    }, 
    "DEDE": {
        "region": "Western Europe", 
        "name": "West Germany", 
        "continent": "Europe"
    }, 
    "GF": {
        "region": "Southern America", 
        "name": "French Guiana", 
        "continent": "South America"
    }, 
    "AU-CS": {
        "region": "Australia and New Zealand", 
        "name": "Coral Sea Islands", 
        "continent": "Oceania"
    }, 
    "WKUM": {
        "region": "Micronesia", 
        "name": "Wake Island", 
        "continent": "Oceania"
    }, 
    "UAUA": {
        "region": "Eastern Europe", 
        "name": "Ukrainian Soviet Socialist Republic", 
        "continent": "Europe"
    }, 
    "CTKI": {
        "region": "Micronesia", 
        "name": "Canton and Enderbury Islands", 
        "continent": "Oceania"
    }, 
    "RU": {
        "region": "Eastern Europe", 
        "name": "Russia", 
        "continent": "Europe"
    }, 
    "RW": {
        "region": "Eastern Africa", 
        "name": "Rwanda", 
        "continent": "Africa"
    }, 
    "RS": {
        "region": "Southern Europe", 
        "name": "Serbia", 
        "continent": "Europe"
    }, 
    "RE": {
        "region": "Eastern Africa", 
        "name": "Réunion", 
        "continent": "Africa"
    }, 
    "LR": {
        "region": "Western Africa", 
        "name": "Liberia", 
        "continent": "Africa"
    }, 
    "RO": {
        "region": "Eastern Europe", 
        "name": "Romania", 
        "continent": "Europe"
    }, 
    "PK-NA": {
        "region": "Southern Asia", 
        "name": "Gilgit-Baltistan", 
        "continent": "Asia"
    }, 
    "GG-HE": {
        "region": "Northern Europe", 
        "name": "Herm", 
        "continent": "Europe"
    }, 
    "CSXX": {
        "region": "Southern Europe", 
        "name": "Serbia and Montenegro", 
        "continent": "Europe"
    }, 
    "AU-AC": {
        "region": "Australia and New Zealand", 
        "name": "Ashmore and Cartier Islands", 
        "continent": "Oceania"
    }, 
    "AU-AQ": {
        "region": "Antarctica", 
        "name": "Australian Antarctic Territory", 
        "continent": "Antarctica"
    }, 
    "TPTL": {
        "region": "South-Eastern Asia", 
        "name": "East Timor", 
        "continent": "Asia"
    }, 
    "GEKI": {
        "region": "Micronesia", 
        "name": "Gilbert Islands", 
        "continent": "Oceania"
    }, 
    "NQAQ": {
        "region": "Antarctica", 
        "name": "Queen Maud Land", 
        "continent": "Antarctica"
    }, 
    "EE": {
        "region": "Northern Europe", 
        "name": "Estonia", 
        "continent": "Europe"
    }, 
    "EG": {
        "region": "Northern Africa", 
        "name": "Egypt", 
        "continent": "Africa"
    }, 
    "EA": {
        "region": "Northern Africa", 
        "name": "Ceuta and Melilla", 
        "continent": "Africa"
    }, 
    "EC": {
        "region": "Southern America", 
        "name": "Ecuador", 
        "continent": "South America"
    }, 
    "EU": {
        "region": "Western Europe", 
        "name": "European Union", 
        "continent": "Europe"
    }, 
    "ET": {
        "region": "Eastern Africa", 
        "name": "Ethiopia", 
        "continent": "Africa"
    }, 
    "ES": {
        "region": "Southern Europe", 
        "name": "Spain", 
        "continent": "Europe"
    }, 
    "ER": {
        "region": "Eastern Africa", 
        "name": "Eritrea", 
        "continent": "Africa"
    }, 
    "RU-CE": {
        "region": "Eastern Europe", 
        "name": "Chechnia", 
        "continent": "Europe"
    }, 
    "VU": {
        "region": "Melanesia", 
        "name": "Vanuatu", 
        "continent": "Oceania"
    }, 
    "AIDJ": {
        "region": "Eastern Africa", 
        "name": "French Afar and Issas", 
        "continent": "Africa"
    }, 
    "IN": {
        "region": "Southern Asia", 
        "name": "India", 
        "continent": "Asia"
    }, 
    "XK": {
        "region": "Southern Europe", 
        "aliases": [
            "Kosova (Kosovo)"
        ], 
        "name": "Kosovo", 
        "continent": "Europe"
    }, 
    "PK-JK": {
        "region": "Southern Asia", 
        "name": "Azad Kashmir", 
        "continent": "Asia"
    }, 
    "BUMM": {
        "region": "South-Eastern Asia", 
        "name": "Burma", 
        "continent": "Asia"
    }, 
    "NR": {
        "region": "Micronesia", 
        "name": "Nauru", 
        "continent": "Oceania"
    }, 
    "KG": {
        "region": "Central Asia", 
        "name": "Kyrgyzstan", 
        "continent": "Asia"
    }, 
    "KE": {
        "region": "Eastern Africa", 
        "name": "Kenya", 
        "continent": "Africa"
    }, 
    "KI": {
        "region": "Micronesia", 
        "name": "Kiribati", 
        "continent": "Oceania"
    }, 
    "KH": {
        "region": "South-Eastern Asia", 
        "name": "Cambodia", 
        "continent": "Asia"
    }, 
    "KN": {
        "region": "Caribbean", 
        "name": "Saint Kitts and Nevis", 
        "continent": "South America"
    }, 
    "KM": {
        "region": "Eastern Africa", 
        "name": "Comoros", 
        "continent": "Africa"
    }, 
    "KR": {
        "region": "Eastern Asia", 
        "name": "South Korea", 
        "continent": "Asia"
    }, 
    "KP": {
        "region": "Eastern Asia", 
        "name": "North Korea", 
        "continent": "Asia"
    }, 
    "KW": {
        "region": "Western Asia", 
        "name": "Kuwait", 
        "continent": "Asia"
    }, 
    "KZ": {
        "region": "Central Asia", 
        "name": "Kazakhstan", 
        "continent": "Asia"
    }, 
    "KY": {
        "region": "Caribbean", 
        "name": "Cayman Islands", 
        "continent": "South America"
    }, 
    "DO": {
        "region": "Caribbean", 
        "name": "Dominican Republic", 
        "continent": "South America"
    }, 
    "DM": {
        "region": "Caribbean", 
        "name": "Dominica", 
        "continent": "South America"
    }, 
    "DJ": {
        "region": "Eastern Africa", 
        "name": "Djibouti", 
        "continent": "Africa"
    }, 
    "DK": {
        "region": "Northern Europe", 
        "name": "Denmark", 
        "continent": "Europe"
    }, 
    "DG": {
        "region": "Southern Asia", 
        "name": "Diego Garcia", 
        "continent": "Asia"
    }, 
    "DE": {
        "region": "Western Europe", 
        "name": "Germany", 
        "continent": "Europe"
    }, 
    "DZ": {
        "region": "Northern Africa", 
        "name": "Algeria", 
        "continent": "Africa"
    }, 
    "BQAQ": {
        "region": "Antarctica", 
        "name": "British Antarctic Territory", 
        "continent": "Antarctica"
    }, 
    "ZA-CI": {
        "region": "Southern Africa", 
        "name": "Ciskei", 
        "continent": "Africa"
    }, 
    "GB-SL": {
        "region": "Northern Europe", 
        "name": "Sealand", 
        "continent": "Europe"
    }, 
    "MD-SN": {
        "region": "Eastern Europe", 
        "name": "Transnistria", 
        "continent": "Europe"
    }, 
    "SKIN": {
        "region": "Southern Asia", 
        "name": "Sikkim", 
        "continent": "Asia"
    }, 
    "FXFR": {
        "region": "Western Europe", 
        "name": "Metropolitan France", 
        "continent": "Europe"
    }, 
    "AE-FU": {
        "region": "Western Asia", 
        "name": "Fujairah", 
        "continent": "Asia"
    }, 
    "QA": {
        "region": "Western Asia", 
        "name": "Qatar", 
        "continent": "Asia"
    }, 
    "WF": {
        "region": "Polynesia", 
        "name": "Wallis and Futuna", 
        "continent": "Oceania"
    }, 
    "JP": {
        "region": "Eastern Asia", 
        "name": "Japan", 
        "continent": "Asia"
    }, 
    "JM": {
        "region": "Caribbean", 
        "name": "Jamaica", 
        "continent": "South America"
    }, 
    "JO": {
        "region": "Western Asia", 
        "name": "Jordan", 
        "continent": "Asia"
    }, 
    "WS": {
        "region": "Polynesia", 
        "name": "Samoa", 
        "continent": "Oceania"
    }, 
    "JE": {
        "region": "Northern Europe", 
        "name": "Jersey", 
        "continent": "Europe"
    }, 
    "KM-M": {
        "region": "Eastern Africa", 
        "name": "Mohéli", 
        "continent": "Africa"
    }, 
    "KM-A": {
        "region": "Eastern Africa", 
        "name": "Anjouan", 
        "continent": "Africa"
    }, 
    "PZPA": {
        "region": "Central America", 
        "name": "Panama Canal Zone", 
        "continent": "South America"
    }, 
    "MIUM": {
        "region": "Polynesia", 
        "name": "Midway Islands", 
        "continent": "Oceania"
    }, 
    "GEHH": {
        "region": "Micronesia", 
        "name": "Gilbert and Ellice Islands", 
        "continent": "Oceania"
    }, 
    "NZ-AQ": {
        "region": "Antarctica", 
        "name": "Ross Dependency", 
        "continent": "Antarctica"
    }, 
    "HVBF": {
        "region": "Western Africa", 
        "name": "Upper Volta", 
        "continent": "Africa"
    }, 
    "GB-AD": {
        "region": "Western Asia", 
        "name": "Akrotiri and Dhekelia", 
        "continent": "Asia"
    }, 
    "UG-RW": {
        "region": "Eastern Africa", 
        "name": "Rwenzururu", 
        "continent": "Africa"
    }, 
    "ZM": {
        "region": "Eastern Africa", 
        "name": "Zambia", 
        "continent": "Africa"
    }, 
    "NTHH": {
        "region": "Western Asia", 
        "name": "Neutral Zone", 
        "continent": "Asia"
    }, 
    "PR": {
        "region": "Caribbean", 
        "name": "Puerto Rico", 
        "continent": "South America"
    }, 
    "PS": {
        "region": "Western Asia", 
        "aliases": [
            "Palestinian Territories", 
            "Occupied Palestinian Territory"
        ], 
        "name": "Palestine", 
        "continent": "Asia"
    }, 
    "PW": {
        "region": "Micronesia", 
        "name": "Palau", 
        "continent": "Oceania"
    }, 
    "PT": {
        "region": "Southern Europe", 
        "name": "Portugal", 
        "continent": "Europe"
    }, 
    "PY": {
        "region": "Southern America", 
        "name": "Paraguay", 
        "continent": "South America"
    }, 
    "PA": {
        "region": "Central America", 
        "name": "Panama", 
        "continent": "South America"
    }, 
    "PF": {
        "region": "Polynesia", 
        "name": "French Polynesia", 
        "continent": "Oceania"
    }, 
    "PG": {
        "region": "Melanesia", 
        "name": "Papua New Guinea", 
        "continent": "Oceania"
    }, 
    "PE": {
        "region": "Southern America", 
        "name": "Peru", 
        "continent": "South America"
    }, 
    "PK": {
        "region": "Southern Asia", 
        "name": "Pakistan", 
        "continent": "Asia"
    }, 
    "PH": {
        "region": "South-Eastern Asia", 
        "name": "Philippines", 
        "continent": "Asia"
    }, 
    "PN": {
        "region": "Polynesia", 
        "aliases": [
            "Pitcairn"
        ], 
        "name": "Pitcairn Islands", 
        "continent": "Oceania"
    }, 
    "PL": {
        "region": "Eastern Europe", 
        "name": "Poland", 
        "continent": "Europe"
    }, 
    "PM": {
        "region": "Northern America", 
        "name": "Saint Pierre and Miquelon", 
        "continent": "North America"
    }, 
    "VDVN": {
        "region": "South-Eastern Asia", 
        "name": "North Vietnam", 
        "continent": "Asia"
    }, 
    "NO-PI": {
        "region": "Antarctica", 
        "name": "Peter I Island", 
        "continent": "Antarctica"
    }, 
    "KOJP": {
        "region": "Eastern Asia", 
        "name": "Korea", 
        "continent": "Asia"
    }, 
    "GBBZ": {
        "region": "Central America", 
        "name": "British Honduras", 
        "continent": "South America"
    }, 
    "RHZW-ZR": {
        "region": "Eastern Africa", 
        "name": "Zimbabwe Rhodesia", 
        "continent": "Africa"
    }, 
    "GB-NIR": {
        "region": "Northern Europe", 
        "name": "Northern Ireland", 
        "continent": "Europe"
    }, 
    "NG-BI": {
        "region": "Western Africa", 
        "name": "Biafra", 
        "continent": "Africa"
    }, 
    "CK": {
        "region": "Polynesia", 
        "name": "Cook Islands", 
        "continent": "Oceania"
    }, 
    "CI": {
        "region": "Western Africa", 
        "aliases": [
            "Ivory Coast"
        ], 
        "name": "Côte d'Ivoire", 
        "continent": "Africa"
    }, 
    "CH": {
        "region": "Western Europe", 
        "name": "Switzerland", 
        "continent": "Europe"
    }, 
    "CO": {
        "region": "Southern America", 
        "name": "Colombia", 
        "continent": "South America"
    }, 
    "CN": {
        "region": "Eastern Asia", 
        "name": "China", 
        "continent": "Asia"
    }, 
    "CM": {
        "region": "Middle Africa", 
        "name": "Cameroon", 
        "continent": "Africa"
    }, 
    "CL-AQ": {
        "region": "Antarctica", 
        "name": "Chilean Antarctic Territory", 
        "continent": "Antarctica"
    }, 
    "CC": {
        "region": "South-Eastern Asia", 
        "aliases": [
            "Cocos (Keeling) Islands"
        ], 
        "name": "Cocos Islands", 
        "continent": "Asia"
    }, 
    "CA": {
        "region": "Northern America", 
        "name": "Canada", 
        "continent": "North America"
    }, 
    "CG": {
        "region": "Middle Africa", 
        "aliases": [
            "Congo"
        ], 
        "name": "Republic of the Congo", 
        "continent": "Africa"
    }, 
    "CF": {
        "region": "Middle Africa", 
        "name": "Central African Republic", 
        "continent": "Africa"
    }, 
    "CD": {
        "region": "Middle Africa", 
        "aliases": [
            "Democratic Republic of Congo"
        ], 
        "name": "Democratic Republic of the Congo", 
        "continent": "Africa"
    }, 
    "CZ": {
        "region": "Eastern Europe", 
        "name": "Czech Republic", 
        "continent": "Europe"
    }, 
    "CY": {
        "region": "Western Asia", 
        "name": "Cyprus", 
        "continent": "Asia"
    }, 
    "CX": {
        "region": "South-Eastern Asia", 
        "name": "Christmas Island", 
        "continent": "Asia"
    }, 
    "CR": {
        "region": "Central America", 
        "name": "Costa Rica", 
        "continent": "South America"
    }, 
    "CP": {
        "region": "Central America", 
        "name": "Clipperton Island", 
        "continent": "South America"
    }, 
    "VNVN": {
        "region": "South-Eastern Asia", 
        "name": "South Vietnam", 
        "continent": "Asia"
    }, 
    "CV": {
        "region": "Western Africa", 
        "name": "Cape Verde", 
        "continent": "Africa"
    }, 
    "CU": {
        "region": "Caribbean", 
        "name": "Cuba", 
        "continent": "South America"
    }, 
    "AO-CAB": {
        "region": "Middle Africa", 
        "name": "Cabinda", 
        "continent": "Africa"
    }, 
    "GBKN": {
        "region": "Caribbean", 
        "name": "Saint Christopher-Nevis-Anguilla", 
        "continent": "South America"
    }, 
    "LKLK": {
        "region": "Southern Asia", 
        "name": "Ceylon", 
        "continent": "Asia"
    }, 
    "CSHH": {
        "region": "Eastern Europe", 
        "name": "Czechoslovakia", 
        "continent": "Europe"
    }, 
    "AE-AZ": {
        "region": "Western Asia", 
        "name": "Abu Dhabi", 
        "continent": "Asia"
    }, 
    "SO-SO": {
        "region": "Eastern Africa", 
        "name": "Somaliland", 
        "continent": "Africa"
    }, 
    "AE-AJ": {
        "region": "Western Asia", 
        "name": "Ajman", 
        "continent": "Asia"
    }, 
    "VA": {
        "region": "Southern Europe", 
        "aliases": [
            "Holy See (Vatican City State)"
        ], 
        "name": "Vatican City", 
        "continent": "Europe"
    }, 
    "VC": {
        "region": "Caribbean", 
        "name": "Saint Vincent and the Grenadines", 
        "continent": "South America"
    }, 
    "VE": {
        "region": "Southern America", 
        "name": "Venezuela", 
        "continent": "South America"
    }, 
    "VG": {
        "region": "Caribbean", 
        "name": "British Virgin Islands", 
        "continent": "South America"
    }, 
    "IQ": {
        "region": "Western Asia", 
        "name": "Iraq", 
        "continent": "Asia"
    }, 
    "VI": {
        "region": "Caribbean", 
        "aliases": [
            "US Virgin Islands"
        ], 
        "name": "United States Virgin Islands", 
        "continent": "South America"
    }, 
    "IS": {
        "region": "Northern Europe", 
        "name": "Iceland", 
        "continent": "Europe"
    }, 
    "IR": {
        "region": "Southern Asia", 
        "name": "Iran", 
        "continent": "Asia"
    }, 
    "IT": {
        "region": "Southern Europe", 
        "name": "Italy", 
        "continent": "Europe"
    }, 
    "VN": {
        "region": "South-Eastern Asia", 
        "name": "Vietnam", 
        "continent": "Asia"
    }, 
    "IM": {
        "region": "Northern Europe", 
        "name": "Isle of Man", 
        "continent": "Europe"
    }, 
    "IL": {
        "region": "Western Asia", 
        "name": "Israel", 
        "continent": "Asia"
    }, 
    "IO": {
        "region": "Southern Asia", 
        "name": "British Indian Ocean Territory", 
        "continent": "Asia"
    }, 
    "NHVU-TF": {
        "region": "Melanesia", 
        "name": "Tafea", 
        "continent": "Oceania"
    }, 
    "IC": {
        "region": "Northern Africa", 
        "name": "Canary Islands", 
        "continent": "Africa"
    }, 
    "IE": {
        "region": "Northern Europe", 
        "name": "Ireland", 
        "continent": "Europe"
    }, 
    "ID": {
        "region": "South-Eastern Asia", 
        "name": "Indonesia", 
        "continent": "Asia"
    }, 
    "NHVU-TN": {
        "region": "Melanesia", 
        "name": "Tanna", 
        "continent": "Oceania"
    }, 
    "GB-ENG": {
        "region": "Northern Europe", 
        "name": "England", 
        "continent": "Europe"
    }, 
    "GG-AL": {
        "region": "Northern Europe", 
        "name": "Alderney", 
        "continent": "Europe"
    }, 
    "BD": {
        "region": "Southern Asia", 
        "name": "Bangladesh", 
        "continent": "Asia"
    }, 
    "BE": {
        "region": "Western Europe", 
        "name": "Belgium", 
        "continent": "Europe"
    }, 
    "BF": {
        "region": "Western Africa", 
        "name": "Burkina Faso", 
        "continent": "Africa"
    }, 
    "BG": {
        "region": "Eastern Europe", 
        "name": "Bulgaria", 
        "continent": "Europe"
    }, 
    "BA": {
        "region": "Southern Europe", 
        "name": "Bosnia and Herzegovina", 
        "continent": "Europe"
    }, 
    "BB": {
        "region": "Caribbean", 
        "name": "Barbados", 
        "continent": "South America"
    }, 
    "AE-SH": {
        "region": "Western Asia", 
        "name": "Sharjah", 
        "continent": "Asia"
    }, 
    "BL": {
        "region": "Caribbean", 
        "name": "Saint Barthélemy", 
        "continent": "South America"
    }, 
    "BM": {
        "region": "Northern America", 
        "name": "Bermuda", 
        "continent": "North America"
    }, 
    "BN": {
        "region": "South-Eastern Asia", 
        "aliases": [
            "Brunei Darussalam"
        ], 
        "name": "Brunei", 
        "continent": "Asia"
    }, 
    "BO": {
        "region": "Southern America", 
        "name": "Bolivia", 
        "continent": "South America"
    }, 
    "BH": {
        "region": "Western Asia", 
        "name": "Bahrain", 
        "continent": "Asia"
    }, 
    "BI": {
        "region": "Eastern Africa", 
        "name": "Burundi", 
        "continent": "Africa"
    }, 
    "BJ": {
        "region": "Western Africa", 
        "name": "Benin", 
        "continent": "Africa"
    }, 
    "BT": {
        "region": "Southern Asia", 
        "name": "Bhutan", 
        "continent": "Asia"
    }, 
    "BV": {
        "region": "Antarctica", 
        "name": "Bouvet Island", 
        "continent": "Antarctica"
    }, 
    "BW": {
        "region": "Southern Africa", 
        "name": "Botswana", 
        "continent": "Africa"
    }, 
    "BQ": {
        "region": "Caribbean", 
        "name": "Bonaire, Sint Eustatius and Saba", 
        "continent": "South America"
    }, 
    "BR": {
        "region": "Southern America", 
        "name": "Brazil", 
        "continent": "South America"
    }, 
    "BS": {
        "region": "Caribbean", 
        "aliases": [
            "The Bahamas"
        ], 
        "name": "Bahamas", 
        "continent": "South America"
    }, 
    "BY": {
        "region": "Eastern Europe", 
        "name": "Belarus", 
        "continent": "Europe"
    }, 
    "BZ": {
        "region": "Central America", 
        "name": "Belize", 
        "continent": "South America"
    }, 
    "DYBJ": {
        "region": "Western Africa", 
        "name": "Dahomey", 
        "continent": "Africa"
    }, 
    "IN-JK": {
        "region": "Southern Asia", 
        "name": "Jammu and Kashmir", 
        "continent": "Asia"
    }, 
    "GG-SA": {
        "region": "Northern Europe", 
        "name": "Sark", 
        "continent": "Europe"
    }, 
    "CY-NC": {
        "region": "Western Asia", 
        "name": "Northern Cyprus", 
        "continent": "Asia"
    }, 
    "ML-AZ": {
        "region": "Western Africa", 
        "name": "Azawad", 
        "continent": "Africa"
    }, 
    "OM": {
        "region": "Western Asia", 
        "name": "Oman", 
        "continent": "Asia"
    }, 
    "DDDE": {
        "region": "Western Europe", 
        "name": "East Germany", 
        "continent": "Europe"
    }, 
    "PCHH": {
        "region": "Micronesia", 
        "name": "Pacific Islands", 
        "continent": "Oceania"
    }, 
    "HR": {
        "region": "Southern Europe", 
        "name": "Croatia", 
        "continent": "Europe"
    }, 
    "AC": {
        "region": "Western Africa", 
        "name": "Ascension", 
        "continent": "Africa"
    }, 
    "HT": {
        "region": "Caribbean", 
        "name": "Haiti", 
        "continent": "South America"
    }, 
    "FQHH": {
        "region": "Antarctica", 
        "name": "French Southern and Antarctic Territories", 
        "continent": "Antarctica"
    }, 
    "HK": {
        "region": "Eastern Asia", 
        "name": "Hong Kong", 
        "continent": "Asia"
    }, 
    "HN": {
        "region": "Central America", 
        "name": "Honduras", 
        "continent": "South America"
    }, 
    "HM": {
        "region": "Antarctica", 
        "name": "Heard Island and McDonald Islands", 
        "continent": "Antarctica"
    }, 
    "PUUM": {
        "region": "Polynesia", 
        "name": "United States Miscellaneous Pacific Islands", 
        "continent": "Oceania"
    }, 
    "GETV": {
        "region": "Polynesia", 
        "name": "Ellice Islands", 
        "continent": "Oceania"
    }, 
    "ZA-VE": {
        "region": "Southern Africa", 
        "name": "Venda", 
        "continent": "Africa"
    }, 
    "GBAE": {
        "region": "Western Asia", 
        "name": "Trucial States", 
        "continent": "Asia"
    }, 
    "KHKA": {
        "region": "South-Eastern Asia", 
        "name": "Khmer Republic", 
        "continent": "Asia"
    }, 
    "UY": {
        "region": "Southern America", 
        "name": "Uruguay", 
        "continent": "South America"
    }, 
    "UZ": {
        "region": "Central Asia", 
        "name": "Uzbekistan", 
        "continent": "Asia"
    }, 
    "US": {
        "region": "Northern America", 
        "aliases": [
            "USA"
        ], 
        "name": "United States", 
        "continent": "North America"
    }, 
    "UM": {
        "region": "Polynesia", 
        "name": "United States Minor Outlying Islands", 
        "continent": "Oceania"
    }, 
    "UK": {
        "region": "Northern Europe", 
        "aliases": [
            "UK"
        ], 
        "name": "United Kingdom", 
        "continent": "Europe"
    }, 
    "AU": {
        "region": "Australia and New Zealand", 
        "name": "Australia", 
        "continent": "Oceania"
    }, 
    "UG": {
        "region": "Eastern Africa", 
        "name": "Uganda", 
        "continent": "Africa"
    }, 
    "UA": {
        "region": "Eastern Europe", 
        "name": "Ukraine", 
        "continent": "Europe"
    }, 
    "RHZW-RH": {
        "region": "Eastern Africa", 
        "name": "Rhodesia", 
        "continent": "Africa"
    }, 
    "NI": {
        "region": "Central America", 
        "name": "Nicaragua", 
        "continent": "South America"
    }, 
    "NL": {
        "region": "Western Europe", 
        "name": "Netherlands", 
        "continent": "Europe"
    }, 
    "NO": {
        "region": "Northern Europe", 
        "name": "Norway", 
        "continent": "Europe"
    }, 
    "NA": {
        "region": "Southern Africa", 
        "name": "Namibia", 
        "continent": "Africa"
    }, 
    "NC": {
        "region": "Melanesia", 
        "name": "New Caledonia", 
        "continent": "Oceania"
    }, 
    "NE": {
        "region": "Western Africa", 
        "name": "Niger", 
        "continent": "Africa"
    }, 
    "NF": {
        "region": "Australia and New Zealand", 
        "name": "Norfolk Island", 
        "continent": "Oceania"
    }, 
    "NG": {
        "region": "Western Africa", 
        "name": "Nigeria", 
        "continent": "Africa"
    }, 
    "NZ": {
        "region": "Australia and New Zealand", 
        "name": "New Zealand", 
        "continent": "Oceania"
    }, 
    "NP": {
        "region": "Southern Asia", 
        "name": "Nepal", 
        "continent": "Asia"
    }, 
    "AZ-NK": {
        "region": "Western Asia", 
        "name": "Nagorno-Karabakh", 
        "continent": "Asia"
    }, 
    "NU": {
        "region": "Polynesia", 
        "name": "Niue", 
        "continent": "Oceania"
    }, 
    "HU": {
        "region": "Eastern Europe", 
        "name": "Hungary", 
        "continent": "Europe"
    }, 
    "RHZW": {
        "region": "Eastern Africa", 
        "name": "Southern Rhodesia", 
        "continent": "Africa"
    }, 
    "AE-DU": {
        "region": "Western Asia", 
        "name": "Dubai", 
        "continent": "Asia"
    }, 
    "GB-SCT": {
        "region": "Northern Europe", 
        "name": "Scotland", 
        "continent": "Europe"
    }, 
    "TZ": {
        "region": "Eastern Africa", 
        "name": "Tanzania", 
        "continent": "Africa"
    }, 
    "TV": {
        "region": "Polynesia", 
        "name": "Tuvalu", 
        "continent": "Oceania"
    }, 
    "TW": {
        "region": "Eastern Asia", 
        "name": "Taiwan", 
        "continent": "Asia"
    }, 
    "TT": {
        "region": "Caribbean", 
        "name": "Trinidad and Tobago", 
        "continent": "South America"
    }, 
    "CL": {
        "region": "Southern America", 
        "name": "Chile", 
        "continent": "South America"
    }, 
    "TR": {
        "region": "Western Asia", 
        "name": "Turkey", 
        "continent": "Asia"
    }, 
    "TN": {
        "region": "Northern Africa", 
        "name": "Tunisia", 
        "continent": "Africa"
    }, 
    "TO": {
        "region": "Polynesia", 
        "name": "Tonga", 
        "continent": "Oceania"
    }, 
    "TL": {
        "region": "South-Eastern Asia", 
        "name": "Timor-Leste", 
        "continent": "Asia"
    }, 
    "TM": {
        "region": "Central Asia", 
        "name": "Turkmenistan", 
        "continent": "Asia"
    }, 
    "TJ": {
        "region": "Central Asia", 
        "name": "Tajikistan", 
        "continent": "Asia"
    }, 
    "TK": {
        "region": "Polynesia", 
        "name": "Tokelau", 
        "continent": "Oceania"
    }, 
    "TH": {
        "region": "South-Eastern Asia", 
        "name": "Thailand", 
        "continent": "Asia"
    }, 
    "TF": {
        "region": "Antarctica", 
        "name": "French Southern Territories", 
        "continent": "Antarctica"
    }, 
    "TG": {
        "region": "Western Africa", 
        "name": "Togo", 
        "continent": "Africa"
    }, 
    "TD": {
        "region": "Middle Africa", 
        "name": "Chad", 
        "continent": "Africa"
    }, 
    "TC": {
        "region": "Caribbean", 
        "name": "Turks and Caicos Islands", 
        "continent": "South America"
    }, 
    "TA": {
        "region": "Western Africa", 
        "name": "Tristan da Cunha", 
        "continent": "Africa"
    }, 
    "GE-SK": {
        "region": "Western Asia", 
        "name": "South Ossetia", 
        "continent": "Asia"
    }, 
    "AE": {
        "region": "Western Asia", 
        "name": "United Arab Emirates", 
        "continent": "Asia"
    }, 
    "AD": {
        "region": "Southern Europe", 
        "name": "Andorra", 
        "continent": "Europe"
    }, 
    "AG": {
        "region": "Caribbean", 
        "name": "Antigua and Barbuda", 
        "continent": "South America"
    }, 
    "AF": {
        "region": "Southern Asia", 
        "name": "Afghanistan", 
        "continent": "Asia"
    }, 
    "AI": {
        "region": "Caribbean", 
        "name": "Anguilla", 
        "continent": "South America"
    }, 
    "AM": {
        "region": "Western Asia", 
        "name": "Armenia", 
        "continent": "Asia"
    }, 
    "AL": {
        "region": "Southern Europe", 
        "name": "Albania", 
        "continent": "Europe"
    }, 
    "AO": {
        "region": "Middle Africa", 
        "name": "Angola", 
        "continent": "Africa"
    }, 
    "AQ": {
        "region": "Antarctica", 
        "name": "Antarctica", 
        "continent": "Antarctica"
    }, 
    "AS": {
        "region": "Polynesia", 
        "name": "American Samoa", 
        "continent": "Oceania"
    }, 
    "AR": {
        "region": "Southern America", 
        "name": "Argentina", 
        "continent": "South America"
    }, 
    "EGEG": {
        "region": "Northern Africa", 
        "name": "United Arab Republic", 
        "continent": "Africa"
    }, 
    "AT": {
        "region": "Western Europe", 
        "name": "Austria", 
        "continent": "Europe"
    }, 
    "AW": {
        "region": "Caribbean", 
        "name": "Aruba", 
        "continent": "South America"
    }, 
    "AX": {
        "region": "Northern Europe", 
        "name": "Åland Islands", 
        "continent": "Europe"
    }, 
    "AZ": {
        "region": "Western Asia", 
        "name": "Azerbaijan", 
        "continent": "Asia"
    }, 
    "YDYE": {
        "region": "Western Asia", 
        "name": "South Yemen", 
        "continent": "Asia"
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
    if isinstance(code_or_name, unicode):
        code_or_name = code_or_name.encode('utf-8')
    if len(code_or_name) == 2:
        code_or_name = code_or_name.upper()
        return COUNTRIES[code_or_name] if code_or_name in COUNTRIES else {}
    else:
        for code, country in COUNTRIES.iteritems():
            if code_or_name == country['name'] or (
                'aliases' in country and code_or_name in country['aliases']
            ):
                return country
    return {}

def get_country_name(country_code):
    country_code = country_code.upper()
    return COUNTRIES[country_code]['name'] if country_code in COUNTRIES else ''

def normalize_country_name(country_name):
    if isinstance(country_name, unicode):
        country_name = country_name.encode('utf-8')
    name = None
    for code, country in COUNTRIES.iteritems():
        if country_name == country['name'] or (
            'aliases' in country and country_name in country['aliases']
        ):
            name = country['name']
            break
    return name and name.decode('utf-8')

def split_geoname(geoname):
    if isinstance(geoname, unicode):
        geoname = geoname.encode('utf-8')
    countries = [
        'Bonaire, Sint Eustatius and Saba',
        'Saint Helena, Ascension and Tristan da Cunha'
    ]
    for country in countries:
        if geoname.endswith(country):
            geoname = geoname.replace(country, country.replace(', ', '; '))
    split = geoname.split(', ')
    for country in countries:
        if geoname.endswith(country.replace(', ', '; ')):
            split[-1] = country
    return split
