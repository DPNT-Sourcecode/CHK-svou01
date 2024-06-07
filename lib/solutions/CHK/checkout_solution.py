# noinspection PyUnusedLocal
# skus = unicode string

Quantities = dict[str, int]

def get_quantities(skus: str) -> Quantities:
    quantities = {}
    for sku in skus:
        if sku not in quantities:
            quantities[sku] = 0
        quantities[sku] += 1
    return quantities

BASIC_PRICES = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
    "E": 40,
    "F": 10,
    "G": 20,
    "H": 10,
    "I": 35,
    "J": 60,
    "K": 80,
    "L": 90,
    "M": 15,
    "N": 40,
    "O": 10,
    "P": 50,
    "Q": 30,
    "R": 50,
    "S": 30,
    "T": 20,
    "U": 40,
    "V": 50,
    "W": 20,
    "X": 90,
    "Y": 10,
    "Z": 50,
}

BULK_DISCOUNTS = {
    "A": {
        3: 130,
        5: 200
    },
    "B": {
        2: 45
    },
    "H": {
        5: 45,
        10: 80
    },
    "K": {
        2: 150
    },
    "P": {
        5: 200
    },
    "Q": {
        3: 80
    },
    "V": {
        2: 90,
        3: 130
    },
}

BUY_N_GET_M_FREE = {
    "E": {
        2: {"B": 1}
    },
    "F": {
        2: {"F": 1}
    }
}

def checkout(skus: str) -> int:
    quantities = get_quantities(skus)

    for sku, offer in buy_n_get_m_free.items():
        if 

if __name__ == "__main__":
    print(checkout("A"))