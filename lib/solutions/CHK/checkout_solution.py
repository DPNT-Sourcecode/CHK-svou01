# noinspection PyUnusedLocal
# skus = unicode string

from dataclasses import dataclass
from typing import Optional, Tuple, Iterable
from frozendict import frozendict
import math
from functools import cache, partial
import line_profiler
from queue import SimpleQueue, Empty
import multiprocessing

Quantities = frozendict[str, int]


@dataclass(frozen=True)
class Offer:
    requires_quantities: Quantities
    includes: Quantities
    price: int


Deal = list[Offer]

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

OFFERS = set(
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


@dataclass
class Scenario:
    quantities: Quantities
    deal: Deal
    available_offers: set[Offer]

def process_scenario(
    queue: SimpleQueue,
    scenario: Scenario
) -> Option[Deal]:
    if all(quantity == 0 for quantity in scenario.quantities.values()):
        return scenario.deal

    applicable_offers = list(
        offer for offer in scenario.available_offers if quantities_geq(
            scenario.quantities,
            offer.requires_quantities
        )
    )

    for offer in applicable_offers:
        new_quantities = scenario.quantities.copy()
        for included_sku, included_quantity in offer.includes.items():
            if included_sku in new_quantities:
                new_quantities = new_quantities.set(
                    included_sku,
                    max(
                        0,
                        new_quantities.get(included_sku) - included_quantity
                    )
                )
        
        queue.put(Scenario(
            frozendict(new_quantities),
            [offer, *scenario.deal],
            applicable_offers
        ))
    
    return None

@line_profiler.profile
def find_best_deal(
    quantities: Quantities,
    *,
    offers: Iterable[Offer] = OFFERS,
) -> Optional[Deal]:
    
    queue = SimpleQueue()
    queue.put(Scenario(quantities, [], offers))

    manager = multiprocessing.Manager()
    mutex = manager.Lock()

    best_price = math.inf
    best_deal = None

    handles = []

    while True:
        try:
            scenario = queue.get_nowait()
        except Empty:
            break
        
        handle = multiprocessing.Process(target=process_scenario, args=(queue, mutex, scenario,))
        handle.start()
        handles.append(
            handle
        )

    for handle in handles:
        deal = handle.join()
        if deal is not None and 

    return best_deal


def checkout(skus: str, *, offers: set[Offer] = OFFERS):
    best_deal = find_best_deal(
        get_quantities(skus),
        offers=offers
    )

    if best_deal is None:
        return -1

    return get_deal_price(best_deal)

if __name__ == "__main__":
    print(checkout("AAA"))




