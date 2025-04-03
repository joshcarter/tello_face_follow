import time

from djitellopy import tello
import cv2.cv2 as cv2
import numpy as np

w, h = 360, 240
forward_back_range = [6200, 6800]
pid = [0.4, 0.4, 0]
perr = 0
run = False


def find_face(img):
    classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = classifier.detectMultiScale(img2, 1.2, 8)
    centers = []
    areas = []

    for (x, y, w, h) in faces:
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


def track_face(t: tello.Tello, info, w, pid, perr):
    x, y = info[0]
    area = info[1]

    err = x - w // 2
    speed = pid[0] * err + pid[1] * (err - perr)
    speed = int(np.clip(speed, -100, 100))

    fb = 0
    if area > forward_back_range[1]:
        fb = -20
    elif area < forward_back_range[0] and area != 0:
        fb = 20

    if area == 0:
        speed = 0
        err = 0

    if run:
        t.send_rc_control(0, fb, 0, speed)
    else:
        print(f'fb: {fb} speed: {speed}')

    return err


def test_capture():
    global perr
    t = start_tello()

    if run:
        t.takeoff()
        t.send_rc_control(0, 0, 25, 0)
        time.sleep(2.2)
        t.send_rc_control(0, 0, 0, 0)

    while True:
        img = t.get_frame_read().frame
        img = cv2.resize(img, (w, h))
        img, info = find_face(img)
        perr = track_face(t, info, w, pid, perr)
        # print(f'area: {info[1]}')
        cv2.imshow("Output", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            if run:
                t.land()
            cv2.destroyAllWindows()
            return


def start_tello():
    t = tello.Tello()
    t.connect()
    print(f'battery: {t.get_battery()}')
    t.streamon()
    return t