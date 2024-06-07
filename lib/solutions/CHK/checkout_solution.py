# noinspection PyUnusedLocal
# skus = unicode string

from dataclasses import dataclass

@dataclass(frozen=True)
class PricePoint:
    sku: str
    quantity: int
    price: int

PRICE_POINTS = set([
    PricePoint('A', 1, 50),
    PricePoint('A', 3, 130),
    PricePoint('B', 1, 30),
    PricePoint('B', 2, 45),
    PricePoint('C', 1, 20),
    PricePoint('D', 1, 15),
])

def best_price_point(sku: str, quantity: int) -> PricePoint:
    """
    Finds the best price for the given SKU, given that
    the customer is buying at least `quantity` of the item.
    """
    price_points_for_sku = set(pp for pp in PRICE_POINTS if pp.sku == sku and pp.quantity >= quantity)
    return min(price_points_for_sku, key=lambda pp: pp.price / pp.quantity)

def checkout(skus: str):
    quantities = {}
    for sku in skus:
        if sku not in quantities:
            quantities[sku] = 0
        quantities[sku] += 1
    print(quantities)
    raise NotImplementedError()



