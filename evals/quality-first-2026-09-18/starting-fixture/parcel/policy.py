def fee_cents(subtotal):
    if type(subtotal) is not int or subtotal < 0:
        raise ValueError("invalid subtotal")
    return 0 if subtotal >= 5000 else 499
