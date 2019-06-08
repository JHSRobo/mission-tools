import cv2
from pynput import mouse
from math import sqrt

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
    IP_ADDRESS = "rtsp://root:jhsrobo@192.168.1.201/axis-media/media.amp"

    # load the image/video
    #cap = cv2.VideoCapture(IP_ADDRESS)
    cap = cv2.VideoCapture(IP_ADDRESS)
    ret, cv_image = cap.read()
    # get pixel ratio
    length = get_measurement(cv_image)
    ratio = length / refrence

    # get irl distance
    length = get_measurement(cv_image)
    canon_height_tall = length / ratio

    # cannon height of small endcap
    # WAIT FOR CLICK
    clicked = False
    while not clicked:
        def on_click(x, y, button, pressed):
            clicked = True

        listener = mouse.Listener(on_click=on_click)
        listener.start()

    cap = cv2.VideoCapture(IP_ADDRESS)
    ret, cv_image = cap.read()

    length = get_measurement(cv_image)
    ratio = length / refrence

    # get irl distance
    length = get_measurement(cv_image)
    canon_height_short = length / ratio

    # height of bore
    clicked = False
    while not clicked:  # wait for click
        def on_click(x, y, button, pressed):
            clicked = True

        listener = mouse.Listener(on_click=on_click)
        listener.start()

    cap = cv2.VideoCapture(IP_ADDRESS)
    ret, cv_image = cap.read()

    length = get_measurement(cv_image)
    ratio = length / refrence

    # get irl distance
    length = get_measurement(cv_image)
    canon_bore = length / ratio


    # cannon length
    cap = cv2.VideoCapture(IP_ADDRESS)
    ret, cv_image = cap.read()

    length = get_measurement(cv_image)
    ratio = length / cannon_height_tall

    length = get_measurement(cv_image)
    canon_length = length / ratio

    print("Cannon height of tall endcap = {0}".format(cannon_height_tall))
    print("Cannon height of short endcap = {0}".format(cannon_height_short))
    print("Cannon bore height = {0}".format(cannon_bore))
    print("Cannon length = {0}".format(cannon_length))


if __name__ == "__main__":
    try:
        measure()
    except Exception as e:
        print(e)
