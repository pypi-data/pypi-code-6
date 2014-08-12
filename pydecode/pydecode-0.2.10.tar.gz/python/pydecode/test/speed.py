import pydecode.hypergraph_tests as ht
import pydecode.utils as utils


def test_lp():
    import pydecode.lp as lp
    h = ht.chain_hypergraph(1000)
    w = utils.random_log_viterbi_potentials(h)
    print "build", len(h.edges), len(h.nodes)
    g = lp.HypergraphLP.make_lp(h, w)


test_lp()
