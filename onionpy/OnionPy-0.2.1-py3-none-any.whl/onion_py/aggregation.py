"""
Aggregation objects for OnionOO
"""

"""
Averages the consensus weight, bandwidth, respective fractions, and guard/middle/exit probabilities of a set of relay detail documents
"""
class AverageRelay:
  def __init__(self, relays):
    self.relays = relays

    self.consensus_weight = sum(r.consensus_weight for r in relays) / len(relays)
    self.bandwidth = (
        sum(r.bandwidth[0] for r in relays) / len(relays),
        sum(r.bandwidth[1] for r in relays) / len(relays),
        sum(r.bandwidth[2] for r in relays) / len(relays),
        sum(r.bandwidth[3] for r in relays) / len(relays),
        )
    self.advertised_bandwidth_fraction = sum(r.advertised_bandwidth_fraction for r in relays) / len(relays)
    self.consensus_weight_fraction = sum(r.consensus_weight_fraction for r in relays) / len(relays)
    self.guard_probability = sum(r.guard_probability for r in relays) / len(relays)
    self.middle_probability = sum(r.middle_probability for r in relays) / len(relays)
    self.guard_probability = sum(r.guard_probability for r in relays) / len(relays)

"""
Sums the consensus weight, bandwidth, respective fractions, and guard/middle/exit probabilities of a set of relay detail documents
"""
class SumRelay:
  def __init__(self, relays):
    self.relays = relays

    self.consensus_weight = sum(r.consensus_weight for r in relays)
    self.bandwidth = (
        sum(r.bandwidth[0] for r in relays),
        sum(r.bandwidth[1] for r in relays),
        sum(r.bandwidth[2] for r in relays),
        sum(r.bandwidth[3] for r in relays),
        )
    self.advertised_bandwidth_fraction = sum(r.advertised_bandwidth_fraction for r in relays)
    self.consensus_weight_fraction = sum(r.consensus_weight_fraction for r in relays)
    self.guard_probability = sum(r.guard_probability for r in relays)
    self.middle_probability = sum(r.middle_probability for r in relays)
    self.guard_probability = sum(r.guard_probability for r in relays)

