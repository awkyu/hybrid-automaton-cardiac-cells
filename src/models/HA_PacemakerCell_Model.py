import numpy as np
import random

"""
Citations:
[1] https://ieeexplore-ieee-org.prox.lib.ncsu.edu/document/7906495
[2] https://ieeexplore-ieee-org.prox.lib.ncsu.edu/document/1186732
"""


class PacemakerCell:
    def __init__(self, dt, name, bpm=70, bpm_sd=5, d4=0.03, d0=3.34, d2=-0.5, d3=-0.9448, h=0.3, f=0.7, hs=35, hr=0.1,
                 m=1, s=6, j=0, r=0.5, VT=25.05, VMin=-74.65, Vm=70, VR=41.25, Vh=-3, init_cond_vel=10, a=0.01, b=3.5,
                 c=0, decay_const=1):
        self.name = name
        self.t = 0
        self.dt = dt
        self.type = 'Nodal Pacemaker'
        self.bpm = bpm
        self.bpm_sd = bpm_sd
        self.model_state = 'q4'  # states rotate between q4, q0, q2, and q3
        self.theta = 0
        self.theta_k = self.theta
        self.d4 = d4  # TODO: change constant?
        self.d0 = d0  # TODO: change constant?
        self.d2 = d2  # TODO: change constant?
        self.d3 = d3  # TODO: change constant?
        self.h = h
        self.f = f
        self.hs = hs
        self.hr = hr
        self.n = 0
        self.m = m
        self.s = s
        self.j = j
        self.v = 0  # voltage
        self.VT = VT  # voltage threshold to start AP
        self.VMin = VMin  # MDP: Maximum Diastolic Potential
        self.Vm = Vm  # Arbitrary
        self.VMax = self.Vm
        self.VR = VR
        self.Vh = Vh
        self.r = r  # Recovery rate constant. If r=1, the cell can recover after the first spontaneous beat.
        #               When r=0, the cell cannot recover to the baseline rate.
        self.i = 0  # counter for beats
        self.init_conduct_vel = init_cond_vel  # in mm/s
        self.a = a
        self.b = b
        self.c = c
        self.decay_const = decay_const  # TODO: Arbitrary right now
        self.beat_arr = [0]
        self.v_arr = []
        self.t_arr = []
        self.state_arr = []
        self.ext_voltages = {}  # Dictionary of connected cells and voltages from them

    def reset(self):
        self.beat_arr = [0]
        self.v_arr = []
        self.t_arr = []
        self.state_arr = []
        self.ext_voltages = {}  # Dictionary of connected cells and voltages from them
        self.t = 0
        self.v = 0  # voltage
        self.i = 0  # counter for beats
        self.n = 0
        self.model_state = 'q4'  # states rotate between q4, q0, q2, and q3
        self.theta = 0
        self.theta_k = self.theta

    def set_params(self, dictionary):
        dictionary = dict(dictionary)
        for k in dictionary:
            eval_string = 'self.set_' + k + '(dictionary["' + k + '"])'
            eval(eval_string)

    def get_dict(self):
        dictionary = {}
        dictionary.update({'bpm': self.get_bpm(), "bpm_sd": self.get_bpm_sd(), 'd4': self.get_d4(),
                           'd0': self.get_d0(), 'd2': self.get_d2(), 'd4': self.get_d3(),
                           'h': self.get_h(), 'f': self.get_f(), 'hr': self.get_hr(),
                           'hs': self.get_hs(), 'm': self.get_m(), 's': self.get_s(),
                           'j': self.get_j(), 'VT': self.get_VT(), 'VMin': self.get_VMin(),
                           'Vm': self.get_Vm(), 'VR': self.get_VR(), 'Vh': self.get_Vh(),
                           'r': self.get_r(), 'init_conduct_vel': self.get_init_conduct_vel(), 'a': self.get_a(),
                           'b': self.get_b(), 'c': self.get_c(), 'decay_const': self.get_decay_const()})
        return dictionary

    def get_type(self):
        return self.type

    def get_bpm(self):
        return self.bpm

    def get_bpm_sd(self):
        return self.bpm_sd

    def get_d4(self):
        return self.d4

    def get_d0(self):
        return self.d0

    def get_d2(self):
        return self.d2

    def get_d3(self):
        return self.d3

    def get_h(self):
        return self.h

    def get_f(self):
        return self.f

    def get_hs(self):
        return self.hs

    def get_hr(self):
        return self.hr

    def get_m(self):
        return self.m

    def get_s(self):
        return self.s

    def get_j(self):
        return self.j

    def get_VT(self):
        return self.VT

    def get_VMin(self):
        return self.VMin

    def get_Vm(self):
        return self.Vm

    def get_VR(self):
        return self.VR

    def get_Vh(self):
        return self.Vh

    def get_r(self):
        return self.r

    def get_init_conduct_vel(self):
        return self.init_conduct_vel

    def get_a(self):
        return self.a

    def get_b(self):
        return self.b

    def get_c(self):
        return self.c

    def get_decay_const(self):
        return self.decay_const

    def set_t(self, t):
        self.t = t

    def set_bpm(self, bpm):
        self.bpm = bpm

    def set_bpm_sd(self, bpm_sd):
        self.bpm_sd = bpm_sd

    def set_d4(self, d4):
        self.d4 = d4

    def set_d0(self, d0):
        self.d0 = d0

    def set_d2(self, d2):
        self.d2 = d2

    def set_d3(self, d3):
        self.d3 = d3

    def set_h(self, h):
        self.h = h

    def set_f(self, f):
        self.f = f

    def set_hs(self, hs):
        self.hs = hs

    def set_hr(self, hr):
        self.hr = hr

    def set_m(self, m):
        self.m = m

    def set_s(self, s):
        self.s = s

    def set_j(self, j):
        self.j = j

    def set_VT(self, VT):
        self.VT = VT

    def set_VMin(self, VMin):
        self.VMin = VMin

    def set_Vm(self, Vm):
        self.Vm = Vm

    def set_VR(self, VR):
        self.VR = VR

    def set_Vh(self, Vh):
        self.Vh = Vh

    def set_r(self, r):
        self.r = r

    def set_init_conduct_vel(self, cond_vel):
        self.init_conduct_vel = cond_vel

    def set_a(self, a):
        self.a = a

    def set_b(self, b):
        self.b = b

    def set_c(self, c):
        self.c = c

    def set_decay_const(self, decay_const):
        self.decay_const = decay_const

    def update_ext_voltages(self, key, value):
        self.ext_voltages.update({key: value})

    def get_conduction_vel(self):
        k = 1/(self.a*np.exp(self.b*self.theta) + (1-self.a)*np.exp(-1*self.c*self.theta))
        return k*self.init_conduct_vel

    def get_name(self):
        return self.name

    def get_state(self):
        return self.model_state

    def get_v(self):
        return self.v

    def get_v_t_ms_ago(self, t):
        return self.get_v_arr()[int(-1*t/self.dt)-1]

    def get_state_t_ms_ago(self, t):
        return self.get_state_arr()[int(-1*t/self.dt)-1]

    def get_t(self):
        return self.t

    def get_v_arr(self):
        return self.v_arr

    def get_t_arr(self):
        return self.t_arr

    def get_state_arr(self):
        return self.state_arr

    def run_model(self):
        eval('self.' + self.model_state + '()')
        self.v_arr.append(self.get_v())
        self.t_arr.append(self.get_t())
        self.state_arr.append(self.get_state())
        self.t += self.dt

    def q4(self):
        v_dot = self.d4 * self.f3(self.theta)
        self.v += v_dot * self.dt
        if self.v >= self.VT:
            self.theta = 0
            self.VMax = self.Vm
            self.n = self.n - self.r * self.n
            self.VMin = self.Vh * self.wn(self.n) * self.f4(self.theta_k)
            self.model_state = 'q0'
        elif sum([self.decay_const*i-self.get_v() for i in self.ext_voltages.values()]) > self.VT > self.v:
            print('Stimulated')
            self.theta = (self.v - self.VT) / (self.VMin - self.VT)
            self.VMax = self.Vm * self.f1(self.theta)
            self.n += 1
            if self.n > (5/self.hr + self.hs):
                self.n = 5/self.hr + self.hs
            self.VMin = self.Vh * self.wn(self.n) * self.f4(self.theta)

    def q0(self):
        v_dot = self.d0 * self.f2(self.theta)
        self.v += v_dot * self.dt
        if self.v >= self.VMax:
            self.model_state = 'q2'

    def q2(self):
        v_dot = self.d2 * self.f2(self.theta)
        self.v += v_dot * self.dt
        if self.v <= self.VR:
            self.model_state = 'q3'

    def q3(self):
        def chi(i, N=100, LF_left=0.04, HF_right=0.4, bcl0=self.bpm/60*1000, SD=self.bpm_sd/60*1000):
            def bcl_power(f, f1=0.1, f2=0.25, c1=0.01, c2=0.01, hflf_ratio=0.5):  # default values from [2]
                # hf/lf ratio is sigma1^2/sigma2^2 ratio
                sig1_2 = 0.13**2
                sig2_2 = sig1_2 / hflf_ratio
                return (sig1_2 / np.sqrt(2 * np.pi * (c1 ** 2))) * np.exp(-1*((f - f1) ** 2) / (2 * (c1 ** 2))) \
                       + (sig2_2 / np.sqrt(2 * np.pi * (c2 ** 2))) * np.exp(-1*((f - f2) ** 2) / (2 * (c2 ** 2)))

            bcl = 0
            fi = np.linspace(LF_left, HF_right, N)
            for ii in range(N):
                bcl += np.sqrt(bcl_power(fi[ii]))*np.cos(2*np.pi*fi[ii]*self.beat_arr[i] + 2*np.pi*random.random())
            bcl = bcl0 + SD*bcl
            C = (self.VMax - self.VR) / abs(self.d2) + (self.VR - self.VMin) / abs(self.d3) \
                + (self.VMax - self.VT) / self.d0
            return (self.VT - self.VMin) / (bcl - C)

        v_dot = self.d3 * self.f2(self.theta)
        self.v += v_dot * self.dt
        if self.v <= self.VMin:
            self.model_state = 'q4'
            self.i = self.i + 1
            self.beat_arr.append(self.t)
            self.d4 = chi(self.i)
            while self.d4 < 0:
                self.d4 = chi(self.i)

    def f1(self, theta):
        return np.exp(-1 * self.h * theta)

    def f2(self, theta):
        return np.exp(-1 * self.f * theta)

    def wn(self, n):
        if n < 1:
            return 0
        elif 1 <= n <= (5 / self.hr + self.hs):
            return 1 / (1 + np.exp(-1 * self.hr * (n - self.hs)))
        elif n > 5 / self.hr + self.hs:
            return 1 / (1 + np.exp(-5))

    def f3(self, theta):
        return 1 / (self.wn(self.n) * self.m * (theta ** self.s) + 1)

    def f4(self, theta):
        return np.exp(self.j * (theta - 1))
