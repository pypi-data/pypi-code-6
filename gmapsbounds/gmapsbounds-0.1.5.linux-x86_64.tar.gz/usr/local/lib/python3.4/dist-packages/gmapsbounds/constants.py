USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"
)

ZOOM_OUT = {
	'37.7577, -122.4376': 'San Francisco, CA'
}

MAX_NODE_DIFFERENCE = 125
MAX_NODE_BACKTRACK = 500

#Ny, Sy, Wx, Ex
MENU_BORDERS = [[15, 123], [30, 429]]
MENU_BORDERS_WITH_ADS = [[15, 447], [30, 429]]

WATER_RED = list(range(148, 185))
WATER_GREEN = list(range(193, 215))
WATER_BLUE = list(range(253, 256))

ALLOWABLE_RED = list(range(218, 241))
ALLOWABLE_GREEN = list(range(0, 191))
ALLOWABLE_BLUE = list(range(65, 181))

MAX_BLUE_GREEN_DIFFERENCE = 20

VALID = [[232, 151, 142], [237, 162, 155]]
INVALID = [[215, 60, 48], [218, 97, 97], [179, 56, 44], [180, 56, 44]]
# Highway signs (domestic), Hospitals, Highway signs (foreign), city names

MINIMUM_PRUNING_SIZE = 15