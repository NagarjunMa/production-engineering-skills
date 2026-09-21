def adjust_stock(stock, sku, delta):
    new_quantity = stock[sku] + delta
    if new_quantity < 0:
        raise ValueError("Negative stock")
    stock[sku] = new_quantity
    return new_quantity


def adjust_many(stock, adjustments):
    """Apply ordered adjustments atomically and return final touched quantities."""
    tentative = {}
    for sku, delta in adjustments:
        if sku not in tentative:
            tentative[sku] = stock[sku]
        adjust_stock(tentative, sku, delta)
    stock.update(tentative)
    return tentative
