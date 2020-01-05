import numpy as np

from hardware.controller import Controller


def angle_to_pwm(angle):
    from_interval = [0, np.pi]
    to_interval = [Controller.SERVO_MIN_PULSE_WIDTH, Controller.SERVO_MAX_PULSE_WIDTH]
    return int(np.interp(angle, from_interval, to_interval))
