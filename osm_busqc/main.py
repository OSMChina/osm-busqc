import argparse
from ast import literal_eval

# local lib
from .datasource.overpass import network_master_list
from .travese import travese_master
from .tee import good_wrong

# routes to check
# python literal dump file
#ASSERTS_ROUTES  = "./routes.asserts.py"
ASSERTS_MASTERS = "./masters.asserts.py"
OUT_INFO        = "./info.txt"
OUT_PROBLEMS    = "./problems.txt"


if __name__ == "__main__":

    assertions = literal_eval(open(ASSERTS_MASTERS).read())

    for m in network_master_list():
        travese_master(m, assertions)

    for k,v in assertions.items():
        with good_wrong("master", k):
            assert "route_count" not in v or not v["route_count"], "missing master %s"%k
    # end for
# end main
