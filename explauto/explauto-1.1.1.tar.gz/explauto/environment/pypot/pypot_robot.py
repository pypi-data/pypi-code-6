import time
import numpy

from ..environment import Environment
from ...utils import bounds_min_max


class PypotEnvironment(Environment):
    """ Environment based on dynamixel based robot using pypot.

        This environment can be used to link explauto with pypot, a library allowing to control robot based on dynamixel motors. It uses an optitrack has the sensor. This could easily be changed by defining other pypot environments.

    """
    use_process = False

    def __init__(self,
                 pypot_robot, motors, move_duration,
                 tracker, tracked_obj,
                 m_mins, m_maxs, s_mins, s_maxs):
        """ :param pypot_robot: robot used as the environment
            :type pypot_robot: :class:`~pypot.robot.robot.Robot`
            :param motors: list of motors used by the environment
            :type motors: list of :class:`~pypot.dynamixel.motor.DxlMotor`
            :param float move_duration: duration (in sec.) of each primitive motion
            :param tracker: tracker used as the sensor by the :class:`~explauto.agent.agent.Agent`
            :type tracker: :class:`~explauto.utils.tracker.Tracker`
            :param string tracked_obj: name of the object tracked by the optitrack
            :param numpy.array m_mins: minimum motor dims
            :param numpy.array m_maxs: maximum motor dims
            :param numpy.array s_mins: minimum sensor dims
            :param numpy.array s_maxs: maximum sensor dims

        """
        Environment.__init__(self, m_mins, m_maxs, s_mins, s_maxs)



        self.readable = range(self.conf.ndims)

        self.robot = pypot_robot
        self.motors = [m.name for m in motors]
        self.move_duration = move_duration

        self.tracker = tracker
        self.tracked_obj = tracked_obj
        self.robot.start_sync()

    def compute_motor_command(self, m_ag):
        """ Compute the motor command by restricting it to the bounds. """
        m_env = bounds_min_max(m_ag, self.conf.m_mins, self.conf.m_maxs)
        return m_env

    def compute_sensori_effect(self, m_env):
        """ Make the robot moves and retrieve the tracked object position. """
        cmd = numpy.rad2deg(m_env)
        pos = dict(zip(self.motors, cmd))
        self.robot.goto_position(pos, self.move_duration, wait=True)
        time.sleep(0.5)

        return self.tracker.get_position(self.tracked_obj)


from numpy import deg2rad, array

# motor bounds for the left arm
l_m_mins = deg2rad(array([-15, 0, -90, -90]))
l_m_maxs = deg2rad(array([90, 90, 90, 0]))

# motor bounds for the right arm
r_m_mins = deg2rad(array([-15, -90, -90, -90]))
r_m_maxs = deg2rad(array([90, 0, 90, 0]))

# sensor bounds for the left arm
l_s_mins = array((-0.2, -0.1, 0.0))
l_s_maxs = array((0.4, 0.5, 0.6))

# sensor bounds for the right arm
r_s_mins = array((-0.2, -0.5, 0.0))
r_s_maxs = array((0.4, 0.1, 0.6))

class VrepTracker(object):
    def get_position(self, tracked_object):
        return getattr(poppy, tracked_object).position

tracker = VrepTracker()

import json

def get_poppy_vrep():
    from pypot.vrep import from_vrep

    config_path = 'poppy_config.json'
    scene_path = 'poppy-sitting.ttt'
    with open(config_path) as cf:
        config = json.load(cf)
    poppy = from_vrep(config, '127.0.0.1', 19997, scene_path,
                      tracked_objects=['left_hand_tracker', 'right_hand_tracker'])
    return poppy

def get_poppy():
    import pypot.robot
    import os
    print os.getcwd()
    config_path = '../../poppy-software/poppytools/configuration/poppy_config.json'
    poppy = pypot.robot.from_json(config_path)
    return poppy

def get_configuration(get_robot, tracker_cls, tracked_obj,
                      m_mins=l_m_mins, m_maxs=l_m_maxs,
                      s_mins=l_s_mins, s_maxs=l_s_maxs):
    pass
    
poppy = get_poppy()

conf = {'pypot_robot': poppy,
        'motors': poppy.l_arm,
        'move_duration': 1.0,
        'tracker': tracker,
        'tracked_obj': 'left_hand_tracker',
        'm_mins': l_m_mins,
        'm_maxs': l_m_maxs,
        's_mins': l_s_mins,
        's_maxs': l_s_maxs}

configurations = {'left_arm': conf, 'default':conf}

environment = PypotEnvironment

testcases = None
