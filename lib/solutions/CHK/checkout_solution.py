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
        Offer(requires_quantity({"A": 1}), {"A": 1}, 50),
        Offer(requires_quantity({"A": 3}), {"A": 3}, 120),
        Offer(requires_quantity({"A": 5}), {"A": 5}, 200),
        Offer(requires_quantity({"B": 1}), {"B": 1}, 30),
        Offer(requires_quantity({"B": 2}), {"B": 2}, 45),
        Offer(requires_quantity({"C": 1}), {"C": 1}, 20),
        Offer(requires_quantity({"D": 1}), {"D": 1}, 15),
        Offer(requires_quantity({"E": 1}), {"E": 1}, 40),
        Offer(requires_quantity({"E": 2}), {"E": 2, "B": 1}, 80),
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




