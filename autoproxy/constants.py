from reportlab.lib import colors

# Page and card dimensions (points)
# Letter page: 8.5"x11" = 612x792 points
PAGE_WIDTH = 612
PAGE_HEIGHT = 792

# Card size: standard poker ~2.5"x3.5" = 180x252 points (scaled slightly for margins)
CARD_WIDTH = 180
CARD_HEIGHT = 252

# Margins from page edge
PAGE_MARGIN = 12  # spacing around entire page

# Inner text margins from card border
TEXT_MARGIN = 6

# Font
FONT = "Courier"
MAX_FONT = 10
MIN_FONT = 6

# Mana dot radius
DOT_RADIUS = 2

# Rarity mapping (single-letter)
RARITY_MAP = {
    "common": "C",
    "uncommon": "U",
    "rare": "R",
    "mythic": "M"
}

# Mana dot color mapping
MANA_DOT_MAP = {
    "W": colors.whitesmoke,
    "U": colors.blue,
    "B": colors.black,
    "R": colors.red,
    "G": colors.green,
    "C": colors.gray,  # generic/colorless
}

# Color bar mapping (same as mana)
COLOR_BAR_MAP = {
    "W": colors.yellow,
    "U": colors.lightblue,
    "B": colors.darkgray,
    "R": colors.red,
    "G": colors.green,
    "C": colors.gray,
}

# Oracle text wrapping width (characters)
ORACLE_WRAP = 40

