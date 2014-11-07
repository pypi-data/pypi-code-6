

class DictDiffer(object):
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect 
    def removed(self):
        return self.set_past - self.intersect 
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])


def diffdict(server1,server2):

    set1 = set(server1)
    set2 = set(server2)

    samekeys = set1.intersection(set2)

    missingkeys = set1 - samekeys
    #print "server1 extra keys", missingkeys
    extrakeys = set2 - samekeys
    #print "server2 extra keys", extrakeys
    samekeysdiffvalues = set(o for o in samekeys if server1[o] != server2[o])
    #print "same keys, but different values", samekeysdiffvalues 
    samekeysandvalues = set(o for o in samekeys if server1[o] == server2[o])
    #print "same keys and values", samekeysandvalues

    return samekeysandvalues, samekeysdiffvalues, missingkeys, extrakeys



