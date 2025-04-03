from djitellopy import tello
import cv2


class Drone:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)

    def frame(self):
        _, img = self.capture.read()
        return img

    def takeoff(self):
        print('takeoff')

    def land(self):
        print('land')

    def move(self, forward_back_vel, up_down_vel, yaw_vel):
        print(
            f'forward/back: {forward_back_vel} up/down: {up_down_vel} yaw: {yaw_vel}')


class TelloDrone(Drone):
    def __init__(self, run: bool = True):
        super().__init__()
        self.run = run
        self.t = tello.Tello()
        self.t.connect()
        print(f'battery: {self.t.get_battery()}')
        self.t.streamon()

    def frame(self):
        return self.t.get_frame_read().frame

    def takeoff(self):
        if self.run:
            self.t.takeoff()
        else:
            print('takeoff')

    def land(self):
        if self.run:
            self.t.land()
        else:
            print('land')

    def move(self, forward_back_vel, up_down_vel, yaw_vel):
        if self.run:
            self.t.send_rc_control(0, forward_back_vel, up_down_vel, yaw_vel)

        print(f'forward/back: {forward_back_vel} up/down: {up_down_vel} yaw: {yaw_vel}')
