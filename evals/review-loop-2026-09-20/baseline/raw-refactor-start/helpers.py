def normalize_tag(value):
    tag = value.strip().lower()
    if not tag:
        raise ValueError("empty tag")
    return tag
