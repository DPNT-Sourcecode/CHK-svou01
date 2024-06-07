from solutions.CHK import checkout_solution


class TestCheckout():
    def test_best_price_point_prices(self):
      assert checkout_solution.best_price_point("A", 1).price == 50
      assert checkout_solution.best_price_point("A", 2).price == 50
      assert checkout_solution.best_price_point("A", 3).price == 130
      assert checkout_solution.best_price_point("A", 50).price == 130
      assert checkout_solution.best_price_point("B", 1).price == 30
      assert checkout_solution.best_price_point("B", 2).price == 45
      assert checkout_solution.best_price_point("B", 100).price == 45
      assert checkout_solution.best_price_point("C", 100).price == 20
      assert checkout_solution.best_price_point("D", 100).price == 15
    
    def test_best_price_point_quantities(self):
      assert checkout_solution.best_price_point("A", 1).quantity == 1
      assert checkout_solution.best_price_point("A", 2).quantity == 1
      assert checkout_solution.best_price_point("A", 3).quantity == 3
      assert checkout_solution.best_price_point("A", 50).quantity == 3
      assert checkout_solution.best_price_point("B", 1).quantity == 1
      assert checkout_solution.best_price_point("B", 2).quantity == 2
      assert checkout_solution.best_price_point("B", 100).quantity == 2
      assert checkout_solution.best_price_point("C", 100).quantity == 1
      assert checkout_solution.best_price_point("D", 100).quantity == 1
    
    def test_best_price_point_invalid_input(self):
      assert checkout_solution.best_price_point("E", 1) is None

    def test_checkout(self):
      assert checkout_solution.checkout("AAABADC") == 130 + 30 + 50 + 15 + 20 

    def test_checkout_invalid_input(self):
      assert checkout_solution.checkout("a") == -1 
