import smbus
import time


class WirelesControl(): 
    def __init__(self):
        self.x_axis = 0
        self.y_axis = 0
        self.speed = 50
        self.max_speed = 200
        self.speed_difference = 5
        self.dead_space = range(-5, 5)
        self.motors_pwm = [0, 0, 0, 0] 
        self.knob_mode_enabled = False
        
        self.events_group_knob = ['Axis Left X', 'Axis Left Y',               #control events
                                  'Button RB', 'Button LB']                   # stop events

        self.events_group_arrows = ['Horizontal arrows', 'Vertical arrows',   # control events
                                    'Button RT', 'Button LT',                 # change speed events
                                    'Button RB', 'Button LB']                 # stop events

    def calculate_pwm(self, event) -> list:
        self._calculate_steer(event)

        self.motors_pwm[0] = (self.x_axis + self.y_axis) * self.speed
        self.motors_pwm[1] = (-1 * self.x_axis + self.y_axis) * self.speed
        self.motors_pwm[2] = (-1 * self.x_axis + -1 * self.y_axis) * self.speed
        self.motors_pwm[3] = (self.x_axis + -1 * self.y_axis) * self.speed

        return self.motors_pwm

    def _calculate_steer(self, event) -> None:
        if event['button'] == 'Button select' and event['value'] == 1:
            self.knob_mode_enabled = not self.knob_mode_enabled
            print("Steer control by knob enabled: ", self.knob_mode_enabled)

        if event['button'] in self.events_group_knob and self.knob_mode_enabled:
            self._parse_knob_control(event)
        elif event['button'] in self.events_group_arrows:
            self._parse_arrows_control(event)
        else:
            if event['button'] != 'Button select':
                print("Unknown event: ", event)

    def _parse_knob_control(self, event) -> None:
        if event['button'] == 'Axis Left X':
            event['value'] -= 128
            self.x_axis = 0 if event['value'] in self.dead_space else event['value']/128

        elif event['button'] == 'Axis Left Y':
            event['value'] -= 128
            self.y_axis = 0 if event['value'] in self.dead_space else event['value']/128

        elif event['button'] == 'Button RB' or 'Button LB':
            self.x_axis = 0
            self.y_axis = 0

    def _parse_arrows_control(self, event) -> None:
        if event['button'] == 'Horizontal arrows':
            self.y_axis = 0
            self.x_axis = 0

            if event['value'] == 1:
                self.x_axis = 1
            elif event['value'] == -1:
                self.x_axis = -1

        elif event['button'] == 'Vertical arrows':
            self.x_axis = 0
            self.y_axis = 0

            if event['value'] == 1:
                self.y_axis = 1
            elif event['value'] == -1:
                self.y_axis = -1

        elif event['button'] == 'Button RT' and event['value'] == 255:
            new_speed = self.speed + self.speed_difference
            self.speed = self.max_speed if new_speed >= self.max_speed else new_speed

        elif event['button'] == 'Button LT' and event['value'] == 255:
            new_speed = self.speed - self.speed_difference
            self.speed = 0 if new_speed <= 0 else new_speed

        elif event['button'] == 'Button RB' or 'Button LB':
            self.x_axis = 0
            self.y_axis = 0

class OnboardControl():
    def __init__(self):
        self.bus = smbus.SMBus(0)
        self.master_address = 0x60

        smbus.open(self.bus)

    def close_connection(self) -> None:
        smbus.close() 

    def read_data(self, register) -> None:
        data = smbus.read_block_data(self.master_address,
                                     register,
                                     force=None)
        
        self.calculate_pwm(data)

