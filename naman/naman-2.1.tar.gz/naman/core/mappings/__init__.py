import vlan_conditions, vlan_actions

modules = [vlan_conditions, vlan_actions]


def get_mappings():
    maps = {}
    for x in modules:
        for y in x.mappings:
            if isinstance(y, str):
                name = y.split(".")
                maps[name[len(name)-1]] = "%s" % y
                continue
            maps[y.__name__] = y
    return maps
