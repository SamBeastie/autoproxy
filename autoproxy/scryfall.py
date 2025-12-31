import requests
import time

def fetch_card(card_name):
    """
    Fetch card JSON from Scryfall API
    """
    r = requests.get(f"https://api.scryfall.com/cards/named?exact={card_name}")
    time.sleep(0.1)
    if not r.ok:
        raise RuntimeError(f"Failed to fetch {card_name}")
    d = r.json()
    return {
        "mana_cost": d.get("mana_cost", ""),
        "oracle_text": d.get("oracle_text", ""),
        "type_line": d.get("type_line", ""),
        "colors": d.get("colors", []),
        "produced_mana": d.get("produced_mana", []),
        "rarity": d.get("rarity", "").upper(),
        "set": d.get("set", "").upper(),
        "power": d.get("power"),
        "toughness": d.get("toughness"),
        "is_land": "Land" in d.get("type_line", "")
    }

def enrich_deck(deck):
    """
    Fetch all Scryfall data for deck cards
    """
    for card in deck:
        data = fetch_card(card["name"])
        card.update(data)

