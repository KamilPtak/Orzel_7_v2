import logging

class Logger(object):
    def __init__(self):
        self.formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')

    def extendable_logger(self, log_name, file_name, level=logging.INFO):
        handler = logging.FileHandler(file_name)
        handler.setFormatter(self.formatter) 
        specified_logger = logging.getLogger(log_name)
        specified_logger.setLevel(level)
        specified_logger.addHandler(handler)

        return (specified_logger, handler)

    def steering_call(self, data):
        steering_logger = self.extendable_logger('steering_logs', 'steering.txt')
        steering_logger[0].info(str(data))
        self.remove_handler(steering_logger[0], steering_logger[1])

    def acc_call(self, data):
        acc_logger = self.extendable_logger('acc_logs', 'acc.txt')
        acc_logger[0].info(str(data))
        self.remove_handler(acc_logger[0], acc_logger[1])

    def gyro_call(self, data):
        gyro_logger = self.extendable_logger('gyro_logs', 'gyro.txt')
        gyro_logger[0].info(str(data))
        self.remove_handler(gyro_logger[0], gyro_logger[1])

    # def current_call(self, data):
    #     curr_logger = self.extendable_logger('current_logs', 'current.txt')
    #     curr_logger[0].info(str(data))
    #     self.remove_handler(curr_logger[0], curr_logger[1])
    
    def pid_call(self, data):
        pid_logger = self.extendable_logger('Pid', 'pid.txt')
        pid_logger[0].info(str(data))
        self.remove_handler(pid_logger[0], pid_logger[1])
    
    def remove_handler(self, logger, handler):
        logger.removeHandler(handler)