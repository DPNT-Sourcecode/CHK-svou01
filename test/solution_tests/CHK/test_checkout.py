from solutions.CHK import checkout_solution as sln
import pytest


class TestCheckout():
    
    def test_checkout_AAABADC(self):
      assert sln.checkout("AAABADC") == 130 + 30 + 50 + 15 + 20 

    def test_checkout_AAAEBADC(self):
      assert sln.checkout("AAAEBADC") == 130 + 40 + 30 + 50 + 15 + 20 

    def test_checkout_AAAEBADCE(self):
      assert sln.checkout("AEBADCE") == 50 + 40 + 0 + 50 + 15 + 20 + 40
    
    def test_checkout_AAAAAEEBAAABB(self):
      assert sln.checkout("AAAAAEEBAAABB") == 200 + 40 + 40 + 0 + 130 + 45

    def test_checkout_FF(self):
      assert sln.checkout("FF") == 20

    def test_checkout_FFF(self):
      assert sln.checkout("FFF") == 20
    
    def test_checkout_empty(self):
      assert sln.checkout("") == 0

    def test_checkout_invalid_input(self):
      assert sln.checkout("ABCa") == -1 
      assert sln.checkout("AxA") == -1
    
    def test_no_bundle_overlap(self):
      for bundle in sln.BUNDLES:
        for sku in bundle:
          assert sku not in sln.BUY_N_GET_M_FREE
          assert sku not in sln.BULK_DISCOUNTS
    
    @pytest.mark.timeout(5)
    def test_checkout_ABCDEFGHIJKLMNOPQRSTUVWXYZ(self):
      assert sln.checkout("ABCDEFGHIJKLMNOPQRSTUVWXYZ") == 965

