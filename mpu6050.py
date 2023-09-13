from smbus import SMBus

class MPU6050:
    def __init__(self) -> None:
        self.PWR_MGMT_1   = 0x6B
        self.SMPLRT_DIV   = 0x19
        self.CONFIG       = 0x1A
        self.GYRO_CONFIG  = 0x1B
        self.INT_ENABLE   = 0x38

        self.ACCEL_REG_ADDR_TABLE = [0x3B, 0x3D, 0x3F]
        self.GYRO_REG_ADDR_TABLE = [0x43, 0x45, 0x47]

        self.accel_list = []
        self.gyro_list = []

        self.bus = SMBus(1)
        self.device_address = 0x68
        self.initial_config()

    def initial_config(self):
        self.bus.write_byte_data(self.device_address, self.SMPLRT_DIV, 7)   #Write to sample rate register    
        self.bus.write_byte_data(self.device_address, self.PWR_MGMT_1, 1)   #Write to power management register
        self.bus.write_byte_data(self.device_address, self.CONFIG, 0)       #Write to Configuration register
        self.bus.write_byte_data(self.device_address, self.GYRO_CONFIG, 24) #Write to Gyro configuration register
        self.bus.write_byte_data(self.device_address, self.INT_ENABLE, 1)   #Write to interrupt enable register

    def read_data(self, sensor_type):
        scale_gyro = lambda value: value/131.0
        scale_accel = lambda value: value/16384.0

        if sensor_type == 'accel':
            self.accel_list = []
            for register_addres in self.ACCEL_REG_ADDR_TABLE:
                value = self.read_raw_value(register_addres)
                self.accel_list.append(scale_accel(value))
            return {"AccX":self.accel_list[0], "AccY":self.accel_list[1], "AccZ":self.accel_list[2]}
        elif sensor_type == 'gyro':
            self.gyro_list = []
            for register_addres in self.GYRO_REG_ADDR_TABLE:
                value = self.read_raw_value(register_addres)
                self.gyro_list.append(scale_gyro(value))
            return {"GyrX":self.gyro_list[0], "GyrY":self.gyro_list[1], "GyrZ":self.gyro_list[2]}
        else:
             print("Wrong sensor type")

    def read_raw_value(self, register_addres):
        high = self.bus.read_byte_data(self.device_address, register_addres)
        low = self.bus.read_byte_data(self.device_address, register_addres+1)
        
        value = ((high << 8) | low)
        if(value > 32768):
            value = value - 65536
        return value
    
    def get_data_to_log(self, sensor_type):
        self.update_data()
        if sensor_type == 'accel':
            return "AccX:" + str(self.accel_list[0]) + " AccY:" + str(self.accel_list[1]) + " AccZ:" + str(self.accel_list[2])
        elif sensor_type == 'gyro':
            return "GyrX: " + str(self.gyro_list[0]) + " GyrY: " + str(self.gyro_list[1]) + " GyrZ: " + str(self.gyro_list[2])
        else:
            print("Wrong sensor type")

    def update_data(self):
        self.read_data('accel')
        self.read_data('gyro')
