import requests

from ..config import URL_OVERPASS_API, FN_NETWORK_QUERY

def network_master_list(query=None):
    query = query or open(FN_NETWORK_QUERY).read()

    resp = requests.post(URL_OVERPASS_API, data=query)
    
    if not resp.status_code == 200:
        raise ValueError("Fail query overpass", resp.text)
        
    masters = resp.text.split()

    for line in masters:
        yield int(line)
# end network_master_list
