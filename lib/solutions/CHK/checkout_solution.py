# noinspection PyUnusedLocal
# skus = unicode string

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PricePoint:
    sku: str
    quantity: int
    price: int


PRICE_POINTS = set(
    [
        PricePoint("A", 1, 50),
        PricePoint("A", 3, 130),
        PricePoint("B", 1, 30),
        PricePoint("B", 2, 45),
        PricePoint("C", 1, 20),
        PricePoint("D", 1, 15),
    ]
)


def best_price_point(sku: str, quantity: int) -> Optional[PricePoint]:
    """
    Returns the best price for the given SKU, given that
    the customer is buying at least `quantity` of the item.

    Returns `None` if there does not exist such a price point
    """
    price_points_for_sku = set(
        pp for pp in PRICE_POINTS if pp.sku == sku and pp.quantity <= quantity
    )
    if len(price_points_for_sku) == 0:
        return None
    return min(price_points_for_sku, key=lambda pp: pp.price / pp.quantity)


def checkout(skus: str):
    quantities = {}
    for sku in skus:
        if sku not in quantities:
            quantities[sku] = 0
        quantities[sku] += 1

    total_price = 0
    for (sku, quantity) in quantities.items():
        while quantity > 0:
            pp = best_price_point(sku, quantity)
            if pp is None:
                return -1
            total_price += pp.price
            quantity -= pp.quantity
    
    return total_price







