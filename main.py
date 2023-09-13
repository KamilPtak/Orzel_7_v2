from mpu6050 import MPU6050
from logger import Logger
from motor import Motor
from time import sleep
import RPi.GPIO as GPIO
from ServoPi import PWM

import control
import gamepad
import threading
import os

GPIO.setmode(GPIO.BCM)
# os.system("raspi-gpio set 2 a0")
# os.system("raspi-gpio set 3 a0")
os.system("sudo i2cdetect -y 1")
sleep(1)

pwmobject = PWM(0x40, 1)
Motor1 = Motor(pin1=6, pin2=13, enable=16, encPinA=26, encPinB=19, motorId=1, pwm=pwmobject)
Motor2 = Motor(pin1=21, pin2=20, enable=15 ,encPinA=16, encPinB=12, motorId=2, pwm=pwmobject)
Motor3 = Motor(pin1=27, pin2=17, enable=1, encPinA=14, encPinB=15, motorId=3, pwm=pwmobject)
Motor4 = Motor(pin1=23, pin2=24, enable=2,encPinA=8, encPinB=25, motorId=4, pwm=pwmobject)

Control = control.WirelesControl()
Logging = Logger()
Imu = MPU6050()

def logg_data():
    while True:
        Logging.acc_call(Imu.get_data_to_log('accel'))
        # Logging.gyro_call(Imu.get_data_to_log('gyro'))
        # print(Imu.get_data_to_log('gyro'))
        # Logger.pid_call()
        sleep(0.5)
loging_loop = threading.Thread(target=logg_data)
loging_loop.start()

# steer = 0

# def input():
#     global steer
#     while True:
#         steer_tmp = input('Input steer: ')
#         Motor1.set_setpoint(int(steer_tmp))
#         sleep(1)
# input_loop = threading.Thread(target=input)
# input_loop.start()

while True:
    event = gamepad.catch_event()

    if event:
        action_type, pwmsValuesList = Control.calculate_pwm(event)

        # res = Control.calculate_pwm(event)
        # print(res)

        if action_type == 'control':
            Motor1.set_setpoint(pwmsValuesList[0])
            Motor2.set_setpoint(pwmsValuesList[1])
            Motor3.set_setpoint(pwmsValuesList[2])
            Motor4.set_setpoint(pwmsValuesList[3])
        elif action_type == 'rotate right':
            Motor1.rotate('R')
            Motor2.rotate('R')
            Motor3.rotate('R')
            Motor4.rotate('R')
        elif action_type == 'rotate left':
            Motor1.rotate('L')
            Motor2.rotate('L')
            Motor3.rotate('L')
            Motor4.rotate('L')
        elif action_type == 'stop':
            Motor1.stop()
            Motor2.stop()
            Motor3.stop()
            Motor4.stop()
        else:
            pass

        print(pwmsValuesList)
        event.clear()
