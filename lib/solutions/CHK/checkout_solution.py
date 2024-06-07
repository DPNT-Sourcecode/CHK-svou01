# noinspection PyUnusedLocal
# skus = unicode string

from dataclasses import dataclass
from typing import Optional
import math

Quantities = dict[str, int]

@dataclass(frozen=True)
class Offer:
    does_qualify: Callable[[Quantities], bool]
    includes: Quantities
    price: int

Deal = list[Offer]

def quantities_geq(lhs: Quantities, rhs: Quantities) -> bool:
    for (sku, quantity) in rhs.items():
        if sku not in lhs or lhs[sku] < quantity:
            return False
    return True

def requires_quantities(required_quantities: Quantities) -> Callable[[Quantities], bool]:
    return lambda quantities: quantities_geq(quantities, required_quantities)

OFFERS = set(
    [
        Offer(requires_quantities({"A": 1}), {"A": 1}, 50),
        Offer(requires_quantities({"A": 3}), {"A": 3}, 120),
        Offer(requires_quantities({"A": 5}), {"A": 5}, 200),
        Offer(requires_quantities({"B": 1}), {"B": 1}, 30),
        Offer(requires_quantities({"B": 2}), {"B": 2}, 45),
        Offer(requires_quantities({"C": 1}), {"C": 1}, 20),
        Offer(requires_quantities({"D": 1}), {"D": 1}, 15),
        Offer(requires_quantities({"E": 1}), {"E": 1}, 40),
        Offer(requires_quantities({"E": 2}), {"E": 2, "B": 1}, 80),
    ]
)

def get_deal_price(deal: Deal) -> int:
    return sum(offer.price for offer in deal)

def find_best_deal(quantities: Quantities) -> Optional[Deal]:
    if all(quantity == 0 for quantity in quantities.values()):
        return []
    
    applicable_offers = set(offer for offer in OFFERS if offer.does_qualify(quantities))
    if len(applicable_offers) == 0:
        return None
    
    best_deal = None
    best_price = math.inf
    for offer in applicable_offers:
        

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






