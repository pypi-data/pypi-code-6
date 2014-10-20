import time


all_tests = ['test1', 'test2', 'test3', 'test4', 'test5', 'test6',
             #'test7',
             'test8', 'test9']


def test1(session):
    yield '^d^k^k12345<enter><home><home>^k^p^p^a^k^p^p^a^k^p^p^p^p.<enter>'
    yield '# hello<enter>'
    yield 'A' * 25 * 1
    yield '<up>^a^b^b<down>^c<page-up>^p'
    yield 'if 1:<enter>a = 1<enter>b = a'
    yield '<enter>^x^w<bs><bs><bs><bs>self-test.txt<enter>^q'
test1.args = ['asdf']


def test2(session):
    yield '<home><home>^shello^s <home>^b^b<up>^d'
    yield '^sA<right>^k^x^w'
    yield '<bs>' * len('self-test.txt')
    yield 'a.py<enter>'
    yield '^oself-test.txt<enter>^v2^q'
test2.args = ['self-test.txt']


def test3(session):
    session.scr.position = (3, 1)
    yield 'a.bc<enter><mouse-clicked>^d'
    assert session.docs[-1].lines[0] == 'abc'
    session.scr.position = (3, 4)
    yield '<mouse-clicked>'
    assert session.docs[-1].view.pos == (1, 0)
    yield '1<enter>2<enter><up><up><up><end><down>'
    assert session.docs[-1].view.pos == (1, 1)
    yield '^q'


def test4(session):
    with open('x.py', 'w') as fd:
        fd.write('a = {\n}')
        fd.close()
    yield '^ox.py<enter>'
    assert session.docs[-1].lines[1] == '}'
    yield '^q'

    
def test5(session):
    yield 'from spelltink<tab>'
    assert session.docs[-1].lines[0].endswith('spelltinkle')
    yield '.ru<tab>'
    assert session.docs[-1].lines[0].endswith('spelltinkle.run')
    yield ' import ru<tab>'
    assert session.docs[-1].lines[0].endswith('run')
    yield '^q'


def test6(session):
    yield '^ox.<tab><enter><end><end><enter>aa<enter>aaa<enter>aaaa<enter>'
    yield '<home><home>^fa<enter>xx<enter>ynyyynn!<down>.^w'
    assert ('-'.join(session.docs[-1].lines) ==
            'xx = {-}-axx-xxxxa-axxxxxx-.')
    yield '^q'

    
def test7(session):
    yield '({[()]})<home>'
    c = session.docs[-1].color.colors[0]
    assert c[0] // 28 == 3, c
    yield '<end>'
    assert c[0] // 28 == 3, c
    yield '^q'


def test8(session):
    yield '1<enter>2<enter>3<enter>'
    yield '<home><home>^k^k<down>^x^k^k<up>^p<bs>^a<bs>'
    assert session.docs[-1].lines[0] == '132'
    yield '^q'

    
def test9(session):
    yield 'abc<enter>'
    yield '123<enter>'
    session.scr.position = (4, 1)
    yield '<mouse-clicked>'
    session.scr.position = (5, 2)
    yield '<mouse-released>'
    time.sleep(0.5)
    session.scr.position = (3, 1)
    yield '<mouse2-clicked>'
    assert ''.join(session.doc.lines) == 'c123abc123'
    yield '^q'
