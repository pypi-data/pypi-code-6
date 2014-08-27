
import math

from pedemath.matrix import Matrix44
from pedemath.vec3 import add_v3
from pedemath.vec3 import cross_v3
from pedemath.vec3 import normalize_v3
from pedemath.vec3 import scale_v3
from pedemath.vec3 import Vec3


def invert_quat(quat):
    length = quat.length()
    return Quat(
        -quat.x / length, -quat.y / length, -quat.z / length, quat.w / length)


def dot_quat(quat1, quat2):
    return (quat1.x * quat2.x + quat1.y * quat2.y + quat1.z * quat2.z +
            quat1.w * quat2.w)


def lerp_quat(from_quat, to_quat, percent):
    """Return linear interpolation of two quaternions."""

    # Check if signs need to be reversed.
    if dot_quat(from_quat, to_quat) < 0.0:
        to_sign = -1
    else:
        to_sign = 1

    # Simple linear interpolation
    percent_from = 1.0 - percent
    percent_to = percent

    result = Quat(
        percent_from * from_quat.x + to_sign * percent_to * to_quat.x,
        percent_from * from_quat.y + to_sign * percent_to * to_quat.y,
        percent_from * from_quat.z + to_sign * percent_to * to_quat.z,
        percent_from * from_quat.w + to_sign * percent_to * to_quat.w)

    return result


def nlerp_quat(from_quat, to_quat, percent):
    """Return normalized linear interpolation of two quaternions."""

    result = lerp_quat(from_quat, to_quat, percent)
    result.normalize()
    return result


class Quat(object):

    def __init__(self, x=0.0, y=0.0, z=0.0, w=1.0):

        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)

    def make_ident(self):

        self.x = float(0)
        self.y = float(0)
        self.z = float(0)
        self.w = float(1)

    def set(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def is_ident(self):
        return (self.x == 0.0 and self.y == 0.0 and self.z == 0.0 and
                self.w == 1.0)

    def __eq__(self, quat):
        return (self.x == quat.x and self.y == quat.y and self.z == quat.z and
                self.w == quat.w)

    def __str__(self):
        """Return a readable string representation of Quat."""
        return str("Quat(%s,%s,%s,%s)" % (self.x, self.y, self.z, self.w))

    def __repr__(self):
        """Return an unambiguous string representation of Quat."""
        return str("Quat(%s,%s,%s,%s)" % (self.x, self.y, self.z, self.w))

    def __mul__(self, quat1):
        x = (self.w * quat1.x + self.x * quat1.w + self.y * quat1.z - self.z *
             quat1.y)
        y = (self.w * quat1.y - self.x * quat1.z + self.y * quat1.w + self.z *
             quat1.x)
        z = (self.w * quat1.z + self.x * quat1.y - self.y * quat1.x + self.z *
             quat1.w)
        w = (self.w * quat1.w - self.x * quat1.x - self.y * quat1.y - self.z *
             quat1.z)
        return Quat(x, y, z, w)

    def __imul__(self, quat1):
        """Multiply arg m with self (*=) and store the result on self."""

        x = (self.w * quat1.x + self.x * quat1.w + self.y * quat1.z - self.z *
             quat1.y)
        y = (self.w * quat1.y - self.x * quat1.z + self.y * quat1.w + self.z *
             quat1.x)
        z = (self.w * quat1.z + self.x * quat1.y - self.y * quat1.x + self.z *
             quat1.w)
        w = (self.w * quat1.w - self.x * quat1.x - self.y * quat1.y - self.z *
             quat1.z)

        self.x, self.y, self.z, self.w = x, y, z, w

        return self

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z +
                         self.w * self.w)

    def dot(self, quat):
        return (self.x * quat.x + self.y * quat.y + self.z * quat.z +
                self.w * quat.w)

    def normalize(self):
        length = self.length()
        self.x = self.x / length
        self.y = self.y / length
        self.z = self.z / length
        self.w = self.w / length

    def invert(self):
        length = self.length()
        self.x = -self.x / length
        self.y = -self.y / length
        self.z = -self.z / length
        self.w = self.w / length

    def __getitem__(self, index):
        """Return the value at index.
        For example, at index 0, return x.
        Raise IndexError if index is invalid.
        """

        if (index == 0):
            return self.x
        elif (index == 1):
            return self.y
        elif (index == 2):
            return self.z
        elif (index == 3):
            return self.w

        raise IndexError("Quat index out of range %s" % index)

    def rotate_vec(self, vec):
        """
        https://code.google.com/p/kri/wiki/Quaternions
        v + 2.0*cross(q.xyz, cross(q.xyz,v) + q.w*v);
        """
        xyz = Vec3(self.x, self.y, self.z)
        return add_v3(vec, scale_v3(
            xyz.cross(xyz.cross(vec) + scale_v3(vec, self.w)), 2.0))

    def to_euler_rad(self, euler_vec3):
        """Returns euler angles"""

        # TODO: consolidated duplicated code in this function and to_euler_deg()
        sqw = self.w * self.w
        sqx = self.x * self.x
        sqy = self.y * self.y
        sqz = self.z * self.z

        euler_vec3.z = math.atan2(2.0 * (self.x * self.y + self.z * self.w),
                                  (sqx - sqy - sqz + sqw))
        euler_vec3.x = math.atan2(2.0 * (self.y * self.z + self.x * self.w),
                                  (-sqx - sqy + sqz + sqw))
        euler_vec3.y = math.asin(-2.0 * (self.x * self.z - self.y * self.w))
        return euler_vec3

    def to_euler_deg(self, euler_vec3):
        """Returns euler angles"""
        sqw = self.w * self.w
        sqx = self.x * self.x
        sqy = self.y * self.y
        sqz = self.z * self.z

        euler_vec3.z = math.atan2(2.0 * (self.x * self.y + self.z * self.w),
                                  (sqx - sqy - sqz + sqw)
                                  ) * (180.0 / math.pi)
        euler_vec3.x = math.atan2(2.0 * (self.y * self.z + self.x * self.w),
                                  (-sqx - sqy + sqz + sqw)
                                  ) * (180.0 / math.pi)
        euler_vec3.y = math.asin(-2.0 * (self.x * self.z - self.y * self.w)
                                 ) * (180.0 / math.pi)
        return euler_vec3

    @staticmethod
    def from_axis_angle(axis_v3, angle_deg):

        axis_v3 = normalize_v3(axis_v3)

        angle_rad = angle_deg * math.pi / 180.

        quat = Quat(math.sin(angle_rad / 2.0) * axis_v3[0],
                    math.sin(angle_rad / 2.0) * axis_v3[1],
                    math.sin(angle_rad / 2.0) * axis_v3[2],
                    math.cos(angle_rad / 2.0))

        return quat

    def get_rot_matrix(self, matrix=None):

        if not matrix:
            matrix = Matrix44()

        matrix.data[0][0] = 1.0 - 2.0 * self.y * self.y - 2.0 * self.z * self.z
        matrix.data[1][0] = 2.0 * self.x * self.y - 2.0 * self.z * self.w
        matrix.data[2][0] = 2.0 * self.x * self.z + 2.0 * self.y * self.w
        matrix.data[3][0] = 0.0

        matrix.data[0][1] = 2.0 * self.x * self.y + 2.0 * self.z * self.w
        matrix.data[1][1] = 1.0 - 2.0 * self.x * self.x - 2.0 * self.z * self.z
        matrix.data[2][1] = 2.0 * self.y * self.z - 2.0 * self.x * self.w
        matrix.data[3][1] = 0.0

        matrix.data[0][2] = 2.0 * self.x * self.z - 2.0 * self.y * self.w
        matrix.data[1][2] = 2.0 * self.y * self.z + 2.0 * self.x * self.w
        matrix.data[2][2] = 1.0 - 2.0 * self.x * self.x - 2.0 * self.y * self.y
        matrix.data[3][2] = 0.0

        matrix.data[0][3] = 0.0
        matrix.data[1][3] = 0.0
        matrix.data[2][3] = 0.0
        matrix.data[3][3] = 1.0

        return matrix

        # TODO: check row vs col major order
        # row 0
        matrix.data[0][0] = 1 - 2 * self.y ** 2 - 2 * self.z ** 2
        matrix.data[0][1] = 2 * self.x * self.y - 2 * self.w * self.z
        matrix.data[0][2] = 2 * self.x * self.z + 2 * self.w * self.y
        matrix.data[0][3] = 0
        # row 1
        matrix.data[1][0] = 2 * self.x * self.y - 2 * self.w * self.z
        matrix.data[1][1] = 1 - 2 * self.x ** 2 - 2 * self.z ** 2
        matrix.data[1][2] = 2 * self.y * self.z + 2 * self.w * self.x
        matrix.data[1][3] = 0
        # row 2
        matrix.data[2][0] = 2 * self.x * self.z - 2 * self.w * self.y
        matrix.data[2][1] = 2 * self.y * self.z - 2 * self.w * self.x
        matrix.data[2][2] = 1 - 2 * self.x ** 2 - 2 * self.y ** 2
        matrix.data[2][3] = 0
        # row 3
        matrix.data[3][0] = 0
        matrix.data[3][1] = 0
        matrix.data[3][2] = 0
        matrix.data[3][3] = 1
        return matrix

