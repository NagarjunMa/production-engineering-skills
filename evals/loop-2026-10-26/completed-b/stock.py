def adjust_stock(stock, sku, delta):
    quantity = stock[sku] + delta
    if quantity < 0:
        raise ValueError('Negative stock')
    stock[sku] = quantity
    return quantity


def adjust_many(stock, adjustments):
    tentative = stock.copy()
    quantities = {}
    for sku, delta in adjustments:
        quantities[sku] = adjust_stock(tentative, sku, delta)
    stock.update(quantities)
    return quantities
