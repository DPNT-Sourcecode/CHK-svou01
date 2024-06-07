from solutions.CHK import checkout_solution as sln
from frozendict import frozendict
import pytest
import cProfile

TEST_OFFERS = frozenset(
    [
        sln.basic_price("A", 50),
        sln.bulk_discount("A", 3, 130),
        sln.bulk_discount("A", 5, 200),
        sln.basic_price("B", 30),
        sln.bulk_discount("B", 2, 45),
        sln.basic_price("C", 20),
        sln.basic_price("D", 15),
        sln.basic_price("E", 40),
        sln.buy_n_get_m_free("E", 2, "B", 1, 80),
        sln.basic_price("F", 10),
        sln.buy_n_get_m_free("F", 2, "F", 1, 20),
    ]
)

class TestCheckout():
    def test_quantities_geq(self):
      assert sln.quantities_geq(
        frozendict({"A": 3}),
        frozendict({"A": 1}),
      )
      assert not sln.quantities_geq(
        frozendict({"A": 3}),
        frozendict({"B": 1}),
      )
      assert sln.quantities_geq(
        frozendict({"A": 3, "B": 1}),
        frozendict({"A": 1}),
      )
      assert sln.quantities_geq(
        frozendict({"A": 1, "B": 1}),
        frozendict({"A": 1}),
      )
    
    def test_checkout_AAABADC(self):
      assert sln.checkout("AAABADC", offers=TEST_OFFERS) == 130 + 30 + 50 + 15 + 20 

    def test_checkout_AAAEBADC(self):
      assert sln.checkout("AAAEBADC", offers=TEST_OFFERS) == 130 + 40 + 30 + 50 + 15 + 20 

    def test_checkout_AAAEBADCE(self):
      assert sln.checkout("AEBADCE", offers=TEST_OFFERS) == 50 + 40 + 0 + 50 + 15 + 20 + 40
    
    def test_checkout_AAAAAEEBAAABB(self):
      assert sln.checkout("AAAAAEEBAAABB", offers=TEST_OFFERS) == 200 + 40 + 40 + 0 + 130 + 45

    def test_checkout_FF(self):
      assert sln.checkout("FF", offers=TEST_OFFERS) == 20

    def test_checkout_FFF(self):
      assert sln.checkout("FFF", offers=TEST_OFFERS) == 20
    
    def test_checkout_empty(self):
      assert sln.checkout("", offers=TEST_OFFERS) == 0

    def test_checkout_invalid_input(self):
      assert sln.checkout("ABCa", offers=TEST_OFFERS) == -1 
      assert sln.checkout("AxA", offers=TEST_OFFERS) == -1
    
    def test_checkout_ABCDEFGHIJKLMNOPQRSTUVWXYZ(self):
      assert sln.checkout("ABCDEFGHIJKLMNOPQRSTUVWXYZ") == 0

    @pytest.mark.timeout(5)
    def test_checkout_large_input(self):
      sln.checkout("AAAAAEEBBAJSUDBIOASCOPINIPAJPSOAAAAAEEBBAJSUDBIOASCOPINIPAJPSO", offers=TEST_OFFERS)

