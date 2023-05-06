from .tee import good_wrong
from .datasource.osmapi import get_master, get_route, get_platform
from .datasource.osmapi import _typid

# CONSTS
KEY_ID   = "id"
KEY_NAME = "name"
KEY_FROM = "from"
KEY_TO   = "to"
KEY_REF  = "ref"
KEY_ROLE = "role"

def travese_platform(platform):
    with good_wrong("platform", _typid(platform)[1]):
        platform = get_platform(platform)
        pname = platform.tags[KEY_NAME]

    return platform
# end travese_platform

def travese_route(route, lint):
    with good_wrong("route", _typid(route)[1]):
        route = get_route(route)
        rname = route.tags[KEY_NAME]
        print(rname)

        members = route.members
        stop_names = []
        non_roles  = []
        for e in members:
            if not e.role.startswith("platform"):

                # probably stop missing role
                if type(e).__name__ == "Node":
                    non_roles.append(e)

                # else no problem
                continue

            platform = travese_platform(e)
            stop_names.append(platform.tags[KEY_NAME])
        # end for members

        print(*stop_names)

        if len(non_roles):
            s = [ str(e) for e in non_roles ]
            s = "\n".join(s)
            assert not len(non_roles), "likely missing role:\n"+s

        assert route.tags[KEY_FROM]==stop_names[ 0], "inconsistent terminal"
        assert route.tags[KEY_TO  ]==stop_names[-1], "inconsistent terminal"

    # end with
    
    return route
# end travese_route

def travese_master(master, lints):
    with good_wrong("master", _typid(master)[1]):
        master = get_master(master)
        ref = master.tags[KEY_REF]
        print("主线", ref)

        lint = lints.get(ref, {})
        routes = master.members
        for r in routes:
            travese_route(r, lint)

        assert ref in lints, "unlisted master"
        if "route_count" in lint:
            lint["route_count"] -= len(routes)
            assert not lint["route_count"], "inconsistent route count"
    # end with
    
    return master
# end travese_master
