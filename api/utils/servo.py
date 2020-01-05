import numpy as np

from hardware.controller import Controller


def angle_to_pwm(angle):
    from_interval = [0, np.pi]
    to_interval = [Controller.SERVO_MIN_PULSE_WIDTH, Controller.SERVO_MAX_PULSE_WIDTH]
    return int(np.interp(angle, from_interval, to_interval))


def clip_horizontal_angle(angle):
    return np.clip(angle, np.deg2rad(0), np.deg2rad(180))


def clip_vertical_angle(angle):
    return np.clip(angle, np.deg2rad(90), np.deg2rad(180))
