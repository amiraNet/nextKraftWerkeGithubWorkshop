import os
import sys
import pytest
import src.vpp.main as vpp
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root)


@pytest.fixture(autouse=True)
def reset_vpp_state():
    vpp.plants.clear()
    vpp.next_id = 1
    yield
