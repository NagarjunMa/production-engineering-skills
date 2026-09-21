DEFAULT_LIMIT = 12


def validate_limit(limit):
    if type(limit) is not int or limit <= 0:
        raise ValueError("limit must be a positive integer")
    return limit


def normalize_text(text, limit=DEFAULT_LIMIT):
    validate_limit(limit)
    if len(text) > limit:
        raise ValueError("text exceeds limit")
    return text.strip().upper()
