# noinspection PyUnusedLocal
# skus = unicode string

from dataclasses import dataclass
from typing import Optional, Callable
from frozendict import frozendict
import math

Quantities = frozendict[str, int]

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
        Offer(requires_quantities(frozendict({"A": 1})), frozendict({"A": 1}), 50),
        Offer(requires_quantities(frozendict({"A": 3})), frozendict({"A": 3}), 120),
        Offer(requires_quantities(frozendict({"A": 5})), frozendict({"A": 5}), 200),
        Offer(requires_quantities(frozendict({"B": 1})), frozendict({"B": 1}), 30),
        Offer(requires_quantities(frozendict({"B": 2})), frozendict({"B": 2}), 45),
        Offer(requires_quantities(frozendict({"C": 1})), frozendict({"C": 1}), 20),
        Offer(requires_quantities(frozendict({"D": 1})), frozendict({"D": 1}), 15),
        Offer(requires_quantities(frozendict({"E": 1})), frozendict({"E": 1}), 40),
        Offer(requires_quantities(frozendict({"E": 2})), frozendict({"E": 2, "B": 1}), 80),
    ]
)

def get_deal_price(deal: Deal) -> int:
    return sum(offer.price for offer in deal)

def find_best_deal(quantities: Quantities) -> Optional[Deal]:
    if all(quantity == 0 for quantity in quantities.values()):
        return []
    
    applicable_offers = set(offer for offer in OFFERS if offer.does_qualify(quantities))
    
    best_deal = None
    best_price = math.inf
    for offer in applicable_offers:
        new_quantities = {**quantities}
        for (included_sku, included_quantity) in offer.includes.items():
            if included_sku in new_quantities:
                new_quantities[included_sku] = max(
                    0,
                    new_quantities[included_sku] - included_quantity
                )
        new_quantities = frozendict(new_quantities)

        new_deal = [offer, *find_best_deal(new_quantities)]
        if (new_deal_price := (get_deal_price(new_deal) + offer.price)) < best_price:
            best_price = new_deal_price
            best_deal = new_deal
    
    return best_deal

def checkout(skus: str):
    quantities = {}
    for sku in skus:
        if sku not in quantities:
            quantities[sku] = 0
        quantities[sku] += 1
    quantities = frozendict(quantities)
    
    best_deal = find_best_deal(quantities)

    if best_deal is None:
        return -1
    print(best_deal)
    
    return get_deal_price(best_deal)
