class Certificate(object):

    auth_method = {
        'sso': 1,
        'cps': 2,
        'ids': 4,
        'named': 8,
        'collective': 16,
        'automate': 32,
        'anonyme': 64,
        'ca': 128,
        'weak': 256
    }

    @staticmethod
    def build_mask(sso=False, cps=False, ids=False, named=False,
                   collective=False, automate=False, anonyme=False, ca=False,
                   weak=False):
        func_vars = vars().copy()
        mask = 0
        for key, value in Certificate.auth_method.iteritems():
            mask += value if func_vars.get(key) else 0
        return mask
