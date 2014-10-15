from numpy import empty

from .sensorimotor_model import SensorimotorModel


class Dummy(SensorimotorModel):
    def __init__(self, conf):  # , n_components=None):
        SensorimotorModel.__init__(self, conf)

    def infer(self, in_dims, out_dims, x):
        return empty(len(out_dims))

    def update(self, m, s):
        pass

configurations = {'default': {}}
sensorimotor_models = {'dummy': (Dummy, configurations)}
