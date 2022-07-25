import py_trees

from okonClient import Okon


class SetDepth(py_trees.behaviour.Behaviour):

    def __init__(self,
                 name: str = "setDepth",
                 okon: Okon = None,
                 depth: float = 0.6,
                 delta: float = .005):
        super().__init__(name)
        self.okon = okon
        self.depth = depth
        self.delta = delta
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))

    def initialise(self):
        self.logger.debug("%s.initialise()" % (self.__class__.__name__))

    def update(self):
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

class Rotate(py_trees.behaviour.Behaviour):

    def __init__(self,
                 name: str = "rotate",
                 okon: Okon = None,
                 add_angle: float = 45.,
                 delta: float = 1.):
        super().__init__(name)
        self.okon = okon
        self.add_angle = add_angle
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
            self.feedback_message = "Current rotation is {0:.3f} degrees. Waiting for target depth of {1:.3f} degrees.".format(
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

