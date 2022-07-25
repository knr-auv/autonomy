import py_trees
import time

from okonClient import OkonClient
from okonActions import Rotate, SetDepth

oc = OkonClient(ip="127.0.0.1", port=44210, sync_interval=.05, debug=False)
oc.connect()
time.sleep(1.)

def main():
    py_trees.logging.level = py_trees.logging.Level.DEBUG

    set_depth_action = SetDepth(okon=oc.okon, depth=0.5, delta=0.005)
    rotate_action = Rotate(okon=oc.okon, add_angle=-45., delta=1.)


    try:
        for _ in range(0, 10):
            set_depth_action.tick_once()
            time.sleep(0.3)
        for _ in range(0, 9):
            rotate_action.tick_once()
            time.sleep(0.1)
        set_depth_action.update_depth(new_depth=0.8)
        for _ in range(0, 10):
            set_depth_action.tick_once()
            time.sleep(0.3)
        rotate_action.update_add_angle(new_add_angle=45)
        for _ in range(0, 9):
            rotate_action.tick_once()
            time.sleep(0.1)
        set_depth_action.update_depth(new_depth=0.2)
        for _ in range(0, 10):
            set_depth_action.tick_once()
            time.sleep(0.3)
        print("\n")
    except KeyboardInterrupt:
        print("")
        pass

if __name__ == '__main__':
    main()