from parcel.policy import fee_cents


def cli_quote(subtotal):
    try:
        return f"Shipping: {fee_cents(subtotal)} cents"
    except ValueError:
        return "Error: invalid subtotal"
