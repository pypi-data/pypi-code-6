from matplotlib import pylab
import numpy

def square_factory(x, y, h, ax, color = 'red'):
    left = x - 0.5*h
    right = x + 0.5*h
    bottom = y - 0.5*h
    top = y + 0.5*h
    x = (left, right)
    ax.fill_between(x, y1 = top, y2 = bottom, color = color)

def circle_factory(x, y, r, ax, color = 'blue'):
    circle = pylab.Circle((x, y), r, color = color)
    ax.add_patch(circle)

fig = pylab.figure()
ax = fig.add_subplot(111, aspect='equal')
x_list = numpy.arange(1, 10) # X values
y_list = numpy.tile(numpy.ones(1), x_list.size) # Y Values
h_list = numpy.arange(0.9, 0, -0.1) # Square height (also area
r_list = numpy.sqrt(h_list/numpy.pi) # Calculate radius for circle of area h
for x, y, h, r in zip(x_list, y_list, h_list, r_list):
    square_factory(x, y + 1, h, ax)
    circle_factory(x, y, r, ax)
    pylab.text(x, y + 2, str(h))
    ax.set_ylim(0, 4)
ax.set_title('Test plot for package SVGCompress')
pylab.savefig(filename = 'test/matplotlib_test.svg', format = 'svg')
pylab.show()