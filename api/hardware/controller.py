"""
 ******************************************************************************
 * File  controller.py
 * Author  Freenove (http://www.freenove.com)
 * Date    2016/11/14
 ******************************************************************************
 * Brief
 *   This is the Class Controller. Used for Control the Shield.
 ******************************************************************************
 * Copyright
 *   Copyright © Freenove (http://www.freenove.com)
 * License
 *   Creative Commons Attribution ShareAlike 3.0
 *   (http://creativecommons.org/licenses/by-sa/3.0/legalcode)
 ******************************************************************************
"""
import time
import smbus
import logging

logger = logging.getLogger(__name__)


class Controller:
    CMD_SERVO1 = 0
    CMD_SERVO2 = 1
    CMD_SERVO3 = 2
    CMD_SERVO4 = 3
    CMD_PWM1 = 4
    CMD_PWM2 = 5
    CMD_DIR1 = 6
    CMD_DIR2 = 7
    CMD_BUZZER = 8
    CMD_IO1 = 9
    CMD_IO2 = 10
    CMD_IO3 = 11
    CMD_SONIC = 12
    SERVO_MAX_PULSE_WIDTH = 2500
    SERVO_MIN_PULSE_WIDTH = 500
    SONIC_MAX_HIGH_BYTE = 50
    DIRECTION_BACKWARD = 0
    DIRECTION_FORWARD = 1

    def __init__(self, address):
        self.address = address
        self.bus = smbus.SMBus(1)
        self.bus.open(1)

    def write(self, cmd, value):
        logger.debug('Writing register {} with value {}'.format(cmd, value))

        try:
            self.bus.write_i2c_block_data(self.address, cmd, [value >> 8, value & 0xff])
            time.sleep(0.001)
            self.bus.write_i2c_block_data(self.address, cmd, [value >> 8, value & 0xff])
            time.sleep(0.001)
            self.bus.write_i2c_block_data(self.address, cmd, [value >> 8, value & 0xff])
            time.sleep(0.001)
        except Exception as e:
            logger.error('Shield write error: {}'.format(str(e)))

    def read(self, cmd):
        logger.debug('Reading register {}', cmd)

        ##################################################################################################
        # Due to the update of SMBus, the communication between Pi and the shield board is not normal.
        # through the following code to improve the success rate of communication.
        # But if there are conditions, the best solution is to update the firmware of the shield board.
        ##################################################################################################
        for i in range(0, 10, 1):
            self.bus.write_i2c_block_data(self.address, cmd, [0])
            a = self.bus.read_i2c_block_data(self.address, cmd, 1)

            self.bus.write_byte(self.address, cmd + 1)
            b = self.bus.read_i2c_block_data(self.address, cmd + 1, 1)

            self.bus.write_byte(self.address, cmd)
            c = self.bus.read_byte_data(self.address, cmd)

            self.bus.write_byte(self.address, cmd + 1)
            d = self.bus.read_byte_data(self.address, cmd + 1)
            # print i,a,b,c,d
            # '''
            if a[0] == c and c < self.SONIC_MAX_HIGH_BYTE:  # and b[0] == d
                return c << 8 | d
            else:
                continue

        return 0
