def web_tag(value):
    tag = value.strip().lower()
    if not tag:
        return 422, {"error": {"message": "empty tag"}}
    return 200, {"tag": tag}


def cli_tag(value):
    tag = value.strip().lower()
    if not tag:
        return 2, "error: empty tag"
    return 0, tag
