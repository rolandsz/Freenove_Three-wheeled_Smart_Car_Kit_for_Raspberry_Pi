"""
 ******************************************************************************
 * File  shield.py
 * Author  Freenove (http://www.freenove.com)
 * Date    2016/11/14
 ******************************************************************************
 * Brief
 *   This is the Class Shield. Used for Control the Shield.
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

from threading import Lock


class Shield:
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
    Is_IO1_State_True = False
    Is_IO2_State_True = False
    Is_IO3_State_True = False
    Is_Buzzer_State_True = False
    handle = True
    mutex = Lock()

    def __init__(self, address=0x18):
        self.address = address
        self.bus = smbus.SMBus(1)
        self.bus.open(1)

    def write(self, cmd, value):
        if not isinstance(value, int):
            value = int(value)

        try:
            self.bus.write_i2c_block_data(self.address, cmd, [value >> 8, value & 0xff])
            time.sleep(0.001)
            self.bus.write_i2c_block_data(self.address, cmd, [value >> 8, value & 0xff])
            time.sleep(0.001)
            self.bus.write_i2c_block_data(self.address, cmd, [value >> 8, value & 0xff])
            time.sleep(0.001)
        except Exception as e:
            print(Exception, "Shield write error :", e)

    def read(self, cmd):
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
