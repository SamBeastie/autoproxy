from reportlab.lib import colors
from reportlab.lib.units import inch

# Layout
CARD_WIDTH = 2.5 * inch
CARD_HEIGHT = 3.5 * inch
PAGE_MARGIN = 0.25 * inch
TEXT_MARGIN = 0.1 * inch

FONT = "Courier"
MAX_FONT = 10
MIN_FONT = 5

# Rarity mapping
RARITY_MAP = {
    "COMMON": "C",
    "UNCOMMON": "U",
    "RARE": "R",
    "MYTHIC": "M"
}

# Color bar
COLOR_BAR_MAP = {
    "W": colors.whitesmoke,
    "U": colors.lightblue,
    "B": colors.lightgrey,
    "R": colors.pink,
    "G": colors.lightgreen
}

# Mana dots
MANA_DOT_MAP = {
    "W": colors.white,
    "U": colors.blue,
    "B": colors.black,
    "R": colors.red,
    "G": colors.green
}

