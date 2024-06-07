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

def buy_n_get_m_free(sku: str, quantity: int, reward_sku: str, reward_quantity: int, price: int) -> Offer:
    if sku == reward_sku:
        return Offer(
            requires_quantities(frozendict({sku: quantity})),
            frozendict({sku: quantity + reward_quantity}),
            80
        )
    else:
        return Offer(
            requires_quantities(frozendict({sku: quantity})),
            frozendict({sku: quantity, reward_sku: reward_quantity}),
            80
        ),

OFFERS = frozenset(
    [
        basic_price("A", 50),
        bulk_discount("A", 3, 130),
        bulk_discount("A", 5, 200),
        basic_price("B", 30),
        bulk_discount("B", 2, 45),
        basic_price("C", 20),
        basic_price("D", 15),
        basic_price("E", 40),
        basic_price("F", 10),
        basic_price("G", 20),
        basic_price("H", 10),
        bulk_discount("H", 5, 45),
        bulk_discount("H", 10, 80),
        basic_price("I", 35),
        basic_price("J", 60),
        basic_price("K", 80),
        bulk_discount("K", 2, 150),
        basic_price("L", 90),
        basic_price("M", 15),
        basic_price("N", 40),
        basic_price("O", 10),
        basic_price("P", 50),
        bulk_discount("P", 5, 200),
        basic_price("Q", 30),
        bulk_discount("Q", 3, 80),
        basic_price("R", 50),
        basic_price("S", 30),
        basic_price("T", 20),
        basic_price("U", 40),
        basic_price("V", 50),
        bulk_discount("V", 2, 90),
        bulk_discount("V", 3, 130),
        basic_price("W", 20),
        basic_price("X", 90),
        basic_price("Y", 10),
        basic_price("Z", 50),
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







