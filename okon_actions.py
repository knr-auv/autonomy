""" Module with implementation of OKON actions using py_trees

"""
import math
import sys
import time

import py_trees

from okon_client import Okon


class SetDepth(py_trees.behaviour.Behaviour):

    def __init__(self,
                 name: str = "set depth",
                 okon: Okon = None,
                 depth: float = 0.6,
                 delta: float = .05):
        super().__init__(name)
        self.okon = okon
        self.depth = depth
        self.delta = delta
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))

    def initialise(self):
        self.logger.debug("%s.initialise()" % (self.__class__.__name__))

    def update(self) -> py_trees.common.Status:
        self.okon.set_depth(self.depth)
        new_status = py_trees.common.Status.SUCCESS if self.okon.reachedTargetDepth(
            self.delta) else py_trees.common.Status.RUNNING
        if new_status == py_trees.common.Status.SUCCESS:
            self.feedback_message = "Target depth of {0} m reached.".format(
                self.depth)
        else:
            self.feedback_message = "Current depth {0:.3f}. Waiting for target depth of {1} m.".format(
                self.okon.sens["baro"] / 1000 / 9.81, self.depth)
        self.logger.debug(
            "%s.update()[%s->%s][%s]" % (
                self.__class__.__name__,
                self.status, new_status,
                self.feedback_message
            )
        )
        return new_status

    def update_depth(self, new_depth):
        self.depth = new_depth

    def terminate(self, new_status):
        """Nothing to clean up in this example."""
        self.logger.debug(
            "%s.terminate()[%s->%s]" % (self.__class__.__name__, self.status, new_status))


class SetVelocity(py_trees.behaviour.Behaviour):

    def __init__(self,
                 name: str = "set velocity",
                 okon: Okon = None,
                 x: float = 0.,
                 y: float = 0.,
                 z: float = 0.):
        super().__init__(name)
        self.okon = okon
        self.x = x
        self.y = y
        self.z = z
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))

    def initialise(self):
        self.logger.debug("%s.initialise()" % (self.__class__.__name__))

    def update(self):
        self.okon.set_stable_vel(x=self.x, y=self.y, z=self.z)
        new_status = py_trees.common.Status.SUCCESS
        if new_status == py_trees.common.Status.SUCCESS:
            self.feedback_message = "Speed set as: Vx = {0:.3f} Vy = {1:.3f} Vz = {2:.3f}.".format(
                self.x, self.y, self.z)
        self.logger.debug(
            "%s.update()[%s->%s][%s]" % (
                self.__class__.__name__,
                self.status, new_status,
                self.feedback_message
            )
        )
        return new_status

    def terminate(self, new_status):
        """Nothing to clean up in this example."""
        self.logger.debug(
            "%s.terminate()[%s->%s]" % (self.__class__.__name__, self.status, new_status))


class Rotate(py_trees.behaviour.Behaviour):

    def __init__(self,
                 name: str = "rotate",
                 okon: Okon = None,
                 add_angle: float = 45.,
                 delta: float = 1.):
        super().__init__(name)
        self.okon = okon
        self.add_angle = add_angle
        self.target_angle = self.okon.sens['imu']['rot']['y'] + self.add_angle
        self.delta = delta
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))

    def initialise(self):
        self.target_angle = self.okon.sens['imu']['rot']['y'] + self.add_angle
        if self.target_angle < 0.:
            self.target_angle += 360.
        self.logger.debug("%s.initialise()" % (self.__class__.__name__))

    def update(self):
        self.okon.set_stable_rot(y=self.target_angle)
        new_status = py_trees.common.Status.SUCCESS if self.okon.reachedTargetRotation(
            self.delta) else py_trees.common.Status.RUNNING
        if new_status == py_trees.common.Status.SUCCESS:
            self.feedback_message = "Target rotation of {0} degrees reached.".format(
                self.target_angle)
        else:
            self.feedback_message = "Current rotation is {0:.3f} degrees. Waiting for target rotation of {1:.3f} degrees.".format(
                self.okon.sens['imu']['rot']['y'], self.target_angle)
        self.logger.debug(
            "%s.update()[%s->%s][%s]" % (
                self.__class__.__name__,
                self.status, new_status,
                self.feedback_message
            )
        )
        return new_status

    def update_add_angle(self, new_add_angle):
        self.add_angle = new_add_angle

    def terminate(self, new_status):
        """Nothing to clean up in this example."""
        self.logger.debug(
            "%s.terminate()[%s->%s]" % (self.__class__.__name__, self.status, new_status))


class RotateDeltaYawAngle(py_trees.behaviour.Behaviour):

    def __init__(self,
                 name: str = "rotate delta yaw angle",
                 okon: Okon = None,
                 delta: float = 1.):
        super().__init__(name)
        self.okon = okon
        self.delta = delta
        self.blackboard = self.attach_blackboard_client()
        self.blackboard.register_key(
            key="deltaYaw", access=py_trees.common.Access.READ)
        self.target_angle = self.okon.sens['imu']['rot']['y'] + \
            self.blackboard.deltaYaw
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))

    def initialise(self):
        self.target_angle = self.okon.sens['imu']['rot']['y'] + \
            self.blackboard.deltaYaw
        if self.target_angle < 0.:
            self.target_angle += 360.
        self.logger.debug("%s.initialise()" % (self.__class__.__name__))

    def update(self):
        self.okon.set_stable_rot(y=self.target_angle)
        new_status = py_trees.common.Status.SUCCESS if self.okon.reachedTargetRotation(
            self.delta) else py_trees.common.Status.RUNNING
        if new_status == py_trees.common.Status.SUCCESS:
            self.feedback_message = "Target rotation of {0} degrees reached.".format(
                self.target_angle)
        else:
            self.feedback_message = "Current rotation is {0:.3f} degrees. Waiting for target rotation of {1:.3f} degrees.".format(
                self.okon.sens['imu']['rot']['y'], self.target_angle)
        self.logger.debug(
            "%s.update()[%s->%s][%s]" % (
                self.__class__.__name__,
                self.status, new_status,
                self.feedback_message
            )
        )
        return new_status

    def terminate(self, new_status):
        """Nothing to clean up in this example."""
        self.logger.debug(
            "%s.terminate()[%s->%s]" % (self.__class__.__name__, self.status, new_status))


class TryDetectNTimes(py_trees.behaviour.Behaviour):

    def __init__(self,
                 name: str = "try detect n times",
                 okon: Okon = None,
                 object: str = "gate",
                 n: int = 3):
        super().__init__(name)
        self.okon = okon
        self.object = object
        self.n = n
        self.counter = 1
        self.blackboard = self.attach_blackboard_client()
        self.blackboard.register_key(
            key="detection", access=py_trees.common.Access.WRITE)
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))

    def initialise(self):
        self.counter = 1
        self.logger.debug("%s.initialise()" % (self.__class__.__name__))

    def update(self):
        detection = self.okon.get_detection(self.object)
        if len(detection) > 0:
            new_status = py_trees.common.Status.SUCCESS
            self.blackboard.detection = detection
        elif self.counter == self.n:
            new_status = py_trees.common.Status.FAILURE
        else:
            new_status = py_trees.common.Status.RUNNING

        if new_status == py_trees.common.Status.SUCCESS:
            self.feedback_message = "Object {0} detected in attempt number {1}".format(
                self.object, self.counter)
        else:
            self.feedback_message = "Object {0} undetected in attempt number {1}".format(
                self.object, self.counter)

        self.counter += 1

        self.logger.debug(
            "%s.update()[%s->%s][%s]" % (
                self.__class__.__name__,
                self.status, new_status,
                self.feedback_message
            )
        )
        return new_status

    def terminate(self, new_status):
        """Nothing to clean up in this example."""
        self.logger.debug(
            "%s.terminate()[%s->%s]" % (self.__class__.__name__, self.status, new_status))


class CalculateDeltaYaw(py_trees.behaviour.Behaviour):

    def __init__(self,
                 name: str = "calculate delta yaw",
                 okon: Okon = None):
        super().__init__(name)
        self.okon = okon
        self.blackboard = self.attach_blackboard_client()
        self.blackboard.register_key(
            key="detection", access=py_trees.common.Access.READ)
        self.blackboard.register_key(
            key="deltaYaw", access=py_trees.common.Access.WRITE)
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))

    def initialise(self):
        self.logger.debug("%s.initialise()" % (self.__class__.__name__))

    def update(self):
        detection = self.blackboard.detection
        if len(detection) > 0:
            new_status = py_trees.common.Status.SUCCESS
            hfov = 60
            gate = detection[0]
            if gate['distance'] < 1:
                self.deltaYaw = 0
            else:
                center = (gate['max']['x'] + gate['min']['x'])/2 * 2 - 1
                cameraPlaneX = 1./math.tan(hfov/2/180*math.pi)
                self.deltaYaw = math.atan(center/cameraPlaneX)/math.pi*180
            self.blackboard.deltaYaw = self.deltaYaw
        else:
            new_status = py_trees.common.Status.FAILURE

        if new_status == py_trees.common.Status.SUCCESS:
            self.feedback_message = "Delta Yaw was calculated and is equal to {0}".format(
                self.deltaYaw)
        else:
            self.feedback_message = "There were no objects in the detection parameter in blackboard."

        self.logger.debug(
            "%s.update()[%s->%s][%s]" % (
                self.__class__.__name__,
                self.status, new_status,
                self.feedback_message
            )
        )
        return new_status

    def terminate(self, new_status):
        """Nothing to clean up in this example."""
        self.logger.debug(
            "%s.terminate()[%s->%s]" % (self.__class__.__name__, self.status, new_status))


class IsGateFarEnough(py_trees.behaviour.Behaviour):

    def __init__(self,
                 name: str = "calculate delta yaw",
                 okon: Okon = None,
                 max_distance: float = 1.5):
        super().__init__(name)
        self.okon = okon
        self.max_distance = max_distance
        self.blackboard = self.attach_blackboard_client()
        self.blackboard.register_key(
            key="detection", access=py_trees.common.Access.READ)
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))

    def initialise(self):
        self.logger.debug("%s.initialise()" % (self.__class__.__name__))

    def update(self):
        gate = self.blackboard.detection[0]
        new_status = py_trees.common.Status.SUCCESS if gate['distance'] > self.max_distance else py_trees.common.Status.FAILURE

        if new_status == py_trees.common.Status.SUCCESS:
            self.feedback_message = "Gate is in distance of {0:.3f} m".format(
                gate['distance'])
        else:
            self.feedback_message = "Gate is closer than max distance set to {0:.3f}m.".format(
                self.max_distance)

        self.logger.debug(
            "%s.update()[%s->%s][%s]" % (
                self.__class__.__name__,
                self.status, new_status,
                self.feedback_message
            )
        )
        return new_status

    def terminate(self, new_status):
        """Nothing to clean up in this example."""
        self.logger.debug(
            "%s.terminate()[%s->%s]" % (self.__class__.__name__, self.status, new_status))


class Wait(py_trees.behaviour.Behaviour):

    def __init__(self,
                 name: str = "wait",
                 okon: Okon = None,
                 secs: float = 0.):
        super().__init__(name)
        self.okon = okon
        self.secs = secs
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))

    def initialise(self):
        self.logger.debug("%s.initialise()" % (self.__class__.__name__))

    def update(self):
        time.sleep(self.secs)
        new_status = py_trees.common.Status.SUCCESS
        if new_status == py_trees.common.Status.SUCCESS:
            self.feedback_message = "Robot waited for {0} secunds.".format(
                self.secs)
        self.logger.debug(
            "%s.update()[%s->%s][%s]" % (
                self.__class__.__name__,
                self.status, new_status,
                self.feedback_message
            )
        )
        return new_status

    def terminate(self, new_status):
        """Nothing to clean up in this example."""
        self.logger.debug(
            "%s.terminate()[%s->%s]" % (self.__class__.__name__, self.status, new_status))


class Exit(py_trees.behaviour.Behaviour):

    def __init__(self,
                 name: str = "exit"):
        super().__init__(name)
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))

    def initialise(self):
        self.logger.debug("%s.initialise()" % (self.__class__.__name__))

    def update(self):
        sys.exit()
