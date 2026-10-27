def adjust_stock(stock, sku, delta):
    quantity = stock[sku] + delta
    if quantity < 0:
        raise ValueError('Negative stock')
    stock[sku] = quantity
    return quantity
