import evdev
import time

def find_device(device_name):
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if device.name == device_name:
            print(f'Found game controler: {device.name}. \n')
            return device.path

def catch_event():
    time.sleep(0.1)
    try:
        device_event = {}
        for event in device.read():
            if event.type == evdev.ecodes.EV_KEY and event.value:
                if('BTN_X' in evdev.ecodes.BTN[event.code]):
                    device_event = {'button':'Button X',
                                    'value': event.value}
                elif('BTN_B' in evdev.ecodes.BTN[event.code]):
                    device_event = {'button':'Button B',
                                    'value': event.value}
                elif('BTN_Y' in evdev.ecodes.BTN[event.code]):
                    device_event = {'button':'Button Y',
                                    'value': event.value}
                elif('BTN_A' in evdev.ecodes.BTN[event.code]):
                    device_event = {'button':'Button A',
                                    'value': event.value}

                elif('BTN_TR' == evdev.ecodes.BTN[event.code]):
                    device_event = {'button':'Button RB',
                                    'value': event.value}
                elif('BTN_TL' == evdev.ecodes.BTN[event.code]):
                    device_event = {'button':'Button LB',
                                    'value': event.value}

                elif('BTN_START' == evdev.ecodes.BTN[event.code]):
                    device_event = {'button':'Button start',
                                    'value': event.value}
                elif('BTN_SELECT' == evdev.ecodes.BTN[event.code]):
                    device_event = {'button':'Button select',
                                    'value': event.value}

                elif('BTN_THUMBR' == evdev.ecodes.BTN[event.code]):
                    device_event = {'button':'Button RPB',
                                    'value': event.value}
                elif('BTN_THUMBL' == evdev.ecodes.BTN[event.code]):
                    device_event = {'button':'Button LPB',
                                    'value': event.value}

            if event.type == evdev.ecodes.EV_ABS:
                if('ABS_GAS' == evdev.ecodes.ABS[event.code]):
                    device_event = {'button':'Button RT',
                                    'value': event.value}
                elif('ABS_BRAKE' == evdev.ecodes.ABS[event.code]):
                    device_event = {'button':'Button LT',
                                    'value': event.value}

                elif('ABS_X' == evdev.ecodes.ABS[event.code]):
                    device_event = {'button':'Axis Left X',
                                    'value': event.value}
                elif('ABS_Y' == evdev.ecodes.ABS[event.code]):
                    device_event = {'button':'Axis Left Y',
                                    'value': event.value}

                elif('ABS_Z' == evdev.ecodes.ABS[event.code]):
                    device_event = {'button':'Axis Right X',
                                    'value': event.value}
                elif('ABS_RZ' == evdev.ecodes.ABS[event.code]):
                    device_event = {'button':'Axis Right Y',
                                    'value': event.value}

                elif('ABS_HAT0X' == evdev.ecodes.ABS[event.code]):
                    device_event = {'button':'Horizontal arrows',
                                    'value': event.value}
                elif('ABS_HAT0Y' == evdev.ecodes.ABS[event.code]):
                    device_event = {'button':'Vertical arrows',
                                    'value': event.value}
        return device_event

    except Exception as e:
        pass

device_name = "shanwan Android GamePad"
device = evdev.InputDevice(find_device(device_name))
print(device)