from abc import ABCMeta
import json

# Constants to indicate if a dictionary key is required
REQUIRED = True
OPTIONAL = False


class DictConvertible(object):
    """
    Abstract base class for classes that can be converted to and from dictionaries.
    """
    __metaclass__ = ABCMeta
    dictionary_attributes = {}

    @classmethod
    def from_dict(cls, d):
        """
        Create an instance from a dictionary.
        """
        assert isinstance(d, dict)
        init_args = dict()
        for key, is_required in cls.dictionary_attributes.iteritems():
            try:
                init_args[key] = d[key]
            except KeyError:
                if is_required:
                    raise DictConvertible.Error('missing key in dictionary', cls, missing_key=key)
        return cls(**init_args)

    @classmethod
    def read_json_file(cls, path):
        """
        Read an instance from a JSON-formatted file.

        :return: A new instance
        """
        with open(path, 'r') as f:
            return cls.from_dict(json.load(f))

    def to_dict(self):
        result = dict()
        for attribute in self.dictionary_attributes.iterkeys():
            attr_value = getattr(self, attribute)
            if isinstance(attr_value, DictConvertible):
                attr_value = attr_value.to_dict()
            result[attribute] = attr_value
        return result

    def write_json_file(self, path):
        """
        Write the instance in JSON format to a file.
        """
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    class Error(Exception):
        """
        Represents an error in the dictionary passed as an argument to the from_dict() method.
        """

        def __init__(self, error, cls, **details):
            super(DictConvertible.Error, self).__init__(error)
            self.error = error
            self.details = dict(details)
            self.details['class'] = cls.__name__


class ExecutionRequest(DictConvertible):
    """
    A request to execute a simulation group on a cluster.
    """
    dictionary_attributes = {
        'simulation_group': REQUIRED,
        'input_files':      OPTIONAL,
    }

    def __init__(self, simulation_group=None, input_files=None):
        self.simulation_group = simulation_group
        self.input_files = input_files

    @classmethod
    def from_dict(cls, d):
        """
        Create an instance from a dictionary.
        """
        execution_request = super(ExecutionRequest, cls).from_dict(d)
        if isinstance(execution_request.simulation_group, dict):
            execution_request.simulation_group = SimulationGroup.from_dict(execution_request.simulation_group)
        return execution_request


class SimulationGroup(DictConvertible):
    """
    A group of related simulations.
    """
    dictionary_attributes = {
        'simulations':     REQUIRED,
        'default_model':   OPTIONAL,
        'default_version': OPTIONAL,
    }

    def __init__(self, simulations=None, default_model=None, default_version=None):
        if simulations is None:
            simulations = []
        self.simulations = simulations
        self.default_model = default_model
        self.default_version = default_version

    def to_dict(self):
        d = super(SimulationGroup, self).to_dict()
        #  d['simulations'] --> same list in self.simulations; each simulation needs converted to a dictionary
        d['simulations'] = [x.to_dict() for x in self.simulations]
        return d

    @classmethod
    def from_dict(cls, d):
        """
        Create an instance from a dictionary.
        """
        instance = super(SimulationGroup, cls).from_dict(d)
        #  instance.simulations is a list of dictionaries; convert each dictionary to a Simulation instance
        instance.simulations = [Simulation.from_dict(x) for x in instance.simulations]
        return instance


class Simulation(DictConvertible):
    """
    An individual model simulation (i.e., the single execution of a simulation model).
    """
    dictionary_attributes = {
        'input_files':   REQUIRED,  # dictionary (local file name --> URL)
        'model':         OPTIONAL,  # if not present, then use the group's default_model
        'model_version': OPTIONAL,  # if not present, then use the group's default_verison
        'cmd_line_args': OPTIONAL,  # list of strings
        'id_on_client':  OPTIONAL,  # string (the id that the client has assigned to the simulation; e.g., PK)
        'output_url':    OPTIONAL,  # string (where to send the simulation's output files)
    }

    def __init__(self, input_files=None, model=None, model_version=None, cmd_line_args=None, id_on_client=None,
                 output_url=None):
        if input_files is None:
            input_files = dict()
        else:
            assert isinstance(input_files, dict)
        self.input_files = input_files
        self.model = model
        self.model_version = model_version
        if cmd_line_args is None:
            cmd_line_args = []
        else:
            assert isinstance(cmd_line_args, (list, tuple))
        self.cmd_line_args = cmd_line_args
        if id_on_client is None:
            id_on_client = ''
        else:
            assert isinstance(id_on_client, basestring)
        self.id_on_client = id_on_client
        self.output_url = output_url

    def to_dict(self):
        d = super(Simulation, self).to_dict()
        #  Copy the two attributes that are data structures just to avoid surprises if the instance's members are
        #  changed later
        d['input_files'] = self.input_files.copy()
        d['cmd_line_args'] = list(self.cmd_line_args)
        return d

    @classmethod
    def from_dict(cls, d):
        """
        Create an instance from a dictionary.
        """
        instance = super(Simulation, cls).from_dict(d)
        #  The instance's input_files and cmd_line_args members still point to data structures in the original
        #  dictionary.  Copy them to avoid surprises if they are changed in the original dictionary.
        instance.input_files = dict(instance.input_files)
        instance.cmd_line_args = list(instance.cmd_line_args)
        return instance