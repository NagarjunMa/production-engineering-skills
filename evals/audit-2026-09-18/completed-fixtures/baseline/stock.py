def adjust_stock(stock, sku, delta):
    new_quantity = stock[sku] + delta
    if new_quantity < 0:
        raise ValueError("Negative stock")
    stock[sku] = new_quantity
    return new_quantity


def adjust_many(stock, adjustments):
    """Apply ordered adjustments atomically and return touched quantities."""
    tentative = stock.copy()
    final_quantities = {}
    for sku, delta in adjustments:
        final_quantities[sku] = adjust_stock(tentative, sku, delta)
    stock.update(final_quantities)
    return final_quantities
