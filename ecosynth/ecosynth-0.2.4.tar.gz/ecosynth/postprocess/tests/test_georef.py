import unittest
from ecosynth.postprocess import transforms
import numpy as np
from numpy import testing

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Here's our "unit tests".
class HelmertTransformTests(unittest.TestCase):

    def setUp(self):
        pass

    def testOne(self):
        zero_array = np.zeros(401)
        forward_array = np.arange(-200, 201)
        backward_array = -forward_array

        cam_array = np.column_stack((forward_array, forward_array, forward_array))
        gps_array = np.column_stack((backward_array, backward_array, backward_array))

        #cam_array = np.column_stack((forward_array, zero_array, zero_array))
        #gps_array = np.column_stack((backward_array, zero_array, zero_array))

        initial_guess = [1, 1, 1, 1, 1, 1, 1]

        sol = transforms._solve_helmert(initial_guess, gps_array, cam_array)

        print sol.parameters

        #testing.assert_approx_equal(sol.parameters[0], )  # Omega
        #testing.assert_approx_equal(sol.parameters[1], np.pi)  # Phi
        #testing.assert_approx_equal(sol.parameters[2], )  # Kappa
        testing.assert_approx_equal(sol.parameters[3], 1)  # Scale
        testing.assert_almost_equal(sol.parameters[4], 0)  # Tx
        testing.assert_almost_equal(sol.parameters[5], 0)  # Ty
        testing.assert_almost_equal(sol.parameters[6], 0)  # Tz

        trans_cam_array = transforms.apply_helmert(sol.parameters, cam_array)

        testing.assert_array_almost_equal(trans_cam_array, gps_array)


def plot3Darray(array):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(array[:, 0], array[:, 1], array[:, 2], zdir='z', c='red')
    ax.axis("equal")
    ax.set_xlabel('X Dim')
    ax.set_ylabel('Y Dim')
    ax.set_zlabel('Z Dim')

    plt.show()


def plot2Darray(array):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(array[:, 0], array[:, 1], c='red')
    ax.axis("equal")
    ax.set_xlabel('X Dim')
    ax.set_ylabel('Y Dim')

    plt.show()


def main():
    unittest.main()

if __name__ == '__main__':
    main()
