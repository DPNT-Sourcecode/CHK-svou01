from solutions.CHK import checkout_solution
from frozendict import frozendict

class TestCheckout():
    def test_quantities_geq(self):
      assert checkout_solution.quantities_geq(
        frozendict({"A": 3}),
        frozendict({"A": 1}),
      )
      assert not checkout_solution.quantities_geq(
        frozendict({"A": 3}),
        frozendict({"B": 1}),
      )
      assert checkout_solution.quantities_geq(
        frozendict({"A": 3, "B": 1}),
        frozendict({"A": 1}),
      )
      assert checkout_solution.quantities_geq(
        frozendict({"A": 1, "B": 1}),
        frozendict({"A": 1}),
      )
    
    def test_offers_qualify(self):
      assert Offer()
      

    def test_checkout(self):
      assert checkout_solution.checkout("AAABADC") == 130 + 30 + 50 + 15 + 20 

    def test_checkout_invalid_input(self):
      assert checkout_solution.checkout("a") == -1 

