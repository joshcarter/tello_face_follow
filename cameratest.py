import cv2
from averager import *
from tracker import *
# from pid import *
# import numpy as np

w, h = 640, 400
forward_back_range = [6200, 6800]

# yaw_pid = PID(0.4, 0.4, 0, -100, 100)
# forward_back_pid = PID(0.5, 0.5, 0, -25, 25)

yaw_tracker = Tracker(Range(0, w), Range(w // 2 - 25, w // 2 + 25), Range(-50, 50))
forward_back_tracker = Tracker(Range(10000, 40000), Range(23000, 27000), Range(-20, 20), invert=True)
up_down_tracker = Tracker(Range(0, h), Range(h // 2 - 25, h // 2 + 25), Range(-20, 20))

avgsamples = 5
avgx = SlidingWindowAverager(avgsamples)
avgy = SlidingWindowAverager(avgsamples)
avgw = SlidingWindowAverager(avgsamples)
avgh = SlidingWindowAverager(avgsamples)


def find_face(img):
    classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # is this necessary?
    faces = classifier.detectMultiScale(img2, 1.2, 8)
    centers = []
    areas = []

    for (x, y, w, h) in faces:
        x = avgx.avg(x)
        y = avgy.avg(y)
        w = avgw.avg(w)
        h = avgh.avg(h)

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        center_x = x + w // 2
        center_y = y + h // 2
        area = w * h
        cv2.circle(img, (center_x, center_y), 5, (0, 0, 255), cv2.FILLED)
        centers.append([center_x, center_y])
        areas.append(area)

    if len(areas) > 0:
        i = areas.index(max(areas))
        return img, [centers[i], areas[i]]
    else:
        return img, [[0, 0], 0]


def track_face(info, w):
    x, y = info[0]
    area = info[1]
    yaw_vel = 0
    forward_back_vel = 0
    up_down_vel = 0

    if area > 0:
        # yaw_vel = yaw_pid.update(x - w // 2)
        # print(f'yaw {yaw_tracker} value {x}')
        # forward_back_vel = forward_back_pid.update((25000 - area) // 10)
        yaw_vel = yaw_tracker.update(x)
        up_down_vel = up_down_tracker.update(y)
        forward_back_vel = forward_back_tracker.update(area)

    # foward_back_vel = 0
    # if area > forward_back_range[1]:
    #     foward_back_vel = -20
    # elif area < forward_back_range[0] and area != 0:
    #     foward_back_vel = 20

    print(f'forward/back: {forward_back_vel} up/down: {up_down_vel} yaw: {yaw_vel}')


def run():
    global perr

    cap = cv2.VideoCapture(0)

    while True:
        _, img = cap.read()
        img = cv2.resize(img, (w, h))
        img, info = find_face(img)
        track_face(info, w)
        print(f'area: {info[1]}')
        cv2.imshow("Output", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            return
