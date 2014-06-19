#!/usr/bin/env python

# local libraries
from .models import generate_n_link_pendulum_equations_of_motion


class TestOctaveMatrixPrinter():
    self.expected_m = \
"""m(0, 0) = 1;
m(0, 1) = 0;
m(0, 2) = 0;
m(0, 3) = 0;
m(0, 4) = 0;
m(0, 5) = 0;
m(1, 0) = 0;
m(1, 1) = 1;
m(1, 2) = 0;
m(1, 3) = 0;
m(1, 4) = 0;
m(1, 5) = 0;
m(2, 0) = 0;
m(2, 1) = 0;
m(2, 2) = 1;
m(2, 3) = 0;
m(2, 4) = 0;
m(2, 5) = 0;
m(3, 0) = 0;
m(3, 1) = 0;
m(3, 2) = 0;
m(3, 3) = m0 + m1 + m2;
m(3, 4) = -l0*(m1 + m2)*sin(q1);
m(3, 5) = -l1*m2*sin(q2);
m(4, 0) = 0;
m(4, 1) = 0;
m(4, 2) = 0;
m(4, 3) = -l0*(m1 + m2)*sin(q1);
m(4, 4) = l0^2*(m1 + m2);
m(4, 5) = l0*l1*m2*cos(q1 - q2);
m(5, 0) = 0;
m(5, 1) = 0;
m(5, 2) = 0;
m(5, 3) = -l1*m2*sin(q2);
m(5, 4) = l0*l1*m2*cos(q1 - q2);
m(5, 5) = l1^2*m2;"""

    expected_f = \
"""f(0) = u0;
f(1) = u1;
f(2) = u2;
f(3) = l0*m1*u1^2*cos(q1) + l0*m2*u1^2*cos(q1) + l1*m2*u2^2*cos(q2);
f(4) = -l0*(g*m1*cos(q1) + g*m2*cos(q1) + l1*m2*u2^2*sin(q1 - q2));
f(5) = l1*m2*(-g*cos(q2) + l0*u1^2*sin(q1 - q2));"""

    expected_m_cse =\
"""x0 = m1 + m2
x1 = q1
x2 = -l0*x0*sin(x1)
x3 = l1*m2
x4 = q2
x5 = -x3*sin(x4)
x6 = l0*x3*cos(x1 - x4)

m(0, 0) = 1
m(0, 1) = 0
m(0, 2) = 0
m(0, 3) = 0
m(0, 4) = 0
m(0, 5) = 0
m(1, 0) = 0
m(1, 1) = 1
m(1, 2) = 0
m(1, 3) = 0
m(1, 4) = 0
m(1, 5) = 0
m(2, 0) = 0
m(2, 1) = 0
m(2, 2) = 1
m(2, 3) = 0
m(2, 4) = 0
m(2, 5) = 0
m(3, 0) = 0
m(3, 1) = 0
m(3, 2) = 0
m(3, 3) = m0 + x0
m(3, 4) = x2
m(3, 5) = x5
m(4, 0) = 0
m(4, 1) = 0
m(4, 2) = 0
m(4, 3) = x2
m(4, 4) = l0^2*x0
m(4, 5) = x6
m(5, 0) = 0
m(5, 1) = 0
m(5, 2) = 0
m(5, 3) = x5
m(5, 4) = x6
m(5, 5) = l1^2*m2"""

    expected_m_f_cse =\
"""x0 = m1 + m2;
x1 = q1;
x2 = -l0*x0*sin(x1);
x3 = l1*m2;
x4 = q2;
x5 = -x3*sin(x4);
x6 = x1 - x4;
x7 = l0*x3*cos(x6);
x8 = u1;
x9 = u2;
x10 = cos(x1);
x11 = x8^2;
x12 = l0*x10*x11;
x13 = cos(x4);
x14 = l1*m2*x9^2;
x15 = g*x10;
x16 = sin(x6);

m(0, 0) = 1;
m(0, 1) = 0;
m(0, 2) = 0;
m(0, 3) = 0;
m(0, 4) = 0;
m(0, 5) = 0;
m(1, 0) = 0;
m(1, 1) = 1;
m(1, 2) = 0;
m(1, 3) = 0;
m(1, 4) = 0;
m(1, 5) = 0;
m(2, 0) = 0;
m(2, 1) = 0;
m(2, 2) = 1;
m(2, 3) = 0;
m(2, 4) = 0;
m(2, 5) = 0;
m(3, 0) = 0;
m(3, 1) = 0;
m(3, 2) = 0;
m(3, 3) = m0 + x0;
m(3, 4) = x2;
m(3, 5) = x5;
m(4, 0) = 0;
m(4, 1) = 0;
m(4, 2) = 0;
m(4, 3) = x2;
m(4, 4) = l0^2*x0;
m(4, 5) = x7;
m(5, 0) = 0;
m(5, 1) = 0;
m(5, 2) = 0;
m(5, 3) = x5;
m(5, 4) = x7;
m(5, 5) = l1^2*m2;

f(0) = u0;
f(1) = x8;
f(2) = x9;
f(3) = m1*x12 + m2*x12 + x13*x14;
f(4) = -l0*(m1*x15 + m2*x15 + x14*x16);
f(5) = x3*(-g*x13 + l0*x11*x16);"""

    def setup(self):
        res = generate_n_link_pendulum_equations_of_motion(2, False)
        res[0].simplify()
        res[1].simplify()
        self.mass_matrix = res[0]
        self.forcing_vector = res[1]
        self.printer = NumPyMatrixPrinter()

    def test_print(self):
        actual = self.printer.print({'m': self.mass_matrix})
        assert actual == self.expected_m

    def test_print_multiple(self):
        actual = self.printer.print({'m':self.mass_matrix, 'f': self.forcing_vector})
        assert actual == self.expected_m + '\n' + self.expected_f

    def test_print_with_cse(self):
        actual = self.printer.print({'m': self.mass_matrix}, cse=True)
        assert actual == self.expected_m + '\n' + self.expected_f

    def test_print_with_cse_multiple(self):
        actual = self.printer.print({'m':self.mass_matrix, 'f': self.forcing_vector}, cse=True)
        assert actual == self.expected_m_f_cse


class TestNumPyMatrixPrinter():
    self.expected_m = \
"""m[0, 0] = 1
m[0, 1] = 0
m[0, 2] = 0
m[0, 3] = 0
m[0, 4] = 0
m[0, 5] = 0
m[1, 0] = 0
m[1, 1] = 1
m[1, 2] = 0
m[1, 3] = 0
m[1, 4] = 0
m[1, 5] = 0
m[2, 0] = 0
m[2, 1] = 0
m[2, 2] = 1
m[2, 3] = 0
m[2, 4] = 0
m[2, 5] = 0
m[3, 0] = 0
m[3, 1] = 0
m[3, 2] = 0
m[3, 3] = m0 + m1 + m2
m[3, 4] = -l0*(m1 + m2)*sin(q1)
m[3, 5] = -l1*m2*sin(q2)
m[4, 0] = 0
m[4, 1] = 0
m[4, 2] = 0
m[4, 3] = -l0*(m1 + m2)*sin(q1)
m[4, 4] = l0**2*(m1 + m2)
m[4, 5] = l0*l1*m2*cos(q1 - q2)
m[5, 0] = 0
m[5, 1] = 0
m[5, 2] = 0
m[5, 3] = -l1*m2*sin(q2)
m[5, 4] = l0*l1*m2*cos(q1 - q2)
m[5, 5] = l1**2*m2"""

    expected_f = \
"""f[0] = u0
f[1] = u1
f[2] = u2
f[3] = l0*m1*u1**2*cos(q1) + l0*m2*u1**2*cos(q1) + l1*m2*u2**2*cos(q2)
f[4] = -l0*(g*m1*cos(q1) + g*m2*cos(q1) + l1*m2*u2**2*sin(q1 - q2))
f[5] = l1*m2*(-g*cos(q2) + l0*u1**2*sin(q1 - q2))
"""

    expected_m_cse =\
"""
x0 = m1 + m2
x1 = q1
x2 = -l0*x0*sin(x1)
x3 = l1*m2
x4 = q2
x5 = -x3*sin(x4)
x6 = l0*x3*cos(x1 - x4)

m[0, 0] = 1
m[0, 1] = 0
m[0, 2] = 0
m[0, 3] = 0
m[0, 4] = 0
m[0, 5] = 0
m[1, 0] = 0
m[1, 1] = 1
m[1, 2] = 0
m[1, 3] = 0
m[1, 4] = 0
m[1, 5] = 0
m[2, 0] = 0
m[2, 1] = 0
m[2, 2] = 1
m[2, 3] = 0
m[2, 4] = 0
m[2, 5] = 0
m[3, 0] = 0
m[3, 1] = 0
m[3, 2] = 0
m[3, 3] = m0 + x0
m[3, 4] = x2
m[3, 5] = x5
m[4, 0] = 0
m[4, 1] = 0
m[4, 2] = 0
m[4, 3] = x2
m[4, 4] = l0**2*x0
m[4, 5] = x6
m[5, 0] = 0
m[5, 1] = 0
m[5, 2] = 0
m[5, 3] = x5
m[5, 4] = x6
m[5, 5] = l1**2*m2"""

    expected_m_f_cse =\
"""x0 = m1 + m2
x1 = q1
x2 = -l0*x0*sin(x1)
x3 = l1*m2
x4 = q2
x5 = -x3*sin(x4)
x6 = x1 - x4
x7 = l0*x3*cos(x6)
x8 = u1
x9 = u2
x10 = cos(x1)
x11 = x8**2
x12 = l0*x10*x11
x13 = cos(x4)
x14 = l1*m2*x9**2
x15 = g*x10
x16 = sin(x6)

m[0, 0] = 1
m[0, 1] = 0
m[0, 2] = 0
m[0, 3] = 0
m[0, 4] = 0
m[0, 5] = 0
m[1, 0] = 0
m[1, 1] = 1
m[1, 2] = 0
m[1, 3] = 0
m[1, 4] = 0
m[1, 5] = 0
m[2, 0] = 0
m[2, 1] = 0
m[2, 2] = 1
m[2, 3] = 0
m[2, 4] = 0
m[2, 5] = 0
m[3, 0] = 0
m[3, 1] = 0
m[3, 2] = 0
m[3, 3] = m0 + x0
m[3, 4] = x2
m[3, 5] = x5
m[4, 0] = 0
m[4, 1] = 0
m[4, 2] = 0
m[4, 3] = x2
m[4, 4] = l0**2*x0
m[4, 5] = x7
m[5, 0] = 0
m[5, 1] = 0
m[5, 2] = 0
m[5, 3] = x5
m[5, 4] = x7
m[5, 5] = l1**2*m2

f[0] = u0
f[1] = x8
f[2] = x9
f[3] = m1*x12 + m2*x12 + x13*x14
f[4] = -l0*(m1*x15 + m2*x15 + x14*x16)
f[5] = x3*(-g*x13 + l0*x11*x16)"""

    def setup(self):
        res = generate_n_link_pendulum_equations_of_motion(2, False)
        res[0].simplify()
        res[1].simplify()
        self.mass_matrix = res[0]
        self.forcing_vector = res[1]
        self.printer = NumPyMatrixPrinter()

    def test_print(self):
        actual = self.printer.print({'m': self.mass_matrix})
        assert actual == self.expected_m

    def test_print_multiple(self):
        actual = self.printer.print({'m':self.mass_matrix, 'f': self.forcing_vector})
        assert actual == self.expected_m + '\n' + self.expected_f

    def test_print_with_cse(self):
        actual = self.printer.print({'m': self.mass_matrix}, cse=True)
        assert actual == self.expected_m + '\n' + self.expected_f

    def test_print_with_cse_multiple(self):
        actual = self.printer.print({'m':self.mass_matrix, 'f': self.forcing_vector}, cse=True)
        assert actual == self.expected_m_f_cse


class TestCMatrixPrinter():
    self.expected_m = \
"""m[0][0] = 1;
m[0][1] = 0;
m[0][2] = 0;
m[0][3] = 0;
m[0][4] = 0;
m[0][5] = 0;
m[1][0] = 0;
m[1][1] = 1;
m[1][2] = 0;
m[1][3] = 0;
m[1][4] = 0;
m[1][5] = 0;
m[2][0] = 0;
m[2][1] = 0;
m[2][2] = 1;
m[2][3] = 0;
m[2][4] = 0;
m[2][5] = 0;
m[3][0] = 0;
m[3][1] = 0;
m[3][2] = 0;
m[3][3] = m0 + m1 + m2;
m[3][4] = -l0*(m1 + m2)*sin(q1);
m[3][5] = -l1*m2*sin(q2);
m[4][0] = 0;
m[4][1] = 0;
m[4][2] = 0;
m[4][3] = -l0*(m1 + m2)*sin(q1);
m[4][4] = pow(l0, 2)*(m1 + m2);
m[4][5] = l0*l1*m2*cos(q1 - q2);
m[5][0] = 0;
m[5][1] = 0;
m[5][2] = 0;
m[5][3] = -l1*m2*sin(q2);
m[5][4] = l0*l1*m2*cos(q1 - q2);
m[5][5] = pow(l1, 2)*m2;"""

    expected_f = \
"""f[0] = u0;
f[1] = u1;
f[2] = u2;
f[3] = l0*m1*pow(u1, 2)*cos(q1) + l0*m2*pow(u1, 2)*cos(q1) + l1*m2*pow(u2, 2)*cos(q2);
f[4] = -l0*(g*m1*cos(q1) + g*m2*cos(q1) + l1*m2*pow(u2, 2)*sin(q1 - q2));
f[5] = l1*m2*(-g*cos(q2) + l0*pow(u1, 2)*sin(q1 - q2));"""

    expected_m_cse =\
"""double x0 = m1 + m2;
double x1 = q1;
double x2 = -l0*x0*sin(x1);
double x3 = l1*m2;
double x4 = q2;
double x5 = -x3*sin(x4);
double x6 = l0*x3*cos(x1 - x4);

m[0][0] = 1;
m[0][1] = 0;
m[0][2] = 0;
m[0][3] = 0;
m[0][4] = 0;
m[0][5] = 0;
m[1][0] = 0;
m[1][1] = 1;
m[1][2] = 0;
m[1][3] = 0;
m[1][4] = 0;
m[1][5] = 0;
m[2][0] = 0;
m[2][1] = 0;
m[2][2] = 1;
m[2][3] = 0;
m[2][4] = 0;
m[2][5] = 0;
m[3][0] = 0;
m[3][1] = 0;
m[3][2] = 0;
m[3][3] = m0 + x0;
m[3][4] = x2;
m[3][5] = x5;
m[4][0] = 0;
m[4][1] = 0;
m[4][2] = 0;
m[4][3] = x2;
m[4][4] = pow(l0, 2)*x0;
m[4][5] = x6;
m[5][0] = 0;
m[5][1] = 0;
m[5][2] = 0;
m[5][3] = x5;
m[5][4] = x6;
m[5][5] = pow(l1, 2)*m2;"""

    expected_m_f_cse =\
"""double x0 = m1 + m2;
double x1 = q1;
double x2 = -l0*x0*sin(x1);
double x3 = l1*m2;
double x4 = q2;
double x5 = -x3*sin(x4);
double x6 = x1 - x4;
double x7 = l0*x3*cos(x6);
double x8 = u1;
double x9 = u2;
double x10 = cos(x1);
double x11 = x8**2;
double x12 = l0*x10*x11;
double x13 = cos(x4);
double x14 = l1*m2*x9**2;
double x15 = g*x10;
double x16 = sin(x6);

m[0][0] = 1;
m[0][1] = 0;
m[0][2] = 0;
m[0][3] = 0;
m[0][4] = 0;
m[0][5] = 0;
m[1][0] = 0;
m[1][1] = 1;
m[1][2] = 0;
m[1][3] = 0;
m[1][4] = 0;
m[1][5] = 0;
m[2][0] = 0;
m[2][1] = 0;
m[2][2] = 1;
m[2][3] = 0;
m[2][4] = 0;
m[2][5] = 0;
m[3][0] = 0;
m[3][1] = 0;
m[3][2] = 0;
m[3][3] = m0 + x0;
m[3][4] = x2;
m[3][5] = x5;
m[4][0] = 0;
m[4][1] = 0;
m[4][2] = 0;
m[4][3] = x2;
m[4][4] = pow(l0, 2)*x0;
m[4][5] = x7;
m[5][0] = 0;
m[5][1] = 0;
m[5][2] = 0;
m[5][3] = x5;
m[5][4] = x7;
m[5][5] = pow(l1, 2)*m2;

f[0] = u0;
f[1] = x8;
f[2] = x9;
f[3] = m1*x12 + m2*x12 + x13*x14;
f[4] = -l0*(m1*x15 + m2*x15 + x14*x16);
f[5] = x3*(-g*x13 + l0*x11*x16);"""

    def setup(self):
        res = generate_n_link_pendulum_equations_of_motion(2, False)
        res[0].simplify()
        res[1].simplify()
        self.mass_matrix = res[0]
        self.forcing_vector = res[1]
        self.printer = CMatrixPrinter()

    def test_print(self):
        actual = self.printer.print({'m': self.mass_matrix})
        assert actual == self.expected_m

    def test_print_multiple(self):
        actual = self.printer.print({'m': self.mass_matrix, 'f':
                                     self.forcing_vector})
        assert actual == self.expected_m + '\n' + self.expected_f

    def test_print_with_cse(self):
        actual = self.printer.print({'m': self.mass_matrix}, cse=True)
        assert actual == self.expected_m + '\n' + self.expected_f

    def test_print_with_cse_multiple(self):
        actual = self.printer.print({'m': self.mass_matrix, 'f':
                                     self.forcing_vector}, cse=True)
        assert actual == self.expected_m_f_cse
