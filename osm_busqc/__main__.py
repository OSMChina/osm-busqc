import argparse
from ast import literal_eval

# local lib
from .datasource.overpass import network_master_list
from .travese import travese_master
from .tee import good_wrong

ASSERTS_MASTERS = "./masters.lints.py"



lints = literal_eval(open(ASSERTS_MASTERS).read())

for m in network_master_list():
    travese_master(m, lints)

for k,v in lints.items():
    with good_wrong("master", k):
        assert "route_count" not in v or not v["route_count"], "missing master %s"%k
# end for

