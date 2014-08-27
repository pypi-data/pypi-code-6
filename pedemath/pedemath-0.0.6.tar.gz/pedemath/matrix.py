
"""
Matrix44
A 4x4 matrix class stored in column major order for easier use with OpenGL.
"""

import math

from numpy import array

from pedemath.vec3 import Vec3

_np_column_major_order = "F"


def _dot_matrix44(m1, m2):
    """
    Multiply/compute the dot product of two matrices.

    Input: Two matrices each as a 2d numpy array.
    Output: dot product of the two matrices.
    """
    # TODO: Investigate improving performance with numpy.

    columns = [
        [m1[0][row] * m2[col][0] +
         m1[1][row] * m2[col][1] +
         m1[2][row] * m2[col][2] +
         m1[3][row] * m2[col][3] for row in range(4)]
        for col in range(4)
        ]

    result = array(columns, dtype="float32",
                   order=_np_column_major_order)
    return result


def transpose_mat44(src_mat, transpose_mat=None):
    """Create a transpose of a matrix."""

    if not transpose_mat:
        transpose_mat = Matrix44()

    for i in range(4):
        for j in range(4):
            transpose_mat.data[i][j] = src_mat.data[j][i]

    return transpose_mat


class Matrix44(object):
    # Use column-major order  data[col][row]  for OpenGL compatibility.
    # TODO: write a similar class with numpy or just use and test perf.
    #
    # Column-major indexes:
    #  0,0 | 1,0 | 2,0 | 3,0 (trans)
    #  0,1 | 1,1 | 2,1 | 3,1 (trans)
    #  0,2 | 1,2 | 2,2 | 3,2 (trans)
    #  0,3 | 1,3 | 2,3 | 3,3

    def __init__(self):
        self.make_identity()

    def make_identity(self):

        # Column-major, similar to OpenGL
        self.data = array([[1, 0, 0, 0],  # Note: columns look like rows here
                           [0, 1, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]], dtype="float32",
                          order=_np_column_major_order)

    def __str__(self):
        """Return a readable string representation of Matrix44.
        Data is in column major order like OpenGL, so we can't just print
        out rows.
        """

        matrix_string = (
            "Matrix44:\n" +
            "\t%9.6f, %9.6f, %9.6f, %9.6f,\n" +
            "\t%9.6f, %9.6f, %9.6f, %9.6f,\n" +
            "\t%9.6f, %9.6f, %9.6f, %9.6f,\n" +
            "\t%9.6f, %9.6f, %9.6f, %6.6f")

        return matrix_string % (
            self.data[0][0], self.data[1][0], self.data[2][0], self.data[3][0],
            self.data[0][1], self.data[1][1], self.data[2][1], self.data[3][1],
            self.data[0][2], self.data[1][2], self.data[2][2], self.data[3][2],
            self.data[0][3], self.data[1][3], self.data[2][3], self.data[3][3])

    #def __repr__(self):
    #    """Return an unambiguous string representation of Matrix44."""

    def __rsub__(self, other):
        if isinstance(other, Matrix44):
            self.data = self.data - other.data
        else:
            raise Exception(
                "Matrix.__rsub__ arg is not a matrix. %s" % type(other))

    def __sub__(self, other):
        if isinstance(other, Matrix44):
            mat = Matrix44()
            mat.data = self.data - other.data
            return mat
        else:
            raise Exception(
                "Matrix.__sub__ arg is not a matrix. %s" % type(other))

    def __radd__(self, other):
        if isinstance(other, Matrix44):
            self.data = self.data + other.data
        else:
            raise Exception(
                "Matrix.__sub__ arg is not a matrix. %s" % type(other))

    def __add__(self, other):
        if isinstance(other, Matrix44):
            mat = Matrix44()
            mat.data = self.data + other.data
            return mat
        else:
            raise Exception(
                "Matrix.__add__ arg is not a matrix. %s" % type(other))

    def __rmul__(self, other):
        if isinstance(other, Matrix44):
            self.data = _dot_matrix44(self.data, other.data)
        else:
            raise Exception(
                "Matrix44.__rmul__, arg is not a matrix: %s" % type(other))

    def __mul__(self, other):
        if isinstance(other, Matrix44):
            mat = Matrix44()
            mat.data = _dot_matrix44(self.data, other.data)
            return mat
        elif isinstance(other, Vec3):
            v = other
            # just copied from above, delete above checks
            return Vec3(v[0]*self.data[0][0] + v[1] * self.data[1][0] +
                        v[2] * self.data[2][0] + self.data[3][0],
                        v[0] * self.data[0][1] + v[1] * self.data[1][1] +
                        v[2] * self.data[2][1] + self.data[3][1],
                        v[0] * self.data[0][2] + v[1] * self.data[1][2] +
                        v[2] * self.data[2][2] + self.data[3][2])
        else:
            raise Exception("Matrix44.__mul__ unhandled type %s" % type(other))

    def __eq__(self, mat2):
        """Return True if the values in mat2 equal the values in this
        matrix.
        """

        if not hasattr(mat2, "data"):
            return False

        for i in range(4):
            if not (self.data[i][0] == mat2.data[i][0] and
                    self.data[i][1] == mat2.data[i][1] and
                    self.data[i][2] == mat2.data[i][2] and
                    self.data[i][3] == mat2.data[i][3]):
                return False

        return True

    def set_x(self, vec3_a):
        self.data[0][0] = vec3_a[0]
        self.data[0][1] = vec3_a[1]
        self.data[0][2] = vec3_a[2]

    def set_y(self, vec3_a):
        self.data[1][0] = vec3_a[0]
        self.data[1][1] = vec3_a[1]
        self.data[1][2] = vec3_a[2]

    def set_z(self, vec3_a):
        self.data[2][0] = vec3_a[0]
        self.data[2][1] = vec3_a[1]
        self.data[2][2] = vec3_a[2]

    def z(self):
        return self.data[2]

    def get_data_gl(self):
        # We are using column-major format, the same as OpenGL
        return self.data

    @staticmethod
    def from_axis_angle(axis, angle):
        c = math.cos(angle)
        s = math.sin(angle)
        t = 1.0 - c
        # normalize
        axis_length = axis.length()

        #raise if length is < 0?

        axis.x /= axis_length
        axis.y /= axis_length
        axis.z /= axis_length

        m = Matrix44()
        m.data[0][0] = c + axis.x*axis.x*t
        m.data[1][1] = c + axis.y*axis.y*t
        m.data[2][2] = c + axis.z*axis.z*t

        tmp1 = axis.x * axis.y * t
        tmp2 = axis.z * s
        m.data[1][0] = tmp1 + tmp2
        m.data[0][1] = tmp1 - tmp2
        tmp1 = axis.x * axis.z * t
        tmp2 = axis.y * s
        m.data[2][0] = tmp1 - tmp2
        m.data[0][2] = tmp1 + tmp2
        tmp1 = axis.y*axis.z*t
        tmp2 = axis.x*s
        m.data[2][1] = tmp1 + tmp2
        m.data[1][2] = tmp1 - tmp2

        return m

    @staticmethod
    def rot_from_vectors(start_vec, end_vec):
        """Return the rotation matrix to rotate from one vector to another."""

        dot = start_vec.dot(end_vec)
        # TODO: check if dot is a valid number
        angle = math.acos(dot)
        # TODO: check if angle is a valid number
        cross = start_vec.cross(end_vec)
        cross.normalize
        rot_matrix = Matrix44.from_axis_angle(cross, angle)

        # TODO: catch exception and return identity for invalid numbers
        return rot_matrix

    @staticmethod
    def from_trans(trans_vec):
        mat = Matrix44()
        # column major,  translation components in column 3
        mat.data[3][0] = trans_vec[0]
        mat.data[3][1] = trans_vec[1]
        mat.data[3][2] = trans_vec[2]
        return mat

    def get_trans(self):
        return Vec3(*self.data[3][:3])

    @staticmethod
    def from_rot_x(angle_degrees):
        mat = Matrix44()
        c = math.cos(angle_degrees * math.pi / 180.)
        s = math.sin(angle_degrees * math.pi / 180.)

        #  1  0    0  0
        #  0 cos -sin 0
        #  0 sin  cos 0
        #  0  0    0  1

        #   [column][row]
        mat.data[1][1] = c
        mat.data[2][1] = -s
        mat.data[1][2] = s
        mat.data[2][2] = c
        return mat

    @staticmethod
    def from_rot_y(angle_degrees):

        mat = Matrix44()
        c = math.cos(angle_degrees * math.pi / 180.)
        s = math.sin(angle_degrees * math.pi / 180.)

        #  cos 0 sin  0
        #   0  1  0   0
        # -sin 0 cos  0
        #   0  0  0   1

        #   [column][row]
        mat.data[0][0] = c
        mat.data[2][0] = s
        mat.data[0][2] = -s
        mat.data[2][2] = c
        return mat

    @staticmethod
    def from_rot_z(angle_degrees):
        mat = Matrix44()
        c = math.cos(angle_degrees * math.pi / 180.)
        s = math.sin(angle_degrees * math.pi / 180.)

        #  cos -sin 0 0
        #  sin  cos 0 0
        #   0    0  1 0
        #   0    0  0 1

        #   [column][row]
        mat.data[0][0] = c
        mat.data[1][0] = -s
        mat.data[0][1] = s
        mat.data[1][1] = c
        return mat


def rotate_v3f_deg_xyz(vec_a, rot):
    rot_mat = Matrix44.from_rot_x(rot[0])
    new_vec = rot_mat * vec_a

    rotMat = Matrix44.from_rot_y(rot[1])
    new_vec = rotMat * new_vec

    rot_mat = Matrix44.from_rot_z(rot[2])
    new_vec = rot_mat * new_vec
    return new_vec


if __name__ == "__main__":
    # TODO: Finish moving all these to unittests.

    print "Identity:"
    m = Matrix44()
    print m.data

    print "Add:"
    m2 = Matrix44()
    m2.data[0][0] = 5
    m2.data[0][1] = 5
    m2.data[0][2] = 5
    m2.data[0][3] = 5
    print (m + m2).data

    print "Subtract:"
    print (m - m2).data

    print "Multiply:"
    print (m * m2).data

    print "matrix44_trans:"
    m3 = matrix44_trans(Vec3(2, 3, 4))
    print m3.data

    print "matrix44_rot_y:"
    m4 = matrix44_rot_y(45)
    print m4.data

    print "unit x vec rotated by 45:"
    v = Vec3(1, 0, 0)
    print m4 * v

    print "unit x vec rotated by 180:"
    print matrix44_rot_y(180) * v

    print "unit x vec translateed by -5,6,-7:"
    print matrix44_trans(Vec3(-5, 6, -7)) * v

    print "translated and rotated origin:"
    print matrix44_rot_y(45) * matrix44_trans(Vec3(1, 0, 0)) * Vec3(0, 0, 0)
    print "a:", matrix44_trans(Vec3(1, 0, 0)) * Vec3(0, 0, 0)
    print "b:", matrix44_rot_y(45) * (
        matrix44_trans(Vec3(1, 0, 0)) * Vec3(0, 0, 0))
    c = matrix44_rot_y(45) * matrix44_trans(Vec3(1, 0, 0))
    print "c:", c
    print "c.5:", c*Vec3(0, 0, 0)
    print "d:", matrix44_rot_y(45) * matrix44_trans(
        Vec3(1, 0, 0)) * Vec3(1, 0, 0)
    print "e:", matrix44_trans(Vec3(1, 0, 0)) * matrix44_trans(
        Vec3(1, 0, 0)) * matrix44_trans(Vec3(0, 1, 0)) * matrix44_trans(
            Vec3(0, 0, 1))
    print "f:", matrix44_rot_y(45) * Vec3(1, 0, 0)
    print "right:", (matrix44_rot_y(45) * matrix44_trans(
        Vec3(1, 0, 0))) * Vec3(0, 0, 0)
    print "right 2 (r t i):", (matrix44_rot_y(45) * matrix44_trans(
        Vec3(1, 0, 0))) * Vec3(0, 0, 1)
    print "right 3 (t r i):", (matrix44_trans(
        Vec3(1, 0, 0)) * matrix44_rot_y(45)) * Vec3(0, 0, 1)
    print "      3b (t r i):", (matrix44_trans(
        Vec3(1, 0, 0)) * matrix44_rot_y(45)) * Vec3(0, 0, 1)
    print "correct 4 (t r i):", (matrix44_trans(
        Vec3(1, 0, 0)) * matrix44_rot_y(90)) * Vec3(0, 0, 1)
    print "        4a (t r i):", matrix44_rot_y(90) * Vec3(0, 0, 1)

    rot_matrix = Matrix44.rot_from_vectors(Vec3(0, 0, -1), Vec3(0.0, -0.5, 0.0))
    print "rot_matrix:", rot_matrix.data
    print "rotated -z axis is:", rot_matrix * Vec3(0, 0, -1)
