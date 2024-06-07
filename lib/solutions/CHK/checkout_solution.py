# noinspection PyUnusedLocal
# skus = unicode string

from dataclasses import dataclass
from typing import Optional

Quantities = dict[str, int]

@dataclass(frozen=True)
class Offer:
    does_qualify: Callable[[Quantities], bool]
    includes: Quantities
    price: int

def quantity_geq(lhs: Quantities, rhs: Quantities) -> bool:
    for (sku, quantity) in rhs.items():
        if sku not in lhs or lhs[sku] < quantity:
            return False
    return True

def requires_quantity(required_quantity: Quantities) -> Callable[[Quantities], bool]:
    return lambda q: quantity_geq(q, required_quantity)

OFFERS = set(
    [
        Offer("A", 1, 50),
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



