import os,sys
#import json
#from ast import literal_eval
from os import path
from os.path import join as pthjoin
import pickle

import osm_easy_api
from osm_easy_api import Node, Relation, Way
from osm_easy_api.data_classes.relation import Member
from osm_easy_api.data_classes.osm_object_primitive import osm_object_primitive

from ..config import DN_MASTERS, DN_ROUTES, DN_PLTFS
from ..config import URL_OPENSTREETMAP_API, OSM_CREDENTIAL

for d in [DN_MASTERS,DN_ROUTES,DN_PLTFS]:
    os.makedirs(d,exist_ok=True)

_conn = osm_easy_api.Api(URL_OPENSTREETMAP_API, *OSM_CREDENTIAL)

def _load_cache(pth, outdate=None):
    """
    pth: path to load
    outdate: date before this value are consider outdate and being pruned
    """
    #if outdate is not None and path.exists(pth):
        #if path.stat then
            # remove file
    
    if not path.exists(pth):
        return None
    
    # else
    #with open(pth) as f:
    #    d = literal_eval(f.read())
    #
    #e = osm_object_primitive.from_dict(d)
    
    with open(pth, "rb") as f:
        e = pickle.load(f)
    
    return e
# end _load_cache

def _save_cache(pth, e):
    with open(pth, "wb") as f:
        pickle.dump(e, f)
    #with open(pth, "w") as f:
    #    print(e.to_dict(), file=f)
# end _save_cache

def _typid(e):
    """
    e: int, str, element
    returns: type, id
    """
    if isinstance(e, Member):
        e = e.element
        
    if isinstance(e, osm_object_primitive):
        return type(e), e.id
        
    if isinstance(e, str):
        return None, int(e)
        
    if isinstance(e, int):
        return None, e
    
    raise ValueError("Strange type "+str(e))
# end _typid

def get_master(id_or_ref, no_cache=False):
    typ, eid = _typid(id_or_ref)
    typ = typ or Relation
    fn = pthjoin(DN_MASTERS, str(eid))

    e = _load_cache(fn) 
    
    if e is not None:
        return e
        
    # else
    e = _conn.elements.get(typ,eid)
    _save_cache(fn, e)

    return e
# end get_master

def get_route(id_or_ref, no_cache=False):
    typ, eid = _typid(id_or_ref)
    typ = typ or Relation
    fn = pthjoin(DN_ROUTES, str(eid))

    e = _load_cache(fn) 
    
    if e is not None:
        return e
        
    # else
    e = _conn.elements.get(typ,eid)
    _save_cache(fn, e)

    return e
# end get_route

def get_platform(ref, no_cache=False):
    typ, eid = _typid(ref)
    assert typ is not None, "Fail detect platform element type"
    fn = pthjoin(DN_PLTFS, str(eid))

    e = _load_cache(fn) 
    
    if e is not None:
        return e
        
    # else
    e = _conn.elements.get(typ,eid)
    _save_cache(fn, e)

    return e
# end get_platform

