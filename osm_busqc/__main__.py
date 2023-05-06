import argparse
from ast import literal_eval

from .datasource.overpass import network_master_list
from .travese import travese_master
from .tee import good_wrong


# CONSTS
ASSERTS_MASTERS = "./masters.lints.py"

# PARAMS
PARAMS = argparse.ArgumentParser()
PARAMS.add_argument("--cache_exp"           , type=str, default=None,
  help="ISO datetime, cached objects before this are expired and re-download.")
PARAMS.add_argument("--lint_file"           , type=str, default=ASSERTS_MASTERS)
PARAMS.add_argument("--masters_list_file"   , type=str, default=None,
  help="read masters from file instead of overpass query, must be a text file comprises one master id per line")

argv = PARAMS.parse_args()

# MAIN
lints = literal_eval(open(ASSERTS_MASTERS).read())
masters = network_master_list() if not argv.masters_list_file \
  else open(argv.masters_list_file).read().split()
  
if argv.cache_exp:
    from .config import set_cache_expiration
    set_cache_expiration(argv.cache_exp)

for m in network_master_list():
    travese_master(m, lints)

for k,v in lints.items():
    with good_wrong("master", k):
        assert "route_count" not in v or not v["route_count"], "missing master or route %s"%k
# end for

