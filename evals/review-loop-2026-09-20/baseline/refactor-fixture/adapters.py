from helpers import normalize_tag


def web_tag(value):
    try:
        tag = normalize_tag(value)
    except ValueError as exc:
        return 422, {"error": {"message": str(exc)}}
    return 200, {"tag": tag}


def cli_tag(value):
    try:
        tag = normalize_tag(value)
    except ValueError as exc:
        return 2, "error: " + str(exc)
    return 0, tag
