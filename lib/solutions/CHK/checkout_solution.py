# noinspection PyUnusedLocal
# skus = unicode string

from dataclasses import dataclass

@dataclass
class PricePoint:
    sku: str
    quantity: int
    price: int

def checkout(skus):
    raise NotImplementedError()

