################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################


import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class LeapListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def __init__(self):
        Leap.Listener.__init__(self)
        self.values = {'left_hand_tracker' : [0.] * 3,
                       'right_hand_tracker' : [0.] * 3}

    def on_init(self, controller):
        print "Leap Motion initialized"

    def on_connect(self, controller):
        print "Leap Motion connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Leap Motion disconnected"

    def on_exit(self, controller):
        print "Leap Motion exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
        #frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        # end_thumb = frame.hands[0].fingers[0].bone(3).center
        # end_index = frame.hands[0].fingers[1].bone(3).center
        # self.grip_size = end_thumb.distance_to(end_index)

        # self.grip_size = frame.hands[0].grab_strength
        # self.hand_roll = frame.hands[0].direction.roll * Leap.RAD_TO_DEG

        # Get hands
        for hand in frame.hands:

            # handType = "Left hand" if hand.is_left else "Right hand"

            # print "  %s, id %d, position: %s" % (
            #     handType, hand.id, hand.palm_position)

            # print "position: %s" % (hand.palm_position)
            if hand.is_left:
                self.values["left_hand_tracker"] = [hand.palm_position[0], hand.palm_position[1], hand.palm_position[2]]
            elif hand.is_right:
                self.values["right_hand_tracker"] = [hand.palm_position[0], hand.palm_position[1], hand.palm_position[2]]
            #self.hand_coord_norm = hand.palm_normal.to_float_array()


            # Get the hand's normal vector and direction
            #normal = hand.palm_normal
            #direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            # print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
            # direction.pitch * Leap.RAD_TO_DEG,
            # normal.roll * Leap.RAD_TO_DEG,
            # direction.yaw * Leap.RAD_TO_DEG)

            # Get arm bone
            #arm = hand.arm
            # print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
            # arm.direction,
            # arm.wrist_position,
            # arm.elbow_position)

            # Get fingers



                # print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                # self.finger_names[finger.type()],
                # finger.id,
                # finger.length,
                # finger.width)

                # Get bones
                # for b in range(0, 4):
                #     bone = finger.bone(b)
                    # print "      Bone: %s, start: %s, end: %s, direction: %s" % (
                    # self.bone_names[bone.type],
                    # bone.prev_joint,
                    # bone.next_joint,
                    # bone.direction)

        # Get tools
        # for tool in frame.tools:

            # print "  Tool id: %d, position: %s, direction: %s" % (
                # tool.id, tool.tip_position, tool.direction)

        # # Get gestures
        # for gesture in frame.gestures():
        #     if gesture.type == Leap.Gesture.TYPE_CIRCLE:
        #         circle = CircleGesture(gesture)
        #
        #         # Determine clock direction using the angle between the pointable and the circle normal
        #         if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
        #             clockwiseness = "clockwise"
        #         else:
        #             clockwiseness = "counterclockwise"
        #
        #         # Calculate the angle swept since the last frame
        #         swept_angle = 0
        #         if circle.state != Leap.Gesture.STATE_START:
        #             previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
        #             swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI
        #
        #         print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
        #                 gesture.id, self.state_names[gesture.state],
        #                 circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)
        #
        #     if gesture.type == Leap.Gesture.TYPE_SWIPE:
        #         swipe = SwipeGesture(gesture)
        #         print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
        #                 gesture.id, self.state_names[gesture.state],
        #                 swipe.position, swipe.direction, swipe.speed)
        #
        #     if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
        #         keytap = KeyTapGesture(gesture)
        #         print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
        #                 gesture.id, self.state_names[gesture.state],
        #                 keytap.position, keytap.direction )
        #
        #     if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
        #         screentap = ScreenTapGesture(gesture)
        #         print "  Screen Tap id: %d, %s, position: %s, direction: %s" % (
        #                 gesture.id, self.state_names[gesture.state],
        #                 screentap.position, screentap.direction )
        #
        # if not (frame.hands.is_empty and frame.gestures().is_empty):
        #     print ""

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

class LeapTracker(object):
    def __init__(self):
        self.listener = LeapListener()
        self.controller = Leap.Controller()
        self.controller.add_listener(self.listener)

    def get_position(self, tracked_object):
        return self.listener.values[tracked_object]

def main():
    # Create a sample listener and controller
    listener = LeapListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
