# This file is auto-generated from clustering.idl(0.5.4-179-gb59b61b) with jenerator version 0.5.4-224-g49229fa/develop
# *** DO NOT EDIT ***


import msgpackrpc
import jubatus.common
from .types import *
from jubatus.common.types import *

class Clustering(jubatus.common.ClientBase):
  def __init__(self, host, port, name, timeout=10):
    super(Clustering, self).__init__(host, port, name, timeout)

  def push(self, points):
    return self.jubatus_client.call("push", [points], TBool(), [TList(TDatum(
        ))])

  def get_revision(self):
    return self.jubatus_client.call("get_revision", [], TInt(False, 4), [])

  def get_core_members(self):
    return self.jubatus_client.call("get_core_members", [], TList(TList(
        TUserDef(WeightedDatum))), [])

  def get_k_center(self):
    return self.jubatus_client.call("get_k_center", [], TList(TDatum()), [])

  def get_nearest_center(self, point):
    return self.jubatus_client.call("get_nearest_center", [point], TDatum(),
        [TDatum()])

  def get_nearest_members(self, point):
    return self.jubatus_client.call("get_nearest_members", [point], TList(
        TUserDef(WeightedDatum)), [TDatum()])

  def clear(self):
    return self.jubatus_client.call("clear", [], TBool(), [])
