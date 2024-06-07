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

# It's important that bulk discounts for a given
# SKU are ordered from best to worst value in this
# list
BULK_DISCOUNTS = {
    "A": {
        5: 200,
        3: 130,
    },
    "B": {
        2: 45
    },
    "H": {
        10: 80,
        5: 45,
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
        3: 130,
        2: 90,
    },
}

BUY_N_GET_M_FREE = {
    "E": {
        2: {"B": 1}
    },
    "F": {
        2: {"F": 1}
    },
    "N": {
        3: {"M": 1}
    },
    {
        "R"
    }
    "U": {
        3: {"U": 1}
    }
}

def checkout(skus: str) -> int:
    quantities = get_quantities(skus)
    quantities_counting_towards_offers = {**quantities}

    # NOTE: I am making the assumption that there will be
    #       no two offers of the form "Buy n X get m Y free"
    #       for the same X and different Ys.
    applied_offer = True
    while applied_offer:
        applied_offer = False
        for sku, offer in BUY_N_GET_M_FREE.items():
            if sku not in quantities_counting_towards_offers:
                continue
            for quantity, reward in offer.items():
                if quantities_counting_towards_offers[sku] >= quantity:
                    for reward_sku, reward_quantity in reward.items():
                        if reward_sku != sku or quantities_counting_towards_offers[sku] >= quantity + reward_quantity:
                            if reward_sku in quantities:
                                quantities[reward_sku] = max(
                                    0,
                                    quantities[reward_sku] - reward_quantity
                                )
                                quantities_counting_towards_offers[sku] -= quantity
                                if reward_sku in quantities_counting_towards_offers:
                                    quantities_counting_towards_offers[reward_sku] = max(
                                        0,
                                        quantities_counting_towards_offers[reward_sku] - reward_quantity
                                    )
                                applied_offer = True
    
    total_price = 0
    applied_bulk_discount = True
    while applied_bulk_discount:
        applied_bulk_discount = False
        for sku, offer in BULK_DISCOUNTS.items():
            if sku not in quantities:
                continue

            # NOTE: Here I'm using the assumption that bulk discounts
            #       are ordered from best to worst value by breaking early
            for discount_quantity, discount_price in offer.items():
                if quantities[sku] >= discount_quantity:
                    total_price += discount_price
                    quantities[sku] -= discount_quantity
                    applied_bulk_discount = True
                    break
    
    for sku, quantity in quantities.items():
        if sku not in BASIC_PRICES:
            return -1
        total_price += BASIC_PRICES[sku] * quantity
    
    return total_price

if __name__ == "__main__":
    print(checkout("UUUU"))
