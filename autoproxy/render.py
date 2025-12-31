import re
import textwrap
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from . import constants as C

def fit_text(c, text, max_width):
    size = C.MAX_FONT
    while c.stringWidth(text, C.FONT, size) > max_width and size > C.MIN_FONT:
        size -= 0.25
    return size

def draw_card(c, x, y, card, draw_bar=True, draw_dots=True):
    # Border
    c.setStrokeColor(colors.black)
    c.rect(x, y, C.CARD_WIDTH, C.CARD_HEIGHT)

    # Name + mana cost
    top_y = y + C.CARD_HEIGHT - C.TEXT_MARGIN - C.MAX_FONT
    mana_w = c.stringWidth(card["mana_cost"], C.FONT, C.MAX_FONT)
    name_size = fit_text(c, card["name"], C.CARD_WIDTH - mana_w - 3*C.TEXT_MARGIN)
    c.setFont(C.FONT, name_size)
    c.setFillColor(colors.black)
    c.drawString(x + C.TEXT_MARGIN, top_y, card["name"])
    c.setFont(C.FONT, C.MAX_FONT)
    mana_x = x + C.CARD_WIDTH - C.TEXT_MARGIN - mana_w
    c.drawString(mana_x, top_y, card["mana_cost"])

    # Mana dots
    if draw_dots:
        c.saveState()
        dot_y = top_y - 4
        dot_r = 2
        symbols = re.findall(r"\{([^}]+)\}", card["mana_cost"])
        cursor = mana_x
        for sym in symbols:
            w = c.stringWidth("{" + sym + "}", C.FONT, C.MAX_FONT)
            cx = cursor + w / 2
            col = C.MANA_DOT_MAP.get(sym.upper(), None)
            if col:
                if col == C.MANA_DOT_MAP.get("W"):
                    c.setFillColor(colors.whitesmoke)
                    c.setStrokeColor(colors.black)
                    c.circle(cx, dot_y, dot_r, fill=1, stroke=1)
                else:
                    c.setFillColor(col)
                    c.circle(cx, dot_y, dot_r, fill=1, stroke=0)
            else:
                c.setFillColor(colors.gray)
                c.circle(cx, dot_y, dot_r, fill=1, stroke=0)
            cursor += w
        c.restoreState()

    # Type line
    type_y = top_y - C.MAX_FONT*1.6
    type_size = fit_text(c, card["type_line"], C.CARD_WIDTH - 2*C.TEXT_MARGIN)
    c.setFont(C.FONT, type_size)
    c.setFillColor(colors.black)
    c.drawString(x + C.TEXT_MARGIN, type_y, card["type_line"])

    # Color bar
    bar_y = type_y - 6
    bar_h = 3
    bar_x = x + C.TEXT_MARGIN
    bar_w = C.CARD_WIDTH - 2*C.TEXT_MARGIN
    if draw_bar:
        c.saveState()
        if card["is_land"]:
            colors_out = card["produced_mana"]
            if colors_out:
                seg_w = bar_w / len(colors_out)
                for i, col in enumerate(colors_out):
                    c.setFillColor(C.COLOR_BAR_MAP.get(col, colors.gray))
                    c.rect(bar_x + i*seg_w, bar_y, seg_w, bar_h, fill=1, stroke=0)
            else:
                c.setFillColor(colors.gray)
                c.rect(bar_x, bar_y, bar_w, bar_h, fill=1, stroke=0)
        else:
            if not card["colors"]:
                c.setFillColor(colors.gray)
            elif len(card["colors"]) == 1:
                c.setFillColor(C.COLOR_BAR_MAP.get(card["colors"][0], colors.gray))
            else:
                c.setFillColor(colors.gold)
            c.rect(bar_x, bar_y, bar_w, bar_h, fill=1, stroke=0)
        c.restoreState()

    # Bottom line
    bottom_y = y + C.TEXT_MARGIN
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)
    rarity = C.RARITY_MAP.get(card["rarity"], "?")
    c.setFont(C.FONT, C.MAX_FONT)
    c.drawString(x + C.TEXT_MARGIN, bottom_y, f"{card['set']} {rarity}")
    if card["power"]:
        pt = f"{card['power']}/{card['toughness']}"
        c.drawString(
            x + C.CARD_WIDTH - C.TEXT_MARGIN - c.stringWidth(pt, C.FONT, C.MAX_FONT),
            bottom_y,
            pt
        )

    # Oracle text
    oracle_top = bar_y - 6
    oracle_bottom = bottom_y + C.MAX_FONT*1.4
    oracle_h = oracle_top - oracle_bottom
    oracle_w = C.CARD_WIDTH - 2*C.TEXT_MARGIN

    lines = []
    for l in card["oracle_text"].split("\n"):
        lines.extend(textwrap.wrap(l, 40) or [""])
    oracle = "\n".join(lines)

    style = ParagraphStyle(
        "oracle",
        fontName=C.FONT,
        fontSize=C.MAX_FONT,
        leading=C.MAX_FONT*1.2
    )
    p = Paragraph(oracle, style)
    w, h = p.wrap(oracle_w, oracle_h)
    if h > oracle_h:
        scale = oracle_h / h
        style.fontSize = max(C.MIN_FONT, C.MAX_FONT*scale)
        style.leading = style.fontSize*1.2
        p = Paragraph(oracle, style)
        w, h = p.wrap(oracle_w, oracle_h)
    c.setFillColor(colors.black)
    p.drawOn(c, x + C.TEXT_MARGIN, oracle_bottom + (oracle_h - h)/2)

def render_pdf(deck, output_file="deck.pdf", draw_bar=True, draw_dots=True):
    from reportlab.lib.pagesizes import letter
    c = canvas.Canvas(output_file, pagesize=letter)
    page_w, page_h = letter
    cards = []
    for d in deck:
        cards.extend([d]*d["count"])
    for i in range(0, len(cards), 9):
        for idx, card in enumerate(cards[i:i+9]):
            col = idx % 3
            row = idx // 3
            x = C.PAGE_MARGIN + col * C.CARD_WIDTH
            y = page_h - C.PAGE_MARGIN - (row + 1) * C.CARD_HEIGHT
            draw_card(c, x, y, card, draw_bar=draw_bar, draw_dots=draw_dots)
        c.showPage()
    c.save()

