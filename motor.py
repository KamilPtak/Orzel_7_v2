import RPi.GPIO as GPIO
from pid import PIDController
from cyclic_timer import CyclicTimer
from filter import MovingAverageFilter

class Motor:
    def __init__(self, pin1, pin2, enable, encPinA, encPinB, motorId, pwm):
        self.motorId = motorId
        self.pin1 = pin1
        self.pin2 = pin2
        self.enable = enable
            
        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.setup(self.pin2, GPIO.OUT)

        self.filter = MovingAverageFilter(window_size=10)

        #PWM related defines
        self.pwm = pwm
        self.pwm.set_pwm_freq(1000)
        self.pwm.output_enable()
        self._max_duty = 4095

        #Encoder related defines
        self.encPinIdA = encPinA
        self.encPinIdB = encPinB

        GPIO.setup(self.encPinIdA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.encPinIdA,
                              GPIO.RISING, 
                              callback=self._enc_callback)
        GPIO.setup(self.encPinIdB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        self.enc_cpr = 48
        self.pos = 0
        self.old_pos = 0
        self.rpm = 0
        self.period = 0.1

        self.rpm_timer = CyclicTimer(self.period, self._rpm_callback)
        self.rpm_timer.start()

        #PID controler related defines
        self.kp = 0.8
        self.ki = 0.2
        self.kd = 0.015
        self.output = 0
        self.setpoint = 0

        self.pid = PIDController(kp=self.kp, ki=self.ki, kd=self.kd)
        self.pid_timer = CyclicTimer(0.15, self._pid_callback)
        self.pid_timer.start()

    def run(self, control):
        norm_output = self._map_to_range(abs(control))

        if self.setpoint == 0:
            self.pwm.set_pwm(self.enable, 0, 0)
            GPIO.output(self.pin1, GPIO.HIGH)
            GPIO.output(self.pin2, GPIO.HIGH)
        elif self.setpoint > 0:
            self.pwm.set_pwm(self.enable, 0,  norm_output)
            GPIO.output(self.pin1, GPIO.LOW)
            GPIO.output(self.pin2, GPIO.HIGH)
        else:
            self.pwm.set_pwm(self.enable, 0,  norm_output)
            GPIO.output(self.pin1, GPIO.HIGH)
            GPIO.output(self.pin2, GPIO.LOW)

    def rotate(self, dir):
        self.pwm.set_pwm(self.enable, 0, 2000)
        if dir == 'R':
            GPIO.output(self.pin1, GPIO.HIGH)
            GPIO.output(self.pin2, GPIO.LOW)
        else:
            GPIO.output(self.pin1, GPIO.LOW)
            GPIO.output(self.pin2, GPIO.HIGH)

    def stop(self):
        self.pwm.set_pwm(self.enable, 0, self._max_duty)
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.LOW)
    
    def set_setpoint(self, new_setpoint):
        self.setpoint = new_setpoint
        self.pid.set_setpoint(new_setpoint)

    def _map_to_range(self, value, in_min=0, in_max=100, out_min=0, out_max=4095):
        value = max(in_min, min(value, in_max))
        mapped_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
        return int(mapped_value)

    def _enc_callback(self, instance):
        if GPIO.input(self.encPinIdB) == 1:
            self.pos += 1
        else:
            self.pos -= 1

    def _rpm_callback(self):
        rpm = (((self.pos - self.old_pos) / self.period) * 60) / self.enc_cpr / 10
        self.filter.add_sample(rpm)
        self.rpm = self.filter.get_average()
        self.old_pos = self.pos

    def _pid_callback(self):
        self.output = self.pid.compute(self.filter.get_average())
        self.run(self.output)

    def get_log_data__(self):
        return "RPM: " + str(self.rpm) + " CTR: " + str(self.output) + " STP: " + str(self.setpoint)


