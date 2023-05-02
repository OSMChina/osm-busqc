# CONFIG

# WORK DIR
# place to load your credential
# see password.sample, write content and name/place it accordingly:
FN_PASSWORD = "./password"
FN_NETWORK_QUERY = "./network_query"
# place cache
DN_FETCH = "./fetch"

# NETWORK
# ref: https://wiki.openstreetmap.org/wiki/Overpass_API
URL_OVERPASS_API        = "https://overpass-api.de/api/interpreter"
# ref: https://docentyt.github.io/osm_easy_api/osm_easy_api/api/api.html
# and https://docentyt.github.io/osm_easy_api/osm_easy_api/api/endpoints.html
URL_OPENSTREETMAP_API   = "https://www.openstreetmap.org"
# https proxy
# comment/uncomment to switch off/on
import os
os.environ["https_proxy"] = "http://localhost:8889"

# DEBUG
# dump http traffic
DEBUG_NETWORK = False
# depth of stacktrace of assertion fail
DEBUG_STACKTRACE = 0

# END CONFIG


# INIT CACHE
from os.path import join as pthjoin
DN_MASTERS  = pthjoin(DN_FETCH, "masters")
DN_ROUTES   = pthjoin(DN_FETCH, "routes")
DN_PLTFS    = pthjoin(DN_FETCH, "platforms")

# LOAD PASSWORD
with open(FN_PASSWORD) as f:
    OSM_CREDENTIAL = f.readline().strip().split(":")

# DEBUG SETUP
def _set_debug_requests():
    import logging
    import http.client as http_client
    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
# end _set_debug_requests

if DEBUG_NETWORK:
    _set_debug_requests()
