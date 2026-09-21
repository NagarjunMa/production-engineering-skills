from parcel.policy import fee_cents


def web_quote(subtotal):
    try:
        return {"status": 200, "fee_cents": fee_cents(subtotal)}
    except ValueError:
        return {"status": 400, "error": "invalid subtotal"}


def web_quotes(subtotals):
    """Return independent web responses in input order without changing inputs."""
    return [web_quote(subtotal) for subtotal in subtotals]
