def parse_decklist(text):
    """
    Parse plaintext decklist into list of dicts:
    [{"name": "Card Name", "count": 3}, ...]
    """
    deck = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        count, *name = line.split()
        deck.append({"name": " ".join(name), "count": int(count)})
    return deck

