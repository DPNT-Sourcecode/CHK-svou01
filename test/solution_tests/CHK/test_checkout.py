from solutions.CHK import checkout_solution as sln
from frozendict import frozendict

TEST_OFFERS = sln.OFFERS

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
    
    def test_offers_qualify(self):
      assert sln.requires_quantities(frozendict({"A": 3}))(frozendict({"A": 3}))

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
