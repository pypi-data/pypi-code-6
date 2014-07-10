from nose.plugins import Plugin


class CustomDescription(Plugin):
    """
    Test custom description output plugin.
    Using the verbose flag (-v) when running a test will display the first line
    of the test doc string if present, otherwise will output the test name.
    What if you want to display the whole docstring or maybe the test name with
    description, this plugin will allow you to customize this output.
    """
    enabled = False
    name = 'customdescription'
    score = 2000

    _options = (
        ("custom_description",
         "Override test description output - one of 0,1,2 [%s] "
         "'0': Test name without description "
         "'1': Test Description without test name "
         "'2': Test name followed by its description (includes the whole doc string)",
         "store"),
    )

    def __init__(self):
        Plugin.__init__(self)

    def options(self, parser, env):
        super(CustomDescription, self).options(parser, env)
        for name, help_, action in self._options:
            env_opt = "NOSE_%s" % name.upper()
            parser.add_option("--%s" % name.replace("_", "-"),
                              action=action,
                              dest=name,
                              default=env.get(env_opt) or '0',
                              help=help_ % env_opt)

    def configure(self, options, conf):
        super(CustomDescription, self).configure(options, conf)
        for name, _, _ in self._options:
            setattr(self, name, getattr(options, name))

    def describeTest(self, test):
        if self.custom_description == '0':
            output = str(test) or None
        elif self.custom_description == '1':
            doc = test.test._testMethodDoc
            output = (doc + '\n\n') if doc else None
        elif self.custom_description == '2':
            doc = test.test._testMethodDoc
            output = (str(test) + '\nDescription:\n' + doc + '\n\n') or None
        else:
            raise ValueError('Unsupported value [%s] for --custom-description' %
                             self.custom_description)
        return output
