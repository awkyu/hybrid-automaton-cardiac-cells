import numpy as np


class CardiomyocyteCell:
    def __init__(self, dt, name, ax0=-0.0087, ax1=-0.0236, ax2=-0.0069, ax3=-0.0332, ay0=-0.1909, ay1=-0.0455,
                 ay2=0.0759, ay3=0.0280, az0=-0.1904, az1=-0.0129, az2=6.8265, az3=0.0020, bx=0.7772, by=0.0589,
                 bz=0.2766, VR=30, VT=44.5, Vo=131.1, decay_const=0.7, init_cond_vel=1000, a=0.3, b=62.89, c=10.99):
        self.dt = dt
        self.name = name
        self.type = 'Cardiomyocyte'
        self.model_state = 'q4'  # Initialized to q0 in original model:
        #                           q0 is Resting&FR (q4/q3 in PacemakerCell),
        #                           q1 is Stimulated (N/A in PacemakerCell),
        #                           q2 is Upstroke (q0),
        #                           q3 is plateau&ER (q2)
        self.t = 0
        self.v = 0

        self.ax0 = ax0  # Default Constants from the Stony Brook Cardiac Cell Model
        self.ax1 = ax1
        self.ax2 = ax2
        self.ax3 = ax3
        self.ay0 = ay0
        self.ay1 = ay1
        self.ay2 = ay2
        self.ay3 = ay3
        self.az0 = az0
        self.az1 = az1
        self.az2 = az2
        self.az3 = az3
        self.bx = bx
        self.by = by
        self.bz = bz

        self.VR = VR
        self.VT = VT
        self.Vo = Vo

        self.vx = 0
        self.vy = 0
        self.vz = 0

        self.decay_const = decay_const  # this equals Gamma_ik * sigma_ik / (A_m * C_m): TODO: Modify empirical values
        # Gamma_ik is the cross-sectional area (units of mm2) from
        # cell i to k, sigma_ik is the electrical conductivity (units of mS/mm)
        # from cell i to k, Am is cell k’s surface area to volume (units of
        # mm−2), Cm is cell k’s specific membrane capacitance (units
        # of µF/mm2)

        self.init_conduct_vel = init_cond_vel  # in mm/s
        self.a = a
        self.b = b
        self.c = c
        self.theta = 0
        self.v_arr = []
        self.t_arr = []
        self.state_arr = []
        self.ext_voltages = {}  # Dictionary of connected cells and voltages from them

    def reset(self):
        self.theta = 0
        self.v_arr = []
        self.t_arr = []
        self.state_arr = []
        self.ext_voltages = {}  # Dictionary of connected cells and voltages from them
        self.model_state = 'q4'
        self.t = 0
        self.v = 0
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def set_params(self, dictionary):
        dictionary = dict(dictionary)
        for k in dictionary:
            eval_string = 'self.set_' + k + '(dictionary["' + k + '"])'
            eval(eval_string)

    def get_dict(self):
        dictionary = {}
        dictionary.update({'ax0': self.get_ax0(), 'ax1': self.get_ax1(), 'ax2': self.get_ax2(), 'ax3': self.get_ax3(),
                           'ay0': self.get_ay0(), 'ay1': self.get_ay1(), 'ay2': self.get_ay2(), 'ay3': self.get_ay3(),
                           'az0': self.get_az0(), 'az1': self.get_az1(), 'az2': self.get_az2(), 'az3': self.get_az3(),
                           'bx': self.get_bx(), 'by': self.get_by(), 'bz': self.get_bz(), 'VR': self.get_VR(),
                           'VT': self.get_VT(), 'Vo': self.get_Vo(), 'decay_const': self.get_decay_const(),
                           'init_conduct_vel': self.get_init_conduct_vel(), 'a': self.get_a(), 'b': self.get_a(),
                           'c': self.get_c()})
        return dictionary

    def get_type(self):
        return self.type

    def get_ax0(self):
        return self.ax0

    def get_ax1(self):
        return self.ax1

    def get_ax2(self):
        return self.ax2

    def get_ax3(self):
        return self.ax3

    def get_ay0(self):
        return self.ay0

    def get_ay1(self):
        return self.ay1

    def get_ay2(self):
        return self.ay2

    def get_ay3(self):
        return self.ay3

    def get_az0(self):
        return self.az0

    def get_az1(self):
        return self.az1

    def get_az2(self):
        return self.az2

    def get_az3(self):
        return self.az3

    def get_bx(self):
        return self.bx

    def get_by(self):
        return self.by

    def get_bz(self):
        return self.bz

    def get_VR(self):
        return self.VR

    def get_VT(self):
        return self.VT

    def get_Vo(self):
        return self.Vo

    def get_decay_const(self):
        return self.decay_const

    def get_init_conduct_vel(self):
        return self.init_conduct_vel

    def get_a(self):
        return self.a

    def get_b(self):
        return self.b

    def get_c(self):
        return self.c

    def set_t(self, value):
        self.t = value

    def set_ax0(self, value):
        self.ax0 = value

    def set_ax1(self, value):
        self.ax1 = value

    def set_ax2(self, value):
        self.ax2 = value

    def set_ax3(self, value):
        self.ax3 = value

    def set_ay0(self, value):
        self.ay0 = value

    def set_ay1(self, value):
        self.ay1 = value

    def set_ay2(self, value):
        self.ay2 = value

    def set_ay3(self, value):
        self.ay3 = value

    def set_az0(self, value):
        self.az0 = value

    def set_az1(self, value):
        self.az1 = value

    def set_az2(self, value):
        self.az2 = value

    def set_az3(self, value):
        self.az3 = value

    def set_bx(self, value):
        self.bx = value

    def set_by(self, value):
        self.by = value

    def set_bz(self, value):
        self.bz = value

    def set_VR(self, value):
        self.VR = value

    def set_VT(self, value):
        self.VT = value

    def set_Vo(self, value):
        self.Vo = value

    def set_decay_const(self, value):
        self.decay_const = value

    def set_init_conduct_vel(self, value):
        self.init_conduct_vel = value

    def set_a(self, value):
        self.a = value

    def set_b(self, value):
        self.b = value

    def set_c(self, value):
        self.c = value

    def run_model(self):
        eval('self.' + self.model_state + '()')
        self.v_arr.append(self.get_v())
        self.t_arr.append(self.get_t())
        self.state_arr.append(self.get_state())
        self.t += self.dt

    def update_ext_voltages(self, key, value):
        self.ext_voltages.update({key: value})

    def get_conduction_vel(self):
        k = 1 / (self.a * np.exp(self.b * self.theta) + (1 - self.a) * np.exp(-1 * self.c * self.theta))
        return k * self.init_conduct_vel

    def get_name(self):
        return self.name

    def get_state(self):
        return self.model_state

    def get_v(self):
        return self.v

    def get_v_t_ms_ago(self, t):
        return self.get_v_arr()[int(-1 * t / self.dt) - 1]

    def get_state_t_ms_ago(self, t):
        return self.get_state_arr()[int(-1 * t / self.dt) - 1]

    def get_t(self):
        return self.t

    def get_v_arr(self):
        return self.v_arr

    def get_t_arr(self):
        return self.t_arr

    def get_state_arr(self):
        return self.state_arr

    def get_ext_voltages(self):
        total_voltage = 0
        for i in self.ext_voltages.values():
            total_voltage += self.decay_const * (i - self.v)
        return total_voltage

    def q4(self):
        vx_dot = self.ax0 * self.vx
        vy_dot = self.ay0 * self.vy
        vz_dot = self.az0 * self.vz
        self.vx += vx_dot * self.dt
        self.vy += vy_dot * self.dt
        self.vz += vz_dot * self.dt
        self.v = self.vx - self.vy + self.vz
        if self.get_ext_voltages() > self.VT:
            self.model_state = 'q1'
            self.theta = self.v / self.VR

    def q1(self):
        ext_v = self.get_ext_voltages()
        vx_dot = self.ax1 * self.vx + self.bx * ext_v
        vy_dot = self.ay1 * self.vy + self.by * ext_v
        vz_dot = self.az1 * self.vz + self.bz * ext_v
        self.vx += vx_dot * self.dt
        self.vy += vy_dot * self.dt
        self.vz += vz_dot * self.dt
        self.v = self.vx - self.vy + self.vz
        if ext_v <= 0 and self.v < self.VT:
            self.model_state = 'q4'
        elif self.v >= self.VT:
            self.model_state = 'q0'

    def q0(self):
        vx_dot = self.ax2 * self.vx
        vy_dot = self.ay2 * self.vy
        vz_dot = self.az2 * self.vz
        self.vx += vx_dot * self.dt
        self.vy += vy_dot * self.dt
        self.vz += vz_dot * self.dt
        self.v = self.vx - self.vy + self.vz
        if self.v >= self.Vo - 80.1 * np.sqrt(self.theta):
            self.model_state = 'q2'

    def q2(self):
        def f(theta):
            if theta < 0.04:
                return 0.29 * np.exp(62.89 * theta) + 0.70 * np.exp(-10.99 * theta)
            else:
                return 4.0395

        vx_dot = self.ax3 * self.vx * f(self.theta)
        vy_dot = self.ay3 * self.vy * f(self.theta)
        vz_dot = self.az3 * self.vz
        self.vx += vx_dot * self.dt
        self.vy += vy_dot * self.dt
        self.vz += vz_dot * self.dt
        self.v = self.vx - self.vy + self.vz
        if self.v <= self.VR:
            self.model_state = 'q4'
