def adjust_stock(stock, sku, delta):
    quantity = stock[sku] + delta
    if quantity < 0:
        raise ValueError('Negative stock')
    stock[sku] = quantity
    return quantity


def adjust_many(stock, adjustments):
    tentative = stock.copy()
    touched = {}
    for sku, delta in adjustments:
        touched[sku] = adjust_stock(tentative, sku, delta)
    stock.update(touched)
    return touched
