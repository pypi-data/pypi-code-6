import pydecode.hyper as ph
import random
import pydecode.nlp.multinomial as multi


def test_multinomial():
    tab = multi.MultinomialTable()
    for i in range(12):
        for j in range(12):
            tab.inc((i,j), random.random())
    tab.reestimate()

    lattice = ph.make_lattice(10, 10, [[i for i in range(10)]] * 10)

    def label_map(label):
        return label.i%4, label.j

    ll = multi.em(tab, label_map, lattice, epochs=100)
    print ll
    for i in range(1, len(ll)):
        assert(ll[i] >= ll[i-1]-1e-4)
    assert(0)
