import pypiview
import pylab
import sys
pylab.ioff()

def test_pypiview():
    p = pypiview.PYPIView('easydev')
    p.plot()
    p = pypiview.PYPIView(['easydev', 'bioservices'])
    p.plot(logy=True)
    pylab.close("all")


def test_help():
    pypiview.help()


def test_main():
    sys.argv = ['pypiview']
    pypiview.main(show=False)

    sys.argv = ['pypiview', 'requests', '--help']
    pypiview.main(show=False)

    sys.argv = ['pypiview', 'requests']
    pypiview.main(show=False)

    sys.argv = ['pypiview', 'requests', '--verbose', '--logy', '--fontsize', '16', '--lw', '2']
    pypiview.main(show=False)
