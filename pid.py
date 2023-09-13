class PIDController:
    def __init__(self, kp, ki, kd, dt=50, setpoint=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.prev_error = 0
        self.integral = 0
        self.dt = dt/1000

    def compute(self, current_value):
        error = self.setpoint - current_value

        P = self.kp * error
        self.integral +=  (error + error * self.dt)
        I = self.ki * self.integral

        delta_error = (error - self.prev_error)
        D = self.kd * delta_error

        output = P + I + D

        self.prev_error = error

        return output
    
    
    def set_setpoint(self, new_setpoint):
        self.prev_error = 0
        self.integral = 0
        self.setpoint = new_setpoint
