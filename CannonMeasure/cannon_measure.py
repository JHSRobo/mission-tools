from math import sqrt
import cv2
import sys

def sqr(num):
    return num * num


mouse_pos = []
clicked = False

def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    global clicked, mouse_pos
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True
        mouse_pos.append(x)
	mouse_pos.append(y)
        print("{0},{1}".format(x,y))

def get_measurement(cv_image):
    global clicked, mouse_pos
    mouse_pos = []
    cv2.imshow('frame', cv_image)
    cv2.setMouseCallback('frame', click_and_crop)
    clicked = False
    while not clicked:
        k = cv2.waitKey(10)
    clicked = False
    while not clicked:
        k = cv2.waitKey(10)
    cv2.line(cv_image, (mouse_pos[0], mouse_pos[1]), (mouse_pos[2], mouse_pos[3]), (0, 255, 0), 3)
    cv2.imshow('frame', cv_image)
    return sqrt(sqr(mouse_pos[0] - mouse_pos[2]) + sqr(mouse_pos[1] - mouse_pos[3])), cv_image


def measure():
    global clicked
    refrence = 15.06
    IP_ADDRESS = "rtsp://root:jhsrobo@192.168.1.201/axis-media/media.amp"
    #IP_ADDRESS = 0
    done = False

    while not done:
        # load the image/video
        # cap = cv2.VideoCapture(IP_ADDRESS)
        cap = cv2.VideoCapture(IP_ADDRESS)
        ret, cv_image = cap.read()
        # get pixel ratio
        length, cv_image = get_measurement(cv_image)
        ratio = length / refrence

        # get irl distance
        irl_length, cv_throwaway = get_measurement(cv_image)
        cannon_height_tall = irl_length / ratio


        # cannon height of small endcap
        # WAIT FOR CLICK
        clicked = False
        print("Taken")
        while not clicked:
            k = cv2.waitKey()
            if k == 97:
                done = False
                clicked = True
            elif k == 13:
                done = True
                clicked = True
            else:
                print(k)

    done = False
    while not done:
        cap = cv2.VideoCapture(IP_ADDRESS)
        ret, cv_image = cap.read()

        length, cv_image = get_measurement(cv_image)
        ratio = length / refrence

        # get irl distance
        length, cv_throwaway = get_measurement(cv_image)
        cannon_height_short = length / ratio

        # height of bore
        # wait for click
        clicked = False
        print("Taken")
        while not clicked:
            k = cv2.waitKey()
            if k == 97:
                done = False
                clicked = True
                break
            elif k == 13:
                done = True
                clicked = True
                break
            else:
                print(k)

    done = False
    while not done:
        cap = cv2.VideoCapture(IP_ADDRESS)
        ret, cv_image = cap.read()

        length = get_measurement(cv_image)
        ratio = length / refrence

        # get irl distance
        length = get_measurement(cv_image)
        cannon_bore = length / ratio


        # cannon length
        cap = cv2.VideoCapture(IP_ADDRESS)
        ret, cv_image = cap.read()

        length = get_measurement(cv_image)
        ratio = length / cannon_height_tall

        length = get_measurement(cv_image)
        cannon_length = length / ratio

        clicked = False
        print("Taken")
        while not clicked:
           k = cv2.waitKey()
           if k == 97:
                done = False
                clicked = True
                break
           elif k == 13:
                done = True
                clicked = True
                break
           else:
               print(k)


    print("Cannon height of tall endcap = {0}\n".format(cannon_height_tall))
    print("Cannon height of short endcap = {0}\n".format(cannon_height_short))
    print("Cannon bore height = {0}\n".format(cannon_bore))
    print("Cannon length = {0}\n".format(cannon_length))



def volume():
    length = float(input("Length: "))
    r1 = float(input("Actual R1: "))
    r2 = float(input("Actual R2: "))
    r3 = float(input("Actual R3: "))
    compound = input("Composition (iron / bronze): ")
    if compound.lower().strip() == "bronze":
        # bronze
        density = 8030 * 0.000001
    elif compound.lower().strip() == "iron":
        density = 7870 * 0.000001
    cut_cone = (1/3) * 3.14159 * length * (sqr(r3) + (r3 * r1) + sqr(r1))
    cylinder = 3.14159 * sqr(r2) * length
    volume = cut_cone - cylinder
    print("Cannon volume = {0}".format(volume))
    mass = volume * density
    water_displaced = volume * 997 * 0.000001
    water_weight = (mass - water_displaced) * 9.8
    print("Cannon weight = {0}".format(water_weight))


if __name__ == "__main__":
    try:
        measure()
        volume()
    except KeyboardInterrupt:
	sys.exit(1)
    except Exception as e:
        print(e)
