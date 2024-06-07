# noinspection PyUnusedLocal
# skus = unicode string

from dataclasses import dataclass
from typing import Optional, Callable, Tuple
from frozendict import frozendict
from frozenlist import FrozenList
import math
from functools import cache, partial
import line_profiler
from queue import Queue, Empty
from multiprocessing import Pool

Quantities = frozendict[str, int]


@dataclass(frozen=True)
class Offer:
    requires_quantities: Quantities
    includes: Quantities
    price: int


Deal = FrozenList[Offer]

@cache
@line_profiler.profile
def quantities_geq(lhs: Quantities, rhs: Quantities) -> bool:
    for sku, quantity in rhs.items():
        if sku not in lhs or lhs[sku] < quantity:
            return False
    return True


def basic_price(sku: str, price: int) -> Offer:
    return bulk_discount(sku, 1, price)

def bulk_discount(sku: str, quantity: int, price: int) -> Offer:
    return Offer(
        frozendict({sku: quantity}),
        frozendict({sku: quantity}),
        price
    )

def buy_n_get_m_free(sku: str, quantity: int, reward_sku: str, reward_quantity: int, price: int) -> Offer:
    if sku == reward_sku:
        return Offer(
            frozendict({sku: quantity}),
            frozendict({sku: quantity + reward_quantity}),
            price
        )
    else:
        return Offer(
            frozendict({sku: quantity}),
            frozendict({
                sku: quantity,
                reward_sku: reward_quantity
            }),
            price
        )

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
        buy_n_get_m_free("E", 2, "B", 1, 80),
        basic_price("F", 10),
        buy_n_get_m_free("F", 2, "F", 1, 20),
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
        buy_n_get_m_free("N", 3, "M", 1, 120),
        basic_price("O", 10),
        basic_price("P", 50),
        bulk_discount("P", 5, 200),
        basic_price("Q", 30),
        bulk_discount("Q", 3, 80),
        basic_price("R", 50),
        buy_n_get_m_free("R", 3, "Q", 1, 150),
        basic_price("S", 30),
        basic_price("T", 20),
        basic_price("U", 40),
        buy_n_get_m_free("U", 3, "U", 1, 120),
        basic_price("V", 50),
        bulk_discount("V", 2, 90),
        bulk_discount("V", 3, 130),
        basic_price("W", 20),
        basic_price("X", 90),
        basic_price("Y", 10),
        basic_price("Z", 50),
    ]
)


def get_deal_price(deal: Deal) -> int:
    return sum(offer.price for offer in deal)

def get_quantities(skus: str) -> Quantities:
    quantities = {}
    for sku in skus:
        if sku not in quantities:
            quantities[sku] = 0
        quantities[sku] += 1
    return frozendict(quantities)

@line_profiler.profile
def find_best_deal(
    quantities: Quantities,
    *,
    offers: frozenset[Offer] = OFFERS,
) -> Optional[Deal]:

    @dataclass
    class Scenario:
        quantities: Quantities
        applied_offers: set[Offer]
        available_offers: frozenset[Offer]
    
    queue = Queue()
    queue.put(Scenario(quantities, set(), offers))

    best_price = math.inf
    best_deal = None

    while True:
        try:
            scenario = queue.get_nowait()
        except Empty:
            break
            
        print(scenario.quantities)

        if all(quantity == 0 for quantity in scenario.quantities.values()):
            deal = FrozenList(list(scenario.applied_offers))
            deal.freeze()
            price = get_deal_price(deal)
            if price < best_price:
                best_price = price
                best_deal = deal
            continue

        applicable_offers = frozenset(
            offer for offer in scenario.available_offers if quantities_geq(
                scenario.quantities,
                offer.requires_quantities
            )
        )

        for offer in applicable_offers:
            new_quantities = {**quantities}
            for included_sku, included_quantity in offer.includes.items():
                if included_sku in new_quantities:
                    new_quantities[included_sku] = max(
                        0, new_quantities[included_sku] - included_quantity
                    )

            queue.put(Scenario(
                frozendict(new_quantities),
                set([offer]).union(scenario.applied_offers),
                applicable_offers
            ))

    return best_deal


def checkout(skus: str, *, offers: frozenset[Offer] = OFFERS):
    best_deal = find_best_deal(
        get_quantities(skus),
        offers=offers
    )

    if best_deal is None:
        return -1

    return get_deal_price(best_deal)

if __name__ == "__main__":
    checkout("A")






