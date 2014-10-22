from nose.tools import assert_equal
import openvcdiff

def test_trivial():
    dictionary = "this is a simple test for vcdiff here"
    target = "in fact this is a really simple test"

    delta = openvcdiff.encode(target, dictionary)
    reconstructed = openvcdiff.decode(delta, dictionary)
    assert_equal(target, reconstructed)    

def test_using_dictionary():
    dictionary = "base dictionary for multiple deltas"
    hashdict = openvcdiff.HashedDictionary(dictionary)
    targets = ["first target encoded w/ base dictionary for deltas",
            "second target encoded w/ base dictionary for deltas"]
    deltas = [openvcdiff.encode(target, hashdict) for target in targets]
    reconstructed = [openvcdiff.decode(delta, dictionary) for delta in deltas]
    assert_equal(targets, reconstructed)

