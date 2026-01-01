# autoproxy

**autoproxy** is a minimalist CLI tool for generating printable Magic: The Gathering proxy sheets from plaintext decklists.

It takes a plain text decklist (e.g. Moxfield export), fetches card data from Scryfall, and produces a clean 9-up PDF designed for home printing and cutting.

No art, just attractive, readable cards that use little ink to print.

---

## Features

- Plaintext decklist input (paste or file)
- Automatic Scryfall lookup
- Oracle text–only card layout
- 9 cards per US Letter page (poker size)
- Mana cost dots and subtle color bars (optional)
- Proper handling of double-faced cards (both faces rendered)
- Designed for monochrome or low-ink printing

---

## Installation

Clone this repo, then run `python3 autoproxy.cli` to test the interactive mode. Install with `pipx install -e .`.

AUR Packaging is planned for the near future.

## Usage
### Paste a deck list
Run `autoproxy` from your console. You'll be prompted for a deck name and deck list. After pasting, press Ctrl+D to send EOF character.

### From a file

`autoproxy -f deck.txt`
`autoproxy -o deck.pdf`

Point the input file to a plaintext file, and send the output to a PDF.

### Disable visual aids
With no options, cards are generated with a colored line to evoke the background color of a real card, and colored dots under the mana symbol. These can be disabled with:
`autoproxy --no-bar`
`autoproxy --no-dots`

### Deck list format
Any plaintext list with one card per line will work. For example:
```
1 Delver of Secrets
1 Lightning Bolt
1 Island
1 Mountain
```

Counts are optional. Defaults to 1.

## Notes
* Scryfall's public API
* Intended for personal use and playtesting
* Not at all affiliated with Wizards of the Coast

<p align="center">
  <img src="images/proxy-cards.png" alt="Sample proxy cards" width="700">
</p>