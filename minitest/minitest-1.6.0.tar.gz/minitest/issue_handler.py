
if __name__ == '__main__':
    from minitest import *

    with test("for loop"):
        for i in range(3):
            i.p()
            i.must_equal(i)
            'true'.must_equal('true')