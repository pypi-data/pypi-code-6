class CmdList(object):
    def __init__(self, args):
        self.args = args

    def __call__(self):
        IGNORED_ARGS = ['command', 'sub_command', 'version']
        output = ""
        for k, v in vars(self.args).iteritems():
            if k not in IGNORED_ARGS:
                output += "{} = {}\n".format(k, v)
        return output
