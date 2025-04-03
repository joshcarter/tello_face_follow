# import tello
# import cameratest
from drone import *
from averager import *
from tracker import *

drone = TelloDrone(run=True)
w, h = 640, 360

yaw_tracker = Tracker(Range(0, w), Range(w // 2 - 50, w // 2 + 50),
                      Range(-50, 50))
forward_back_tracker = Tracker(Range(1000, 25000), Range(6000, 9000),
                               Range(-25, 25), invert=True)
up_down_tracker = Tracker(Range(0, h), Range(h // 2 - 50, h // 2 + 20),
                          Range(-75, 75), invert=True)

avgsamples = 5
avgx = SlidingWindowAverager(avgsamples)
avgy = SlidingWindowAverager(avgsamples)
avgw = SlidingWindowAverager(avgsamples)
avgh = SlidingWindowAverager(avgsamples)


def find_face(img):
    classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    # img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # is this necessary?
    faces = classifier.detectMultiScale(img, 1.2, 8)
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


def track_face(info, drone: Drone):
    x, y = info[0]
    area = info[1]
    yaw_vel = 0
    forward_back_vel = 0
    up_down_vel = 0

    if area > 0:
        yaw_vel = yaw_tracker.update(x)
        up_down_vel = up_down_tracker.update(y)
        forward_back_vel = forward_back_tracker.update(area)

    drone.move(forward_back_vel, up_down_vel, yaw_vel)


def main():
    drone.takeoff()

    while True:
        img = drone.frame()
        img = cv2.resize(img, (w, h))
        img, info = find_face(img)
        track_face(info, drone)
        print(f'area: {info[1]}')
        cv2.imshow("Output", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.land()
            cv2.destroyAllWindows()
            return


if __name__ == '__main__':
    main()
