from .tee import good_wrong
from .datasource.osmapi import get_master, get_route, get_platform
from .datasource.osmapi import _typid

def travese_platform(platform):
    with good_wrong("platform", _typid(platform)[1]):
        platform = get_platform(platform)
        pname = platform.tags["name"]

    return pname

def travese_route(route, lint):
    with good_wrong("route", _typid(route)[1]):
        route = get_route(route)
        rname = route.tags["name"]
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

            pname = travese_platform(e)
            stop_names.append(pname)
        # end for members

        print(*stop_names)

        assert route.tags["from"]==stop_names[0] , "inconsistent terminal"
        assert route.tags["to"]  ==stop_names[-1], "inconsistent terminal"

        if len(non_roles):
            s = [ e["id"] for e in non_roles ]
            s = ",".join(s)
            assert not len(non_roles), "likely missing role: "+s

    # end with
# end travese_route

def travese_master(master, lints):
    with good_wrong("master", _typid(master)[1]):
        master = get_master(master)
        ref = master.tags["ref"]
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
# end travese_master
