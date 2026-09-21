def adjust_stock(stock, sku, delta):
    new_quantity = stock[sku] + delta
    if new_quantity < 0:
        raise ValueError("Negative stock")
    stock[sku] = new_quantity
    return new_quantity
