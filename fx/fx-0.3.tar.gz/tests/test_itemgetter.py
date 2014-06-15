from fx.itemgetter import _, x


def test_x_alias():
    assert _ is x


def test_index():
    seq = [1, 2, 3, 4, 5]

    fst = _[0]
    snd = _[1]
    trd = _[2]

    assert fst(seq) == 1
    assert snd(seq) == 2
    assert trd(seq) == 3


def test_negative_index():
    seq = [1, 2, 3, 4, 5]

    last = _[-1]

    assert last(seq) == 5


def test_slice():
    seq = [1, 2, 3, 4, 5]

    rest = _[1:]

    assert rest(seq) == [2, 3, 4, 5]

    init = _[:-1]

    assert init(seq) == [1, 2, 3, 4]

    odd_indices = _[::2]

    assert odd_indices(seq) == [1, 3, 5]


def test_generator():

    def monty():
        yield 'spam'
        yield 'ham'
        yield 'eggs'

    head, tail = _[0], _[1:]

    assert head(monty()) == 'spam'
    assert list(tail(monty())) == ['ham', 'eggs']


def test_iterable():
    from itertools import count

    second_to_five = _[1:5]

    assert list(second_to_five(count(1))) == [2, 3, 4, 5]


def test_lazy_eval():
    def infinite():
        at = 0
        while True:
            at += 1
            yield at

    the_answer = _[41]

    assert the_answer(infinite()) == 42


def test_chain():
    seq = ['abcde', 'ABCDE']

    car = _[0]

    assert car(seq) == 'abcde'

    caar = car[0]

    assert caar(seq) == 'a'
    assert _[0][0](seq) == 'a'

    cdr = _[1:]
    cddr = cdr[1:]

    assert cddr('ABCDE') == 'CDE'


def test_other_key_type():
    someone = {'name': 'Joe', 'age': 42}

    get_name = _['name']

    assert get_name(someone) == 'Joe'
