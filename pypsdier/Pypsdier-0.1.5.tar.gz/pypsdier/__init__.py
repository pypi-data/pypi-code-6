# Main functions to be used directly from pypsdier
from core.ode_library import ode
from core.pde_library import pde
from core.installation_test_library import test
from core.seed_handler_library import create_seed_handler

# Versioning
version = "0.1.5"
  
if __name__=="__main__":
  test()
  create_seed_handler()
  print ":)"
