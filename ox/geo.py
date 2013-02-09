# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2008

import math

__all__ = ['get_country', 'get_country_name']

'''
var countries = {};
Ox.COUNTRIES.forEach(function(country) {
    if (country.code.length == 2) {
        countries[country.code] = {
            name: country.name,
            region: country.region,
            continent: country.continent
        }
        if (country.googleName || country.imdbName) {
            countries[country.code].aliases = Ox.compact(Ox.unique(
                [country.googleName, country.imdbName]
            ));
        }
    }
});
Ox.print(JSON.stringify(countries, null, '   '));
'''

COUNTRIES = {
    "AC": {
        "name": "Ascension",
        "region": "Western Africa",
        "continent": "Africa"
    },
    "AD": {
        "name": "Andorra",
        "region": "Southern Europe",
        "continent": "Europe"
    },
    "AE": {
        "name": "United Arab Emirates",
        "region": "Western Asia",
        "continent": "Asia"
    },
    "AF": {
        "name": "Afghanistan",
        "region": "Southern Asia",
        "continent": "Asia"
    },
    "AG": {
        "name": "Antigua and Barbuda",
        "region": "Caribbean",
        "continent": "South America"
    },
    "AI": {
        "name": "Anguilla",
        "region": "Caribbean",
        "continent": "South America"
    },
    "AL": {
        "name": "Albania",
        "region": "Southern Europe",
        "continent": "Europe"
    },
    "AM": {
        "name": "Armenia",
        "region": "Western Asia",
        "continent": "Asia"
    },
    "AO": {
        "name": "Angola",
        "region": "Middle Africa",
        "continent": "Africa"
    },
    "AQ": {
        "name": "Antarctica",
        "region": "Antarctica",
        "continent": "Antarctica"
    },
    "AR": {
        "name": "Argentina",
        "region": "Southern America",
        "continent": "South America"
    },
    "AS": {
        "name": "American Samoa",
        "region": "Polynesia",
        "continent": "Oceania"
    },
    "AT": {
        "name": "Austria",
        "region": "Western Europe",
        "continent": "Europe"
    },
    "AU": {
        "name": "Australia",
        "region": "Australia and New Zealand",
        "continent": "Oceania"
    },
    "AW": {
        "name": "Aruba",
        "region": "Caribbean",
        "continent": "South America"
    },
    "AX": {
        "name": "Åland Islands",
        "region": "Northern Europe",
        "continent": "Europe"
    },
    "AZ": {
        "name": "Azerbaijan",
        "region": "Western Asia",
        "continent": "Asia"
    },
    "BA": {
        "name": "Bosnia and Herzegovina",
        "region": "Southern Europe",
        "continent": "Europe"
    },
    "BB": {
        "name": "Barbados",
        "region": "Caribbean",
        "continent": "South America"
    },
    "BD": {
        "name": "Bangladesh",
        "region": "Southern Asia",
        "continent": "Asia"
    },
    "BE": {
        "name": "Belgium",
        "region": "Western Europe",
        "continent": "Europe"
    },
    "BF": {
        "name": "Burkina Faso",
        "region": "Western Africa",
        "continent": "Africa"
    },
    "BG": {
        "name": "Bulgaria",
        "region": "Eastern Europe",
        "continent": "Europe"
    },
    "BH": {
        "name": "Bahrain",
        "region": "Western Asia",
        "continent": "Asia"
    },
    "BI": {
        "name": "Burundi",
        "region": "Eastern Africa",
        "continent": "Africa"
    },
    "BJ": {
        "name": "Benin",
        "region": "Western Africa",
        "continent": "Africa"
    },
    "BL": {
        "name": "Saint Barthélemy",
        "region": "Caribbean",
        "continent": "South America"
    },
    "BM": {
        "name": "Bermuda",
        "region": "Northern America",
        "continent": "North America"
    },
    "BN": {
        "name": "Brunei",
        "region": "South-Eastern Asia",
        "continent": "Asia",
        "aliases": [
            "Brunei Darussalam"
        ]
    },
    "BO": {
        "name": "Bolivia",
        "region": "Southern America",
        "continent": "South America"
    },
    "BQ": {
        "name": "Bonaire, Sint Eustatius and Saba",
        "region": "Caribbean",
        "continent": "South America"
    },
    "BR": {
        "name": "Brazil",
        "region": "Southern America",
        "continent": "South America"
    },
    "BS": {
        "name": "Bahamas",
        "region": "Caribbean",
        "continent": "South America",
        "aliases": [
            "The Bahamas"
        ]
    },
    "BT": {
        "name": "Bhutan",
        "region": "Southern Asia",
        "continent": "Asia"
    },
    "BV": {
        "name": "Bouvet Island",
        "region": "Antarctica",
        "continent": "Antarctica"
    },
    "BW": {
        "name": "Botswana",
        "region": "Southern Africa",
        "continent": "Africa"
    },
    "BY": {
        "name": "Belarus",
        "region": "Eastern Europe",
        "continent": "Europe"
    },
    "BZ": {
        "name": "Belize",
        "region": "Central America",
        "continent": "South America"
    },
    "CA": {
        "name": "Canada",
        "region": "Northern America",
        "continent": "North America"
    },
    "CC": {
        "name": "Cocos Islands",
        "region": "South-Eastern Asia",
        "continent": "Asia",
        "aliases": [
            "Cocos (Keeling) Islands"
        ]
    },
    "CD": {
        "name": "Democratic Republic of the Congo",
        "region": "Middle Africa",
        "continent": "Africa",
        "aliases": [
            "Democratic Republic of Congo"
        ]
    },
    "CF": {
        "name": "Central African Republic",
        "region": "Middle Africa",
        "continent": "Africa"
    },
    "CG": {
        "name": "Republic of the Congo",
        "region": "Middle Africa",
        "continent": "Africa",
        "aliases": [
            "Congo"
        ]
    },
    "CH": {
        "name": "Switzerland",
        "region": "Western Europe",
        "continent": "Europe"
    },
    "CI": {
        "name": "Côte d'Ivoire",
        "region": "Western Africa",
        "continent": "Africa",
        "aliases": [
            "Ivory Coast"
        ]
    },
    "CK": {
        "name": "Cook Islands",
        "region": "Polynesia",
        "continent": "Oceania"
    },
    "CL": {
        "name": "Chile",
        "region": "Southern America",
        "continent": "South America"
    },
    "CM": {
        "name": "Cameroon",
        "region": "Middle Africa",
        "continent": "Africa"
    },
    "CN": {
        "name": "China",
        "region": "Eastern Asia",
        "continent": "Asia"
    },
    "CO": {
        "name": "Colombia",
        "region": "Southern America",
        "continent": "South America"
    },
    "CP": {
        "name": "Clipperton Island",
        "region": "Central America",
        "continent": "South America"
    },
    "CR": {
        "name": "Costa Rica",
        "region": "Central America",
        "continent": "South America"
    },
    "CU": {
        "name": "Cuba",
        "region": "Caribbean",
        "continent": "South America"
    },
    "CV": {
        "name": "Cape Verde",
        "region": "Western Africa",
        "continent": "Africa"
    },
    "CW": {
        "name": "Curaçao",
        "region": "Caribbean",
        "continent": "South America"
    },
    "CX": {
        "name": "Christmas Island",
        "region": "South-Eastern Asia",
        "continent": "Asia"
    },
    "CY": {
        "name": "Cyprus",
        "region": "Western Asia",
        "continent": "Asia"
    },
    "CZ": {
        "name": "Czech Republic",
        "region": "Eastern Europe",
        "continent": "Europe"
    },
    "DE": {
        "name": "Germany",
        "region": "Western Europe",
        "continent": "Europe"
    },
    "DG": {
        "name": "Diego Garcia",
        "region": "Southern Asia",
        "continent": "Asia"
    },
    "DJ": {
        "name": "Djibouti",
        "region": "Eastern Africa",
        "continent": "Africa"
    },
    "DK": {
        "name": "Denmark",
        "region": "Northern Europe",
        "continent": "Europe"
    },
    "DM": {
        "name": "Dominica",
        "region": "Caribbean",
        "continent": "South America"
    },
    "DO": {
        "name": "Dominican Republic",
        "region": "Caribbean",
        "continent": "South America"
    },
    "DZ": {
        "name": "Algeria",
        "region": "Northern Africa",
        "continent": "Africa"
    },
    "EA": {
        "name": "Ceuta and Melilla",
        "region": "Northern Africa",
        "continent": "Africa"
    },
    "EC": {
        "name": "Ecuador",
        "region": "Southern America",
        "continent": "South America"
    },
    "EE": {
        "name": "Estonia",
        "region": "Northern Europe",
        "continent": "Europe"
    },
    "EG": {
        "name": "Egypt",
        "region": "Northern Africa",
        "continent": "Africa"
    },
    "EH": {
        "name": "Sahrawi",
        "region": "Northern Africa",
        "continent": "Africa",
        "aliases": [
            "Western Sahara"
        ]
    },
    "ER": {
        "name": "Eritrea",
        "region": "Eastern Africa",
        "continent": "Africa"
    },
    "ES": {
        "name": "Spain",
        "region": "Southern Europe",
        "continent": "Europe"
    },
    "ET": {
        "name": "Ethiopia",
        "region": "Eastern Africa",
        "continent": "Africa"
    },
    "EU": {
        "name": "European Union",
        "region": "Western Europe",
        "continent": "Europe"
    },
    "FI": {
        "name": "Finland",
        "region": "Northern Europe",
        "continent": "Europe"
    },
    "FJ": {
        "name": "Fiji",
        "region": "Melanesia",
        "continent": "Oceania"
    },
    "FK": {
        "name": "Falkland Islands",
        "region": "Southern America",
        "continent": "South America"
    },
    "FM": {
        "name": "Micronesia",
        "region": "Micronesia",
        "continent": "Oceania",
        "aliases": [
            "Federated States of Micronesia"
        ]
    },
    "FO": {
        "name": "Faroe Islands",
        "region": "Northern Europe",
        "continent": "Europe"
    },
    "FR": {
        "name": "France",
        "region": "Western Europe",
        "continent": "Europe"
    },
    "GA": {
        "name": "Gabon",
        "region": "Middle Africa",
        "continent": "Africa"
    },
    "GB": {
        "name": "United Kingdom",
        "region": "Northern Europe",
        "continent": "Europe",
        "aliases": [
            "UK"
        ]
    },
    "GD": {
        "name": "Grenada",
        "region": "Caribbean",
        "continent": "South America"
    },
    "GE": {
        "name": "Georgia",
        "region": "Western Asia",
        "continent": "Asia"
    },
    "GF": {
        "name": "French Guiana",
        "region": "Southern America",
        "continent": "South America"
    },
    "GG": {
        "name": "Guernsey",
        "region": "Northern Europe",
        "continent": "Europe"
    },
    "GH": {
        "name": "Ghana",
        "region": "Western Africa",
        "continent": "Africa"
    },
    "GI": {
        "name": "Gibraltar",
        "region": "Southern Europe",
        "continent": "Europe"
    },
    "GL": {
        "name": "Greenland",
        "region": "Northern America",
        "continent": "North America"
    },
    "GM": {
        "name": "Gambia",
        "region": "Western Africa",
        "continent": "Africa",
        "aliases": [
            "The Gambia"
        ]
    },
    "GN": {
        "name": "Guinea",
        "region": "Western Africa",
        "continent": "Africa"
    },
    "GP": {
        "name": "Guadeloupe",
        "region": "Caribbean",
        "continent": "South America"
    },
    "GQ": {
        "name": "Equatorial Guinea",
        "region": "Middle Africa",
        "continent": "Africa"
    },
    "GR": {
        "name": "Greece",
        "region": "Southern Europe",
        "continent": "Europe"
    },
    "GS": {
        "name": "South Georgia and the South Sandwich Islands",
        "region": "Antarctica",
        "continent": "Antarctica"
    },
    "GT": {
        "name": "Guatemala",
        "region": "Central America",
        "continent": "South America"
    },
    "GU": {
        "name": "Guam",
        "region": "Micronesia",
        "continent": "Oceania"
    },
    "GW": {
        "name": "Guinea-Bissau",
        "region": "Western Africa",
        "continent": "Africa"
    },
    "GY": {
        "name": "Guyana",
        "region": "Southern America",
        "continent": "South America"
    },
    "HK": {
        "name": "Hong Kong",
        "region": "Eastern Asia",
        "continent": "Asia"
    },
    "HM": {
        "name": "Heard Island and McDonald Islands",
        "region": "Antarctica",
        "continent": "Antarctica"
    },
    "HN": {
        "name": "Honduras",
        "region": "Central America",
        "continent": "South America"
    },
    "HR": {
        "name": "Croatia",
        "region": "Southern Europe",
        "continent": "Europe"
    },
    "HT": {
        "name": "Haiti",
        "region": "Caribbean",
        "continent": "South America"
    },
    "HU": {
        "name": "Hungary",
        "region": "Eastern Europe",
        "continent": "Europe"
    },
    "IC": {
        "name": "Canary Islands",
        "region": "Northern Africa",
        "continent": "Africa"
    },
    "ID": {
        "name": "Indonesia",
        "region": "South-Eastern Asia",
        "continent": "Asia"
    },
    "IE": {
        "name": "Ireland",
        "region": "Northern Europe",
        "continent": "Europe"
    },
    "IL": {
        "name": "Israel",
        "region": "Western Asia",
        "continent": "Asia"
    },
    "IM": {
        "name": "Isle of Man",
        "region": "Northern Europe",
        "continent": "Europe"
    },
    "IN": {
        "name": "India",
        "region": "Southern Asia",
        "continent": "Asia"
    },
    "IO": {
        "name": "British Indian Ocean Territory",
        "region": "Southern Asia",
        "continent": "Asia"
    },
    "IQ": {
        "name": "Iraq",
        "region": "Western Asia",
        "continent": "Asia"
    },
    "IR": {
        "name": "Iran",
        "region": "Southern Asia",
        "continent": "Asia"
    },
    "IS": {
        "name": "Iceland",
        "region": "Northern Europe",
        "continent": "Europe"
    },
    "IT": {
        "name": "Italy",
        "region": "Southern Europe",
        "continent": "Europe"
    },
    "JE": {
        "name": "Jersey",
        "region": "Northern Europe",
        "continent": "Europe"
    },
    "JM": {
        "name": "Jamaica",
        "region": "Caribbean",
        "continent": "South America"
    },
    "JO": {
        "name": "Jordan",
        "region": "Western Asia",
        "continent": "Asia"
    },
    "JP": {
        "name": "Japan",
        "region": "Eastern Asia",
        "continent": "Asia"
    },
    "KE": {
        "name": "Kenya",
        "region": "Eastern Africa",
        "continent": "Africa"
    },
    "KG": {
        "name": "Kyrgyzstan",
        "region": "Central Asia",
        "continent": "Asia"
    },
    "KH": {
        "name": "Cambodia",
        "region": "South-Eastern Asia",
        "continent": "Asia"
    },
    "KI": {
        "name": "Kiribati",
        "region": "Micronesia",
        "continent": "Oceania"
    },
    "KM": {
        "name": "Comoros",
        "region": "Eastern Africa",
        "continent": "Africa"
    },
    "KN": {
        "name": "Saint Kitts and Nevis",
        "region": "Caribbean",
        "continent": "South America"
    },
    "KP": {
        "name": "North Korea",
        "region": "Eastern Asia",
        "continent": "Asia"
    },
    "KR": {
        "name": "South Korea",
        "region": "Eastern Asia",
        "continent": "Asia"
    },
    "KW": {
        "name": "Kuwait",
        "region": "Western Asia",
        "continent": "Asia"
    },
    "KY": {
        "name": "Cayman Islands",
        "region": "Caribbean",
        "continent": "South America"
    },
    "KZ": {
        "name": "Kazakhstan",
        "region": "Central Asia",
        "continent": "Asia"
    },
    "LA": {
        "name": "Laos",
        "region": "South-Eastern Asia",
        "continent": "Asia"
    },
    "LB": {
        "name": "Lebanon",
        "region": "Western Asia",
        "continent": "Asia"
    },
    "LC": {
        "name": "Saint Lucia",
        "region": "Caribbean",
        "continent": "South America"
    },
    "LI": {
        "name": "Liechtenstein",
        "region": "Western Europe",
        "continent": "Europe"
    },
    "LK": {
        "name": "Sri Lanka",
        "region": "Southern Asia",
        "continent": "Asia"
    },
    "LR": {
        "name": "Liberia",
        "region": "Western Africa",
        "continent": "Africa"
    },
    "LS": {
        "name": "Lesotho",
        "region": "Southern Africa",
        "continent": "Africa"
    },
    "LT": {
        "name": "Lithuania",
        "region": "Northern Europe",
        "continent": "Europe"
    },
    "LU": {
        "name": "Luxembourg",
        "region": "Western Europe",
        "continent": "Europe"
    },
    "LV": {
        "name": "Latvia",
        "region": "Northern Europe",
        "continent": "Europe"
    },
    "LY": {
        "name": "Libya",
        "region": "Northern Africa",
        "continent": "Africa"
    },
    "MA": {
        "name": "Morocco",
        "region": "Northern Africa",
        "continent": "Africa"
    },
    "MC": {
        "name": "Monaco",
        "region": "Western Europe",
        "continent": "Europe"
    },
    "MD": {
        "name": "Moldova",
        "region": "Eastern Europe",
        "continent": "Europe"
    },
    "ME": {
        "name": "Montenegro",
        "region": "Southern Europe",
        "continent": "Europe"
    },
    "MF": {
        "name": "Saint Martin",
        "region": "Caribbean",
        "continent": "South America",
        "aliases": [
            "Saint Martin (French part)"
        ]
    },
    "MG": {
        "name": "Madagascar",
        "region": "Eastern Africa",
        "continent": "Africa"
    },
    "MH": {
        "name": "Marshall Islands",
        "region": "Micronesia",
        "continent": "Oceania"
    },
    "MK": {
        "name": "Macedonia",
        "region": "Southern Europe",
        "continent": "Europe",
        "aliases": [
            "Former Yugoslav Republic of Macedonia",
            "Republic of Macedonia"
        ]
    },
    "ML": {
        "name": "Mali",
        "region": "Western Africa",
        "continent": "Africa"
    },
    "MM": {
        "name": "Myanmar",
        "region": "South-Eastern Asia",
        "continent": "Asia",
        "aliases": [
            "Burma"
        ]
    },
    "MN": {
        "name": "Mongolia",
        "region": "Eastern Asia",
        "continent": "Asia"
    },
    "MO": {
        "name": "Macau",
        "region": "Eastern Asia",
        "continent": "Asia",
        "aliases": [
            "Macao"
        ]
    },
    "MP": {
        "name": "Northern Mariana Islands",
        "region": "Micronesia",
        "continent": "Oceania"
    },
    "MQ": {
        "name": "Martinique",
        "region": "Caribbean",
        "continent": "South America"
    },
    "MR": {
        "name": "Mauritania",
        "region": "Western Africa",
        "continent": "Africa"
    },
    "MS": {
        "name": "Montserrat",
        "region": "Caribbean",
        "continent": "South America"
    },
    "MT": {
        "name": "Malta",
        "region": "Southern Europe",
        "continent": "Europe"
    },
    "MU": {
        "name": "Mauritius",
        "region": "Eastern Africa",
        "continent": "Africa"
    },
    "MV": {
        "name": "Maldives",
        "region": "Southern Asia",
        "continent": "Asia"
    },
    "MW": {
        "name": "Malawi",
        "region": "Eastern Africa",
        "continent": "Africa"
    },
    "MX": {
        "name": "Mexico",
        "region": "Central America",
        "continent": "South America"
    },
    "MY": {
        "name": "Malaysia",
        "region": "South-Eastern Asia",
        "continent": "Asia"
    },
    "MZ": {
        "name": "Mozambique",
        "region": "Eastern Africa",
        "continent": "Africa"
    },
    "NA": {
        "name": "Namibia",
        "region": "Southern Africa",
        "continent": "Africa"
    },
    "NC": {
        "name": "New Caledonia",
        "region": "Melanesia",
        "continent": "Oceania"
    },
    "NE": {
        "name": "Niger",
        "region": "Western Africa",
        "continent": "Africa"
    },
    "NF": {
        "name": "Norfolk Island",
        "region": "Australia and New Zealand",
        "continent": "Oceania"
    },
    "NG": {
        "name": "Nigeria",
        "region": "Western Africa",
        "continent": "Africa"
    },
    "NI": {
        "name": "Nicaragua",
        "region": "Central America",
        "continent": "South America"
    },
    "NL": {
        "name": "Netherlands",
        "region": "Western Europe",
        "continent": "Europe"
    },
    "NO": {
        "name": "Norway",
        "region": "Northern Europe",
        "continent": "Europe"
    },
    "NP": {
        "name": "Nepal",
        "region": "Southern Asia",
        "continent": "Asia"
    },
    "NR": {
        "name": "Nauru",
        "region": "Micronesia",
        "continent": "Oceania"
    },
    "NU": {
        "name": "Niue",
        "region": "Polynesia",
        "continent": "Oceania"
    },
    "NZ": {
        "name": "New Zealand",
        "region": "Australia and New Zealand",
        "continent": "Oceania"
    },
    "OM": {
        "name": "Oman",
        "region": "Western Asia",
        "continent": "Asia"
    },
    "PA": {
        "name": "Panama",
        "region": "Central America",
        "continent": "South America"
    },
    "PE": {
        "name": "Peru",
        "region": "Southern America",
        "continent": "South America"
    },
    "PF": {
        "name": "French Polynesia",
        "region": "Polynesia",
        "continent": "Oceania"
    },
    "PG": {
        "name": "Papua New Guinea",
        "region": "Melanesia",
        "continent": "Oceania"
    },
    "PH": {
        "name": "Philippines",
        "region": "South-Eastern Asia",
        "continent": "Asia"
    },
    "PK": {
        "name": "Pakistan",
        "region": "Southern Asia",
        "continent": "Asia"
    },
    "PL": {
        "name": "Poland",
        "region": "Eastern Europe",
        "continent": "Europe"
    },
    "PM": {
        "name": "Saint Pierre and Miquelon",
        "region": "Northern America",
        "continent": "North America"
    },
    "PN": {
        "name": "Pitcairn Islands",
        "region": "Polynesia",
        "continent": "Oceania",
        "aliases": [
            "Pitcairn"
        ]
    },
    "PR": {
        "name": "Puerto Rico",
        "region": "Caribbean",
        "continent": "South America"
    },
    "PS": {
        "name": "Palestine",
        "region": "Western Asia",
        "continent": "Asia",
        "aliases": [
            "Palestinian Territories",
            "Occupied Palestinian Territory"
        ]
    },
    "PT": {
        "name": "Portugal",
        "region": "Southern Europe",
        "continent": "Europe"
    },
    "PW": {
        "name": "Palau",
        "region": "Micronesia",
        "continent": "Oceania"
    },
    "PY": {
        "name": "Paraguay",
        "region": "Southern America",
        "continent": "South America"
    },
    "QA": {
        "name": "Qatar",
        "region": "Western Asia",
        "continent": "Asia"
    },
    "RE": {
        "name": "Réunion",
        "region": "Eastern Africa",
        "continent": "Africa"
    },
    "RO": {
        "name": "Romania",
        "region": "Eastern Europe",
        "continent": "Europe"
    },
    "RS": {
        "name": "Serbia",
        "region": "Southern Europe",
        "continent": "Europe"
    },
    "RU": {
        "name": "Russia",
        "region": "Eastern Europe",
        "continent": "Europe"
    },
    "RW": {
        "name": "Rwanda",
        "region": "Eastern Africa",
        "continent": "Africa"
    },
    "SA": {
        "name": "Saudi Arabia",
        "region": "Western Asia",
        "continent": "Asia"
    },
    "SB": {
        "name": "Solomon Islands",
        "region": "Melanesia",
        "continent": "Oceania"
    },
    "SC": {
        "name": "Seychelles",
        "region": "Eastern Africa",
        "continent": "Africa"
    },
    "SD": {
        "name": "Sudan",
        "region": "Northern Africa",
        "continent": "Africa"
    },
    "SE": {
        "name": "Sweden",
        "region": "Northern Europe",
        "continent": "Europe"
    },
    "SG": {
        "name": "Singapore",
        "region": "South-Eastern Asia",
        "continent": "Asia"
    },
    "SH": {
        "name": "Saint Helena, Ascension and Tristan da Cunha",
        "region": "Western Africa",
        "continent": "Africa",
        "aliases": [
            "Saint Helena"
        ]
    },
    "SI": {
        "name": "Slovenia",
        "region": "Southern Europe",
        "continent": "Europe"
    },
    "SJ": {
        "name": "Svalbard and Jan Mayen",
        "region": "Northern Europe",
        "continent": "Europe"
    },
    "SK": {
        "name": "Slovakia",
        "region": "Eastern Europe",
        "continent": "Europe"
    },
    "SL": {
        "name": "Sierra Leone",
        "region": "Western Africa",
        "continent": "Africa"
    },
    "SM": {
        "name": "San Marino",
        "region": "Southern Europe",
        "continent": "Europe"
    },
    "SN": {
        "name": "Senegal",
        "region": "Western Africa",
        "continent": "Africa"
    },
    "SO": {
        "name": "Somalia",
        "region": "Eastern Africa",
        "continent": "Africa"
    },
    "SR": {
        "name": "Suriname",
        "region": "Southern America",
        "continent": "South America"
    },
    "SS": {
        "name": "South Sudan",
        "region": "Northern Africa",
        "continent": "Africa"
    },
    "ST": {
        "name": "São Tomé and Príncipe",
        "region": "Middle Africa",
        "continent": "Africa",
        "aliases": [
            "Sao Tome and Principe"
        ]
    },
    "SV": {
        "name": "El Salvador",
        "region": "Central America",
        "continent": "South America"
    },
    "SX": {
        "name": "Sint Maarten",
        "region": "Caribbean",
        "continent": "South America"
    },
    "SY": {
        "name": "Syria",
        "region": "Western Asia",
        "continent": "Asia"
    },
    "SZ": {
        "name": "Swaziland",
        "region": "Southern Africa",
        "continent": "Africa"
    },
    "TA": {
        "name": "Tristan da Cunha",
        "region": "Western Africa",
        "continent": "Africa"
    },
    "TC": {
        "name": "Turks and Caicos Islands",
        "region": "Caribbean",
        "continent": "South America"
    },
    "TD": {
        "name": "Chad",
        "region": "Middle Africa",
        "continent": "Africa"
    },
    "TF": {
        "name": "French Southern Territories",
        "region": "Antarctica",
        "continent": "Antarctica"
    },
    "TG": {
        "name": "Togo",
        "region": "Western Africa",
        "continent": "Africa"
    },
    "TH": {
        "name": "Thailand",
        "region": "South-Eastern Asia",
        "continent": "Asia"
    },
    "TJ": {
        "name": "Tajikistan",
        "region": "Central Asia",
        "continent": "Asia"
    },
    "TK": {
        "name": "Tokelau",
        "region": "Polynesia",
        "continent": "Oceania"
    },
    "TL": {
        "name": "Timor-Leste",
        "region": "South-Eastern Asia",
        "continent": "Asia"
    },
    "TM": {
        "name": "Turkmenistan",
        "region": "Central Asia",
        "continent": "Asia"
    },
    "TN": {
        "name": "Tunisia",
        "region": "Northern Africa",
        "continent": "Africa"
    },
    "TO": {
        "name": "Tonga",
        "region": "Polynesia",
        "continent": "Oceania"
    },
    "TR": {
        "name": "Turkey",
        "region": "Western Asia",
        "continent": "Asia"
    },
    "TT": {
        "name": "Trinidad and Tobago",
        "region": "Caribbean",
        "continent": "South America"
    },
    "TV": {
        "name": "Tuvalu",
        "region": "Polynesia",
        "continent": "Oceania"
    },
    "TW": {
        "name": "Taiwan",
        "region": "Eastern Asia",
        "continent": "Asia"
    },
    "TZ": {
        "name": "Tanzania",
        "region": "Eastern Africa",
        "continent": "Africa"
    },
    "UA": {
        "name": "Ukraine",
        "region": "Eastern Europe",
        "continent": "Europe"
    },
    "UG": {
        "name": "Uganda",
        "region": "Eastern Africa",
        "continent": "Africa"
    },
    "UK": {
        "name": "United Kingdom",
        "region": "Northern Europe",
        "continent": "Europe",
        "aliases": [
            "UK"
        ]
    },
    "UM": {
        "name": "United States Minor Outlying Islands",
        "region": "Polynesia",
        "continent": "Oceania"
    },
    "US": {
        "name": "United States",
        "region": "Northern America",
        "continent": "North America",
        "aliases": [
            "USA"
        ]
    },
    "UY": {
        "name": "Uruguay",
        "region": "Southern America",
        "continent": "South America"
    },
    "UZ": {
        "name": "Uzbekistan",
        "region": "Central Asia",
        "continent": "Asia"
    },
    "VA": {
        "name": "Vatican City",
        "region": "Southern Europe",
        "continent": "Europe",
        "aliases": [
            "Holy See (Vatican City State)"
        ]
    },
    "VC": {
        "name": "Saint Vincent and the Grenadines",
        "region": "Caribbean",
        "continent": "South America"
    },
    "VE": {
        "name": "Venezuela",
        "region": "Southern America",
        "continent": "South America"
    },
    "VG": {
        "name": "British Virgin Islands",
        "region": "Caribbean",
        "continent": "South America"
    },
    "VI": {
        "name": "United States Virgin Islands",
        "region": "Caribbean",
        "continent": "South America",
        "aliases": [
            "US Virgin Islands"
        ]
    },
    "VN": {
        "name": "Vietnam",
        "region": "South-Eastern Asia",
        "continent": "Asia"
    },
    "VU": {
        "name": "Vanuatu",
        "region": "Melanesia",
        "continent": "Oceania"
    },
    "WF": {
        "name": "Wallis and Futuna",
        "region": "Polynesia",
        "continent": "Oceania"
    },
    "WS": {
        "name": "Samoa",
        "region": "Polynesia",
        "continent": "Oceania"
    },
    "XK": {
        "name": "Kosovo",
        "region": "Southern Europe",
        "continent": "Europe",
        "aliases": [
            "Kosova (Kosovo)"
        ]
    },
    "YE": {
        "name": "Yemen",
        "region": "Western Asia",
        "continent": "Asia"
    },
    "YT": {
        "name": "Mayotte",
        "region": "Eastern Africa",
        "continent": "Africa"
    },
    "ZA": {
        "name": "South Africa",
        "region": "Southern Africa",
        "continent": "Africa"
    },
    "ZM": {
        "name": "Zambia",
        "region": "Eastern Africa",
        "continent": "Africa"
    },
    "ZW": {
        "name": "Zimbabwe",
        "region": "Eastern Africa",
        "continent": "Africa"
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

def get_country(country_code):
    country_code = country_code.upper()
    return COUNTRIES[country_code] if country_code in COUNTRIES else {}

def get_country_name(country_code):
    country_code = country_code.upper()
    return COUNTRIES[country_code]['name'] if country_code in COUNTRIES else ''

def normalize_country_name(country_name):
    name = None
    for code, country in COUNTRIES.iteritems():
        if country_name == country['name'] or (
            'aliases' in country and country_name in country['aliases']
        ):
            name = country['name']
            break
    return name
