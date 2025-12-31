#!/usr/bin/env python3
import argparse
import sys
import requests
from . import render

SCRYFALL_URL = "https://api.scryfall.com/cards/named"

def fetch_card_data(name):
    """Query Scryfall for a card and return a standardized dictionary."""
    resp = requests.get(SCRYFALL_URL, params={"fuzzy": name})
    if resp.status_code != 200:
        print(f"Warning: Could not fetch {name}, skipping.")
        return None
    data = resp.json()

    # Determine if this is a double-faced card
    card_faces_data = data.get("card_faces", None)
    faces = []
    if card_faces_data:
        for face in card_faces_data:
            faces.append({
                "name": face.get("name", ""),
                "mana_cost": face.get("mana_cost", ""),
                "type_line": face.get("type_line", ""),
                "oracle_text": face.get("oracle_text", ""),
                "colors": face.get("colors", []),
                "power": face.get("power", None),
                "toughness": face.get("toughness", None)
            })

    return {
        "name": data.get("name", ""),
        "mana_cost": data.get("mana_cost", ""),
        "type_line": data.get("type_line", ""),
        "oracle_text": data.get("oracle_text", ""),
        "colors": data.get("colors", []),
        "power": data.get("power", None),
        "toughness": data.get("toughness", None),
        "rarity": data.get("rarity", "?"),
        "set": data.get("set", ""),
        "is_land": "land" in data.get("type_line", "").lower(),
        "produced_mana": data.get("produced_mana", []),
        "count": 1,
        "card_faces": faces  # always a list
    }

def parse_plaintext_deck(lines):
    """Convert plaintext Moxfield decklist to a list of card dicts."""
    deck = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            print(f"Skipping invalid line: {line}")
            continue
        try:
            count = int(parts[0])
            name = parts[1]
        except ValueError:
            print(f"Skipping invalid line: {line}")
            continue

        card_data = fetch_card_data(name)
        if card_data:
            card_data["count"] = count
            deck.append(card_data)
    return deck

def main():
    parser = argparse.ArgumentParser(description="Minimalist MTG proxy generator")
    parser.add_argument("-f", "--file", help="Plaintext decklist file")
    parser.add_argument("-o", "--out-file", help="Output PDF filename", default="deck.pdf")
    parser.add_argument("--no-bar", action="store_true", help="Disable color bars")
    parser.add_argument("--no-dots", action="store_true", help="Disable mana dots")
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, "r") as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading file {args.file}: {e}")
            sys.exit(1)
        output_file = args.out_file
    else:
        output_file = input("Enter a name for the PDF: ").strip() or "deck.pdf"
        print("Paste your plaintext Moxfield decklist below (Ctrl+D to finish):")

        # Read exactly like before, but add feedback
        raw_input = sys.stdin.read()  # read until Ctrl+D
        print("\nInput received. Processing deck...")  # feedback
        lines = raw_input.splitlines()  # preserves empty lines and spacing

    deck = parse_plaintext_deck(lines)

    if not deck:
        print("No valid cards to render. Exiting.")
        sys.exit(1)

    print(f"Rendering PDF to {output_file}...")
    render.render_pdf(deck, output_file=output_file,
                      draw_bar=not args.no_bar,
                      draw_dots=not args.no_dots)
    print("Done!")

if __name__ == "__main__":
    main()

