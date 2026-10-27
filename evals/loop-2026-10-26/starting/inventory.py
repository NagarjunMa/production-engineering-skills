def adjust_stock(stock, sku, delta):
    stock[sku] += delta
    if stock[sku] < 0:
        raise ValueError('Negative stock')
    return stock[sku]
