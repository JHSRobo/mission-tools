import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
from std_msgs.msg import Header
from pynput import mouse
from math import sqrt
from cannon_measure.srv import cannon_measure

def sqr(num: int):
    return num * num

def get_measurement(cv_image):
        cv2.rectangle(cv_image, (110, 400), (510, 100), (255, 255, 255), 3)
        cv2.imshow('frame', cv_image)

        mouse_pos = {}
        clicked = False
        while not clicked:
            def on_click(x, y, button, pressed):
                mouse_pos['inital_x'] = x
                mouse_pos['inital_y'] = y
                clicked = True

            listener = mouse.Listener(on_click=on_click)
            listener.start()

        clicked = False
        while not clicked:
            def on_click(x, y, button, pressed):
                mouse_pos['secondary_x'] = x
                mouse_pos['secondary_y'] = y
                clicked = True

            listener = mouse.Listener(on_click=on_click)
            listener.start()
        return sqrt(sqr(mouse_pos['inital_x'] - mouse_pos['secondary_x']) + sqr(mouse_pos['inital_x'] - mouse_pos['secondary_x']))


def measure():
    refrence = 15.06
    msg = cannon_measure()

    header = Header()

    # update message headers
    header.stamp = rospy.Time.now()
    header.frame_id = 'humidity_data'
    msg.header = header

    # cannon height of large endcap
    try:
        data = rospy.wait_for_message("/rov/image_raw", Image, timeout=5)
    except rospy.ROSException:
        return None
    else:
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(data.data, desired_encoding="passthrough")

        # get pixel ratio
        length = get_measurement(cv_image)
        ratio = length / refrence

        # get irl distance
        length = get_measurement(cv_image)
        msg.canon_height_tall = length / ratio

    # cannon height of small endcap
    # WAIT FOR CLICK
    clicked = False
    while not clicked:
        def on_click(x, y, button, pressed):
            clicked = True

        listener = mouse.Listener(on_click=on_click)
        listener.start()

    try:
        data = rospy.wait_for_message("/rov/image_raw", Image, timeout=5)
    except rospy.ROSException:
        return None
    else:
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(data.data, desired_encoding="passthrough")

        length = get_measurement(cv_image)
        ratio = length / refrence

        # get irl distance
        length = get_measurement(cv_image)
        msg.canon_height_short = length / ratio

    # height of bore
    clicked = False
    while not clicked:
        def on_click(x, y, button, pressed):
            clicked = True

        listener = mouse.Listener(on_click=on_click)
        listener.start()

    try:
        data = rospy.wait_for_message("/rov/image_raw", Image, timeout=5)
    except rospy.ROSException:
        return None
    else:
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(data.data, desired_encoding="passthrough")

        length = get_measurement(cv_image)
        ratio = length / refrence

        # get irl distance
        length = get_measurement(cv_image)
        msg.canon_bore = length / ratio


    # cannon length
    try:
        data = rospy.wait_for_message("/rov/image_raw", Image, timeout=5)
    except rospy.ROSException:
        return None
    else:
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(data.data, desired_encoding="passthrough")

        length = get_measurement(cv_image)
        ratio = length / msg.cannon_height_tall

        length = get_measurement(cv_image)
        msg.canon_length = length / ratio


def listener():
    rospy.init_node("measure")
    rospy.Service('start_cannon_measure', cannon_measure, measure)
    rospy.spin()

if __name__ == "__main__":
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
