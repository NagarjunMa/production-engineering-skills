DEFAULT_LIMIT = 12


def normalize_text(text, limit=DEFAULT_LIMIT):
    if len(text) > limit:
        raise ValueError("text exceeds limit")
    return text.strip().upper()
