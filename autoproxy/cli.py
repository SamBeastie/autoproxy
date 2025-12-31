import argparse
import sys
from .deckparse import parse_decklist
from .scryfall import enrich_deck
from .render import render_pdf

def main():
    parser = argparse.ArgumentParser(
        description="Generate minimalist MTG proxy PDFs from decklists"
    )
    parser.add_argument("-f", "--file", help="Decklist file")
    parser.add_argument("-o", "--output", help="Output PDF filename")
    parser.add_argument("--no-bar", action="store_true", help="Disable color bar")
    parser.add_argument("--no-dots", action="store_true", help="Disable mana dots")
    args = parser.parse_args()

    # Input
    if args.file:
        with open(args.file) as f:
            deck_text = f.read()
        deck_name = args.output or args.file.rsplit(".", 1)[0]
        print(f"[INFO] Loaded decklist from {args.file} ({len(deck_text.splitlines())} lines).")
    elif not sys.stdin.isatty():
        deck_text = sys.stdin.read()
        deck_name = "deck"
        print(f"[INFO] Received decklist from stdin ({len(deck_text.splitlines())} lines).")
    else:
        deck_name = input("Deck name: ").strip()
        print("Paste decklist below. End input with Ctrl-D (Unix) or Ctrl-Z+Enter (Windows):")
        deck_text = sys.stdin.read()
        print(f"[INFO] Finished reading decklist ({len(deck_text.splitlines())} lines).")

    # Determine output file
    output_file = args.output or f"{deck_name.replace(' ', '_').lower()}.pdf"

    # Parse deck and fetch Scryfall data
    deck = parse_decklist(deck_text)
    enrich_deck(deck)

    # Render PDF
    render_pdf(
        deck,
        output_file=output_file,
        draw_bar=not args.no_bar,
        draw_dots=not args.no_dots
    )

    print(f"[SUCCESS] Generated PDF: {output_file}")

if __name__ == "__main__":
    main()

