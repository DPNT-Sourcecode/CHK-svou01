# noinspection PyUnusedLocal
# skus = unicode string

from dataclasses import dataclass
from typing import Optional, Callable
from frozendict import frozendict
from frozenlist import FrozenList
import math
from functools import lru_cache

Quantities = frozendict[str, int]


@dataclass(frozen=True)
class Offer:
    does_qualify: Callable[[Quantities], bool]
    includes: Quantities
    price: int


Deal = FrozenList[Offer]


@lru_cache(maxsize=None)
def quantities_geq(lhs: Quantities, rhs: Quantities) -> bool:
    for sku, quantity in rhs.items():
        if sku not in lhs or lhs[sku] < quantity:
            return False
    return True


def requires_quantities(
    required_quantities: Quantities,
) -> Callable[[Quantities], bool]:
    return lambda quantities: quantities_geq(quantities, required_quantities)

def basic_price(sku: str, price: int) -> Offer:
    return bulk_discount(sku, 1, price)

def bulk_discount(sku: str, quantity: int, price: int) -> Offer:
    return Offer(
        requires_quantities(frozendict({sku: quantity})),
        frozendict({sku: quantity}),
        price
    )


OFFERS = frozenset(
    [
        basic_price("A", 50),
        bulk_discount("A", 3, 130),
        bulk_discount("A", 5, 200),
        basic_price("B", 30),
        bulk_discount("B", 2, )
    ]
)


@lru_cache(maxsize=None)
def get_deal_price(deal: Deal) -> int:
    return sum(offer.price for offer in deal)


@lru_cache(maxsize=None)
def get_quantities(skus: str) -> Quantities:
    quantities = {}
    for sku in skus:
        if sku not in quantities:
            quantities[sku] = 0
        quantities[sku] += 1
    return frozendict(quantities)


@lru_cache(maxsize=None)
def find_best_deal(
    quantities: Quantities,
    *,
    offers: frozenset[Offer] = OFFERS
) -> Optional[Deal]:
    global indent
    if all(quantity == 0 for quantity in quantities.values()):
        empty = FrozenList([])
        empty.freeze()
        return empty

    applicable_offers = set(offer for offer in offers if offer.does_qualify(quantities))

    best_deal = None
    best_price = math.inf
    for offer in applicable_offers:
        new_quantities = {**quantities}
        for included_sku, included_quantity in offer.includes.items():
            if included_sku in new_quantities:
                new_quantities[included_sku] = max(
                    0, new_quantities[included_sku] - included_quantity
                )
        new_quantities = frozendict(new_quantities)

        rest_of_deal = find_best_deal(new_quantities)
        if rest_of_deal is None:
            continue
        new_deal = FrozenList([offer, *rest_of_deal])
        new_deal.freeze()
        if (new_deal_price := get_deal_price(new_deal)) < best_price:
            best_price = new_deal_price
            best_deal = new_deal

    return best_deal


@lru_cache(maxsize=None)
def checkout(skus: str, *, offers: frozenset[Offer] = OFFERS):
    best_deal = find_best_deal(
        get_quantities(skus),
        offers=offers
    )

    if best_deal is None:
        return -1

    return get_deal_price(best_deal)





