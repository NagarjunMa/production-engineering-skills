from parcel.policy import fee_cents


def web_quote(subtotal):
    try:
        return {"status": 200, "fee_cents": fee_cents(subtotal)}
    except ValueError:
        return {"status": 400, "error": "invalid subtotal"}
