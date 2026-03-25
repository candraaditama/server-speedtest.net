"""
Fetch Ookla Speedtest.net server list and generate MikroTik .rsc files.
Queries the Speedtest.net API from multiple geographic coordinates to get comprehensive server coverage.
"""
import json
import urllib.request
import urllib.error
import time
import sys
import os

# Define geographic query points to cover different regions
# Each entry: (lat, lon, description)
QUERY_POINTS = {
    "ASEAN": [
        # Indonesia
        (-6.2088, 106.8456, "Jakarta"),
        (-7.2575, 112.7521, "Surabaya"),
        (-6.9175, 107.6191, "Bandung"),
        (-8.6500, 115.2167, "Bali"),
        (3.5952, 98.6722, "Medan"),
        (-5.1477, 119.4327, "Makassar"),
        (-0.5071, 117.1526, "Balikpapan"),
        (1.4748, 124.8421, "Manado"),
        (-2.5916, 140.6690, "Jayapura"),
        (-3.6954, 128.1814, "Ambon"),
        (-1.6101, 103.6131, "Batam"),
        (-2.9761, 104.7754, "Palembang"),
        (0.5071, 101.4478, "Pekanbaru"),
        (-7.7956, 110.3695, "Yogyakarta"),
        (-6.9666, 110.4196, "Semarang"),
        # Singapore
        (1.3521, 103.8198, "Singapore"),
        # Malaysia
        (3.1390, 101.6869, "Kuala Lumpur"),
        (5.4164, 100.3327, "Penang"),
        (1.5535, 110.3593, "Kuching"),
        (6.1256, 116.0563, "Kota Kinabalu"),
        (4.5996, 103.4169, "Kuantan"),
        (1.4854, 103.7618, "Johor"),
        # Thailand
        (13.7563, 100.5018, "Bangkok"),
        (18.7883, 98.9853, "Chiang Mai"),
        (7.0051, 100.4747, "Hat Yai"),
        (12.9236, 100.8825, "Pattaya"),
        (8.0863, 98.9063, "Phuket"),
        (14.9713, 102.1019, "Nakhon Ratchasima"),
        (16.4322, 102.8236, "Khon Kaen"),
        # Vietnam
        (21.0285, 105.8542, "Hanoi"),
        (10.8231, 106.6297, "Ho Chi Minh City"),
        (16.0544, 108.2022, "Da Nang"),
        (10.0452, 105.7469, "Can Tho"),
        # Philippines
        (14.5995, 120.9842, "Manila"),
        (10.3157, 123.8854, "Cebu"),
        (7.1907, 125.4553, "Davao"),
        (10.3000, 123.9000, "Cebu City"),
        (14.6042, 121.0345, "Quezon City"),
        (16.4023, 120.5960, "Baguio"),
        # Cambodia
        (11.5564, 104.9282, "Phnom Penh"),
        (13.3633, 103.8564, "Siem Reap"),
        # Myanmar
        (16.8661, 96.1951, "Yangon"),
        (21.9588, 96.0891, "Mandalay"),
        # Laos
        (17.9757, 102.6331, "Vientiane"),
        # Brunei
        (4.9031, 114.9399, "Bandar Seri Begawan"),
        # Timor-Leste
        (-8.5569, 125.5603, "Dili"),
        # Taiwan
        (25.0330, 121.5654, "Taipei"),
        (22.6273, 120.3014, "Kaohsiung"),
        (24.1477, 120.6736, "Taichung"),
        # Hong Kong
        (22.3193, 114.1694, "Hong Kong"),
        # Macau
        (22.1987, 113.5439, "Macau"),
        # Australia (nearby)
        (-12.4634, 130.8456, "Darwin"),
        (-31.9505, 115.8605, "Perth"),
        (-33.8688, 151.2093, "Sydney"),
        (-37.8136, 144.9631, "Melbourne"),
        (-27.4698, 153.0251, "Brisbane"),
        (-34.9285, 138.6007, "Adelaide"),
        # Sri Lanka
        (6.9271, 79.8612, "Colombo"),
        # Bangladesh
        (23.8103, 90.4125, "Dhaka"),
        (22.3569, 91.7832, "Chittagong"),
        # India (South/East)
        (13.0827, 80.2707, "Chennai"),
        (12.9716, 77.5946, "Bangalore"),
        (17.3850, 78.4867, "Hyderabad"),
        (22.5726, 88.3639, "Kolkata"),
        (9.9312, 76.2673, "Kochi"),
        (26.1445, 91.7362, "Guwahati"),
        (25.6093, 85.1376, "Patna"),
        (19.0760, 72.8777, "Mumbai"),
        # Maldives
        (4.1755, 73.5093, "Male"),
        # Bhutan
        (27.4728, 89.6390, "Thimphu"),
        # Nepal
        (27.7172, 85.3240, "Kathmandu"),
        # South China
        (23.1291, 113.2644, "Guangzhou"),
        (22.5431, 114.0579, "Shenzhen"),
        (25.2330, 110.3060, "Guilin"),
        (22.8200, 108.3200, "Nanning"),
        # Japan (nearby)
        (35.6762, 139.6503, "Tokyo"),
        (34.6937, 135.5023, "Osaka"),
        (26.3344, 127.8007, "Okinawa"),
        # South Korea (nearby)
        (37.5665, 126.9780, "Seoul"),
        # Papua New Guinea
        (-6.2141, 155.8817, "Bougainville"),
        (-5.4477, 145.7860, "Madang"),
        # Guam/Pacific
        (13.4443, 144.7937, "Guam"),
        (15.1850, 145.7457, "Saipan"),
        (7.3463, 134.4790, "Palau"),
        # Mongolia
        (47.9184, 106.9177, "Ulaanbaatar"),
        # China (various)
        (30.5728, 104.0668, "Chengdu"),
        (29.5630, 106.5516, "Chongqing"),
        (30.2741, 120.1551, "Hangzhou"),
        (31.2304, 121.4737, "Shanghai"),
        (32.0603, 118.7969, "Nanjing"),
        (34.2619, 108.9428, "Xi'an"),
        (30.5928, 114.3055, "Wuhan"),
        (28.2280, 112.9388, "Changsha"),
        (36.0671, 120.3826, "Qingdao"),
        (25.0389, 102.7183, "Kunming"),
        (26.6470, 106.6302, "Guiyang"),
        (29.8683, 121.5440, "Ningbo"),
        (24.4798, 118.0894, "Xiamen"),
        (26.0745, 119.2965, "Fuzhou"),
    ],
    "EUROPE": [
        # UK
        (51.5074, -0.1278, "London"),
        (53.4808, -2.2426, "Manchester"),
        (52.4862, -1.8904, "Birmingham"),
        (55.9533, -3.1883, "Edinburgh"),
        (51.4545, -2.5879, "Bristol"),
        (53.8008, -1.5491, "Leeds"),
        (50.3755, -4.1427, "Plymouth"),
        # France
        (48.8566, 2.3522, "Paris"),
        (45.7640, 4.8357, "Lyon"),
        (43.2965, 5.3698, "Marseille"),
        (47.2184, -1.5536, "Nantes"),
        (43.6047, 1.4442, "Toulouse"),
        (48.5734, 7.7521, "Strasbourg"),
        (44.8378, -0.5792, "Bordeaux"),
        (43.7102, 7.2620, "Nice"),
        (50.6292, 3.0573, "Lille"),
        (45.1885, 5.7245, "Grenoble"),
        (35.1740, -1.2854, "Rennes"),
        # Germany
        (52.5200, 13.4050, "Berlin"),
        (50.1109, 8.6821, "Frankfurt"),
        (48.1351, 11.5820, "Munich"),
        (53.5511, 9.9937, "Hamburg"),
        (51.2277, 6.7735, "Dusseldorf"),
        (50.9375, 6.9603, "Cologne"),
        (48.7758, 9.1829, "Stuttgart"),
        (51.0504, 13.7373, "Dresden"),
        (54.3233, 10.1228, "Kiel"),
        (52.2689, 8.0479, "Bielefeld"),
        (49.4521, 11.0767, "Nuremberg"),
        # Italy
        (41.9028, 12.4964, "Rome"),
        (45.4642, 9.1900, "Milan"),
        (40.8518, 14.2681, "Naples"),
        (43.7696, 11.2558, "Florence"),
        (44.4949, 11.3426, "Bologna"),
        (45.4384, 10.9916, "Verona"),
        (45.0703, 7.6869, "Turin"),
        (45.4064, 11.8768, "Padova"),
        (44.4056, 8.9463, "Genova"),
        (40.3515, 18.1718, "Lecce"),
        (39.2238, 9.1217, "Cagliari"),
        # Spain
        (40.4168, -3.7038, "Madrid"),
        (41.3874, 2.1686, "Barcelona"),
        (37.3891, -5.9845, "Seville"),
        (39.4699, -0.3763, "Valencia"),
        (36.7213, -4.4217, "Malaga"),
        (43.2630, -2.9350, "Bilbao"),
        (42.8782, -8.5448, "Santiago"),
        (28.1235, -15.4363, "Las Palmas"),
        (38.3452, -0.4810, "Alicante"),
        # Netherlands
        (52.3676, 4.9041, "Amsterdam"),
        (51.9225, 4.4792, "Rotterdam"),
        (52.0907, 5.1214, "Utrecht"),
        (52.3792, 6.9006, "Enschede"),
        (51.4416, 5.4697, "Eindhoven"),
        # Belgium
        (50.8503, 4.3517, "Brussels"),
        (51.2194, 4.4025, "Antwerp"),
        (51.0543, 3.7174, "Ghent"),
        # Switzerland
        (47.3769, 8.5417, "Zurich"),
        (46.2044, 6.1432, "Geneva"),
        (46.9480, 7.4474, "Bern"),
        (47.5596, 7.5886, "Basel"),
        (46.0037, 8.9511, "Lugano"),
        # Austria
        (48.2082, 16.3738, "Vienna"),
        (47.2692, 11.4041, "Innsbruck"),
        (47.8095, 13.0550, "Salzburg"),
        (47.0707, 15.4395, "Graz"),
        (46.6247, 14.3089, "Klagenfurt"),
        # Czech Republic
        (50.0755, 14.4378, "Prague"),
        (49.1951, 16.6068, "Brno"),
        (49.8209, 18.2625, "Ostrava"),
        (50.7663, 15.0543, "Liberec"),
        # Poland
        (52.2297, 21.0122, "Warsaw"),
        (50.0647, 19.9450, "Krakow"),
        (51.7592, 19.4560, "Lodz"),
        (54.3520, 18.6466, "Gdansk"),
        (51.1079, 17.0385, "Wroclaw"),
        (53.1235, 18.0084, "Bydgoszcz"),
        (51.2465, 22.5684, "Lublin"),
        # Hungary
        (47.4979, 19.0402, "Budapest"),
        (46.2530, 20.1414, "Szeged"),
        (47.6875, 17.6504, "Gyor"),
        (46.0727, 18.2323, "Pecs"),
        # Slovakia
        (48.1486, 17.1077, "Bratislava"),
        (48.7164, 21.2611, "Kosice"),
        # Slovenia
        (46.0569, 14.5058, "Ljubljana"),
        (46.5547, 15.6459, "Maribor"),
        # Croatia
        (45.8150, 15.9819, "Zagreb"),
        (43.5081, 16.4402, "Split"),
        (45.3271, 14.4422, "Rijeka"),
        # Romania
        (44.4268, 26.1025, "Bucharest"),
        (46.7712, 23.6236, "Cluj-Napoca"),
        (45.7489, 21.2087, "Timisoara"),
        (47.1585, 27.6014, "Iasi"),
        # Bulgaria
        (42.6977, 23.3219, "Sofia"),
        (42.1354, 24.7453, "Plovdiv"),
        (43.2141, 27.9147, "Varna"),
        # Greece
        (37.9838, 23.7275, "Athens"),
        (40.6401, 22.9444, "Thessaloniki"),
        (35.3387, 25.1442, "Heraklion"),
        # Serbia
        (44.7866, 20.4489, "Belgrade"),
        (45.2671, 19.8335, "Novi Sad"),
        # Bosnia
        (43.8563, 18.4131, "Sarajevo"),
        (44.7722, 17.1910, "Banja Luka"),
        # Ireland
        (53.3498, -6.2603, "Dublin"),
        (51.8985, -8.4756, "Cork"),
        # Portugal
        (38.7223, -9.1393, "Lisbon"),
        (41.1579, -8.6291, "Porto"),
        # Nordics
        (59.3293, 18.0686, "Stockholm"),
        (59.9139, 10.7522, "Oslo"),
        (55.6761, 12.5683, "Copenhagen"),
        (60.1699, 24.9384, "Helsinki"),
        (64.1466, -21.9426, "Reykjavik"),
        (57.7089, 11.9746, "Gothenburg"),
        (63.8258, 20.2630, "Umea"),
        (60.3913, 5.3221, "Bergen"),
        (63.4305, 10.3951, "Trondheim"),
        (61.4978, 23.7610, "Tampere"),
        (60.4518, 22.2666, "Turku"),
        # Baltic
        (56.9496, 24.1052, "Riga"),
        (54.6872, 25.2797, "Vilnius"),
        (59.4370, 24.7536, "Tallinn"),
        # Ukraine
        (50.4501, 30.5234, "Kyiv"),
        (49.8397, 24.0297, "Lviv"),
        (48.4647, 35.0462, "Dnipro"),
        (46.4825, 30.7233, "Odessa"),
        # Turkey
        (41.0082, 28.9784, "Istanbul"),
        (39.9334, 32.8597, "Ankara"),
        (38.4192, 27.1287, "Izmir"),
        (36.8969, 30.7133, "Antalya"),
        # Russia (European)
        (55.7558, 37.6173, "Moscow"),
        (59.9343, 30.3351, "St Petersburg"),
        (56.8519, 60.6122, "Yekaterinburg"),
        (54.7388, 55.9721, "Ufa"),
        (56.3287, 44.0020, "Nizhny Novgorod"),
        (55.7879, 49.1233, "Kazan"),
        # Andorra
        (42.5063, 1.5218, "Andorra"),
        # Malta
        (35.8989, 14.5146, "Malta"),
        # Cyprus
        (35.1856, 33.3823, "Nicosia"),
        # Luxembourg
        (49.6116, 6.1319, "Luxembourg"),
        # Liechtenstein
        (47.1410, 9.5215, "Vaduz"),
        # Monaco
        (43.7384, 7.4246, "Monaco"),
        # Montenegro
        (42.4304, 19.2594, "Podgorica"),
        # North Macedonia
        (41.9981, 21.4254, "Skopje"),
        # Albania
        (41.3275, 19.8187, "Tirana"),
        # Kosovo
        (42.6629, 21.1655, "Pristina"),
        # Moldova
        (47.0105, 28.8638, "Chisinau"),
        # Georgia
        (41.7151, 44.8271, "Tbilisi"),
        # Armenia
        (40.1872, 44.5152, "Yerevan"),
        # Azerbaijan
        (40.4093, 49.8671, "Baku"),
    ],
    "US": [
        # US West
        (37.7749, -122.4194, "San Francisco"),
        (34.0522, -118.2437, "Los Angeles"),
        (47.6062, -122.3321, "Seattle"),
        (45.5051, -122.6750, "Portland"),
        (32.7157, -117.1611, "San Diego"),
        (36.1699, -115.1398, "Las Vegas"),
        (33.4484, -112.0740, "Phoenix"),
        (40.7608, -111.8910, "Salt Lake City"),
        (39.7392, -104.9903, "Denver"),
        (43.6150, -116.2023, "Boise"),
        (46.8721, -113.9940, "Missoula"),
        (38.5816, -121.4944, "Sacramento"),
        (36.7783, -119.4179, "Fresno"),
        (36.1627, -86.7816, "Nashville"),
        (35.1495, -90.0490, "Memphis"),
        # US Central
        (41.8781, -87.6298, "Chicago"),
        (29.7604, -95.3698, "Houston"),
        (32.7767, -96.7970, "Dallas"),
        (29.4241, -98.4936, "San Antonio"),
        (30.2672, -97.7431, "Austin"),
        (39.0997, -94.5786, "Kansas City"),
        (44.9778, -93.2650, "Minneapolis"),
        (43.0389, -87.9065, "Milwaukee"),
        (39.7684, -86.1581, "Indianapolis"),
        (40.4406, -79.9959, "Pittsburgh"),
        (39.9612, -82.9988, "Columbus"),
        (38.6270, -90.1994, "St Louis"),
        (41.2524, -95.9980, "Omaha"),
        (35.4676, -97.5164, "Oklahoma City"),
        (36.1540, -95.9928, "Tulsa"),
        (37.6879, -97.3375, "Wichita"),
        (34.7465, -92.2896, "Little Rock"),
        (39.5501, -105.7821, "Colorado"),
        # US East
        (40.7128, -74.0060, "New York"),
        (42.3601, -71.0589, "Boston"),
        (39.9526, -75.1652, "Philadelphia"),
        (38.9072, -77.0369, "Washington DC"),
        (35.2271, -80.8431, "Charlotte"),
        (33.7490, -84.3880, "Atlanta"),
        (25.7617, -80.1918, "Miami"),
        (28.5383, -81.3792, "Orlando"),
        (27.9506, -82.4572, "Tampa"),
        (30.3322, -81.6557, "Jacksonville"),
        (36.8529, -75.9780, "Virginia Beach"),
        (36.1627, -86.7816, "Nashville"),
        (39.2904, -76.6122, "Baltimore"),
        (42.3314, -83.0458, "Detroit"),
        (41.4993, -81.6944, "Cleveland"),
        (43.0481, -76.1474, "Syracuse"),
        (40.4406, -79.9959, "Pittsburgh"),
        (37.5407, -77.4360, "Richmond"),
        (35.7796, -78.6382, "Raleigh"),
        (32.7765, -79.9311, "Charleston"),
        (32.0809, -81.0912, "Savannah"),
        (30.4515, -91.1871, "Baton Rouge"),
        (29.9511, -90.0715, "New Orleans"),
        (33.5207, -86.8025, "Birmingham"),
        (32.3792, -86.3077, "Montgomery"),
        (30.4383, -84.2807, "Tallahassee"),
        (26.1224, -80.1373, "Fort Lauderdale"),
        # US Mountain/Plains
        (46.8772, -96.7898, "Fargo"),
        (46.8083, -100.7837, "Bismarck"),
        (44.3683, -100.3510, "Pierre"),
        (43.5546, -96.7311, "Sioux Falls"),
        (42.0308, -93.6319, "Ames"),
        (41.2565, -95.9345, "Omaha"),
        (41.5868, -93.6250, "Des Moines"),
        (40.8136, -96.7026, "Lincoln"),
        (38.9717, -95.2353, "Lawrence"),
        (41.1400, -104.8202, "Cheyenne"),
        (42.8666, -106.3131, "Casper"),
        (35.0844, -106.6504, "Albuquerque"),
        (32.2226, -110.9747, "Tucson"),
        (31.7619, -106.4850, "El Paso"),
        # Alaska & Hawaii
        (61.2181, -149.9003, "Anchorage"),
        (64.8378, -147.7164, "Fairbanks"),
        (21.3069, -157.8583, "Honolulu"),
        # Canada (West)
        (49.2827, -123.1207, "Vancouver"),
        (51.0447, -114.0719, "Calgary"),
        (53.5461, -113.4938, "Edmonton"),
        (50.4452, -104.6189, "Regina"),
        (49.8951, -97.1384, "Winnipeg"),
        # Canada (Central/East)
        (43.6532, -79.3832, "Toronto"),
        (45.5017, -73.5673, "Montreal"),
        (45.4215, -75.6972, "Ottawa"),
        (46.8139, -71.2080, "Quebec City"),
        (44.6488, -63.5752, "Halifax"),
        (47.5615, -52.7126, "St Johns"),
        # Mexico
        (19.4326, -99.1332, "Mexico City"),
        (20.6597, -103.3496, "Guadalajara"),
        (25.6866, -100.3161, "Monterrey"),
        (31.6904, -106.4245, "Ciudad Juarez"),
        (28.6353, -106.0889, "Chihuahua"),
        (21.1619, -86.8515, "Cancun"),
        (20.9674, -89.5926, "Merida"),
        (32.5149, -117.0382, "Tijuana"),
        (24.1426, -110.3128, "La Paz"),
        (19.1738, -96.1342, "Veracruz"),
        (25.4267, -100.9942, "Saltillo"),
        # Caribbean
        (18.4655, -66.1057, "San Juan"),
        (18.1096, -77.2975, "Kingston"),
        (25.0343, -77.3963, "Nassau"),
        (19.4517, -70.6970, "Santiago DR"),
        (18.4861, -69.9312, "Santo Domingo"),
        (10.5000, -66.9167, "Caracas"),
        (10.6918, -61.2225, "Port of Spain"),
        # Central America
        (14.6349, -90.5069, "Guatemala City"),
        (13.6929, -89.2182, "San Salvador"),
        (14.0723, -87.1921, "Tegucigalpa"),
        (12.1150, -86.2362, "Managua"),
        (9.9281, -84.0907, "San Jose CR"),
        (8.9824, -79.5199, "Panama City"),
        (17.2510, -88.7590, "Belmopan"),
        (18.5944, -72.3074, "Port-au-Prince"),
    ],
}

# Country code to region mapping for classification
REGION_COUNTRIES = {
    "ASEAN": [
        "ID", "SG", "MY", "TH", "VN", "PH", "KH", "MM", "LA", "BN", "TL",  # ASEAN
        "TW", "HK", "MO",  # East Asia (nearby)
        "AU", "NZ", "PG", "FJ", "WS", "TO", "VU", "SB", "KI", "TV", "NR", "MH", "FM", "PW", "GU", "MP", "AS", "CK", "NU", "TK", "WF", "NC", "PF",  # Oceania
        "LK", "MV", "NP", "BT",  # South Asia
        "BD", "IN",  # South/Southeast Asia
        "CN",  # China
        "JP", "KR", "KP", "MN",  # East Asia
    ],
    "EUROPE": [
        "GB", "FR", "DE", "IT", "ES", "PT", "NL", "BE", "CH", "AT", "LI", "LU", "MC", "AD", "SM", "VA",  # Western Europe
        "SE", "NO", "DK", "FI", "IS", "FO", "AX", "SJ", "GL",  # Nordics
        "IE",  # Ireland
        "PL", "CZ", "SK", "HU", "RO", "BG", "HR", "SI", "RS", "BA", "ME", "MK", "AL", "XK",  # Central/Eastern Europe
        "EE", "LV", "LT",  # Baltics
        "UA", "MD", "BY",  # Eastern Europe
        "RU",  # Russia
        "TR", "GE", "AM", "AZ", "CY",  # Eurasia
        "MT",  # Malta
        "GR",  # Greece
    ],
    "US": [
        "US", "CA", "MX",  # North America
        "PR", "VI", "GU", "AS", "MP", "UM",  # US Territories
        "GT", "SV", "HN", "NI", "CR", "PA", "BZ",  # Central America
        "JM", "HT", "DO", "CU", "BS", "BB", "TT", "GD", "AG", "DM", "KN", "LC", "VC", "AW", "CW", "SX", "BQ",  # Caribbean
        "CO", "VE", "EC", "PE", "BO", "PY", "UY", "AR", "CL", "BR", "GY", "SR", "GF",  # South America
        "BM",  # Bermuda
    ],
}


def get_region_for_country(cc):
    """Determine which region file a country belongs to."""
    for region, countries in REGION_COUNTRIES.items():
        if cc in countries:
            return region
    # Default: try to assign based on continent
    return None


def fetch_servers(lat, lon, retries=3):
    """Fetch servers from Ookla API for given coordinates."""
    url = f"https://www.speedtest.net/api/js/servers?engine=js&limit=100&lat={lat}&lon={lon}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://www.speedtest.net/",
    }
    
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode())
                return data
        except Exception as e:
            if attempt < retries - 1:
                print(f"  Retry {attempt + 1} for ({lat}, {lon}): {e}")
                time.sleep(2)
            else:
                print(f"  Failed ({lat}, {lon}): {e}")
                return []


def extract_host(server):
    """Extract the hostname from a server entry."""
    host = server.get("host", "")
    # Remove port number
    if ":" in host:
        host = host.split(":")[0]
    # Remove .prod.hosts.ooklaserver.net suffix
    if host.endswith(".prod.hosts.ooklaserver.net"):
        host = host.replace(".prod.hosts.ooklaserver.net", "")
    return host


def main():
    print("=" * 60)
    print("Fetching Ookla Speedtest.net Server List")
    print("=" * 60)
    
    # Collect all servers by region
    all_servers = {"ASEAN": {}, "EUROPE": {}, "US": {}}
    
    for region, points in QUERY_POINTS.items():
        print(f"\n--- Fetching {region} servers ({len(points)} query points) ---")
        for i, (lat, lon, desc) in enumerate(points):
            print(f"  [{i+1}/{len(points)}] Querying {desc} ({lat}, {lon})...")
            servers = fetch_servers(lat, lon)
            new_count = 0
            for server in servers:
                host = extract_host(server)
                cc = server.get("cc", "")
                
                if not host or host == "":
                    continue
                
                # Determine the correct region for this server
                server_region = get_region_for_country(cc)
                if server_region is None:
                    server_region = region  # Default to query region
                
                if host not in all_servers[server_region]:
                    all_servers[server_region][host] = {
                        "host": host,
                        "name": server.get("name", ""),
                        "country": server.get("country", ""),
                        "cc": cc,
                        "sponsor": server.get("sponsor", ""),
                        "id": server.get("id", ""),
                    }
                    new_count += 1
            
            print(f"    Found {len(servers)} servers, {new_count} new")
            time.sleep(0.3)  # Be polite to the API
    
    # Write .rsc files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for region, servers in all_servers.items():
        filename = os.path.join(base_dir, f"{region} server-speedtest.net.rsc")
        sorted_hosts = sorted(servers.values(), key=lambda x: (x["country"], x["name"], x["host"]))
        
        print(f"\n--- Writing {region} ({len(sorted_hosts)} servers) to {filename} ---")
        
        with open(filename, "wb") as f:
            f.write(b"/ip firewall address-list\r\n")
            for srv in sorted_hosts:
                line = f"add list=speedtest address={srv['host']}\r\n"
                f.write(line.encode("utf-8"))
            f.write(b"\r\n")
        
        print(f"  Written {len(sorted_hosts)} entries")
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    for region, servers in all_servers.items():
        print(f"  {region}: {len(servers)} servers")
    print(f"  Total: {sum(len(s) for s in all_servers.values())} servers")
    print("=" * 60)


if __name__ == "__main__":
    main()
