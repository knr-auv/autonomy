import py_trees
import sys
import time

from okonClient import OkonClient
from okonActions import TryDetectNTimes, IsGateFarEnough, CalculateDeltaYaw, RotateDeltaYawAngle, SetDepth, SetVelocity, Wait, Exit

oc = OkonClient(ip="127.0.0.1", port=44210, sync_interval=.05, debug=False)
oc.connect()
time.sleep(1.)


def create_root():
	root = py_trees.composites.Selector("Selector")

	sequence_1 = py_trees.composites.Sequence("Sequence 1")

	try_detection_3_times = TryDetectNTimes(
		name="Try detect gate 3 times", okon=oc.okon, object="gate", n=3)
	check_if_gate_far_enough = IsGateFarEnough(
		name="Check if gate is further than 1.5 m", okon=oc.okon,max_distance=1.5)
	calculate_delta_yaw = CalculateDeltaYaw(
		name="Calculate delta yaw", okon=oc.okon)
	set_depth = SetDepth(
		name="Set Depth to 1.1 m", okon=oc.okon, depth=1.1, delta=0.005)
	rotate_deltaYaw = RotateDeltaYawAngle(
		name="Turn deltaYaw angle", okon=oc.okon, delta=2.)
	set_velocity = SetVelocity(
		name="Set stable velocity of 1 m/s on Z axis", okon=oc.okon, z=1.)

	sequence_1.add_children([
					try_detection_3_times,
					check_if_gate_far_enough,
					calculate_delta_yaw,
					set_depth,
					rotate_deltaYaw,
					set_velocity])

	sequence_2 = py_trees.composites.Sequence("Sequence 2")

	wait_for_2_secs = Wait(
		name="Wait for 2 seconds", okon = oc.okon, secs = 2.)
	stop_okon = SetVelocity(
		name="Stop Okon", okon=oc.okon,z=0.)
	wait_for_a_while = Wait(
		name="Wait for 0.1 seconds", okon = oc.okon, secs = .1)
	exit = Exit(
		name="Exit")

	sequence_2.add_children([
					wait_for_2_secs,
        			stop_okon,
					wait_for_a_while,
        			exit])

	root.add_children([
                    sequence_1,
                    sequence_2])

	return root


##############################################################################
# Main
##############################################################################

def main():
    py_trees.logging.level = py_trees.logging.Level.DEBUG

    root = create_root()

####################
# Execute
####################

    root.setup_with_descendants()
    for i in range(0, 200):
        try:
            print("\n--------- Tick {0} ---------\n".format(i))
            root.tick_once()
            print("\n")
            print(py_trees.display.unicode_tree(root=root, show_status=True))
            print(py_trees.display.unicode_blackboard())
            time.sleep(.1)
        except KeyboardInterrupt:
            break
    print("\n")


if __name__ == '__main__':
    main()