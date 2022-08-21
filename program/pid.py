class Pid:
    def __init__(self, p, i, d):
        self.p = p
        self.i = i
        self.d = d
        self.sum = 0
        self.last_error = 0

    def pid(self, process_variable, set_point):
        error = set_point - process_variable 
        p_val = error * self.p
        dev = self.last_error - error
        d_val = dev * self.d
        self.last_error = error
        self.sum += error
        i_val = self.sum * self.i
        correction = p_val + d_val + i_val
        return round(correction)

