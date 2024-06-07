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

OFFERS = set(
    [
        bulk_discount("A", 3, 130),
        bulk_discount("A", 5, 200),
        
        bulk_discount("B", 2, 45),
        
        
        
        buy_n_get_m_free("E", 2, "B", 1, 80),
        
        buy_n_get_m_free("F", 2, "F", 1, 20),
        
        
        bulk_discount("H", 5, 45),
        bulk_discount("H", 10, 80),
        
        
        
        bulk_discount("K", 2, 150),
        
        
        
        buy_n_get_m_free("N", 3, "M", 1, 120),
        
        
        bulk_discount("P", 5, 200),
        
        bulk_discount("Q", 3, 80),
        
        buy_n_get_m_free("R", 3, "Q", 1, 150),
        
        
        
        buy_n_get_m_free("U", 3, "U", 1, 120),
        
        bulk_discount("V", 2, 90),
        bulk_discount("V", 3, 130),
        
        
        
        
    ]
)

def checkout(skus: str) -> int:
    quantities = get_quantities(skus)

if __name__ == "__main__":
    print(checkout("A"))