def web_error(message):
    return 400, {"error": {"message": message}}


def cli_error(message):
    return 2, "error: " + message
