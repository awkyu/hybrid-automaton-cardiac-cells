from src.models.HA_PacemakerCell_Model import PacemakerCell
from src.models.HA_Cardiomyocyte_Model import CardiomyocyteCell
from src.models.HA_Path_Model import Path

import numpy as np


class SubsidiaryPacemakerCell:
    def __init__(self, dt, name, bpm=50, bpm_sd=5, d4=0.03, d0=3.34, d2=-0.5, d3=-0.9448, h=0.3, f=0.7, hs=35, hr=0.1,
                 m=1, s=6, j=0, r=0.5, VT_PM=25.05, VMin=-74.65, Vm=70, VR_PM=41.25, Vh=-3, init_cond_vel_PM=10,
                 a_PM=0.01, b_PM=3.5, c_PM=0, decay_const_PM=0.7, ax0=-0.0087, ax1=-0.0236, ax2=-0.0069, ax3=-0.0332,
                 ay0=-0.1909, ay1=-0.0455, ay2=0.0759, ay3=0.0280, az0=-0.1904, az1=-0.0129, az2=6.8265, az3=0.0020,
                 bx=0.7772, by=0.0589, bz=0.2766, VR_CM=30, VT_CM=44.5, Vo=131.1, decay_const_CM=0.7,
                 init_cond_vel_CM=1000, a_CM=0.3, b_CM=62.89, c_CM=10.99):
        self.dt = dt
        self.name = name
        self.type = 'Subsidiary Pacemaker'
        self.cardiomyocyte = CardiomyocyteCell(self.dt, self.name, ax0=ax0, ax1=ax1, ax2=ax2, ax3=ax3, ay0=ay0, ay1=ay1,
                                               ay2=ay2, ay3=ay3, az0=az0, az1=az1, az2=az2, az3=az3, bx=bx, by=by,
                                               bz=bz, VR=VR_CM, VT=VT_CM, Vo=Vo, decay_const=decay_const_CM,
                                               init_cond_vel=init_cond_vel_CM, a=a_CM, b=b_CM, c=c_CM)
        self.pacemaker = PacemakerCell(self.dt, self.name, bpm=bpm, bpm_sd=bpm_sd, d4=d4, d0=d0, d2=d2, d3=d3, h=h, f=f,
                                       hs=hs, hr=hr, m=m, s=s, j=j, r=r, VT=VT_PM, VMin=VMin, Vm=Vm, VR=VR_PM, Vh=Vh,
                                       init_cond_vel=init_cond_vel_PM, a=a_PM, b=b_PM, c=c_PM,
                                       decay_const=decay_const_PM)
        self.path = Path(self.pacemaker, self.cardiomyocyte, 0, self.dt)

    def reset(self):
        self.cardiomyocyte.reset()
        self.pacemaker.reset()
        self.path.reset()

    def get_dict(self):
        dict_PM = self.pacemaker.get_dict()
        dict_CM = self.cardiomyocyte.get_dict()
        dict_CM.update({'VR_CM': dict_CM['VR'], 'VT_CM': dict_CM['VT'], 'decay_const_CM': dict_CM['decay_const'],
                        'init_conduct_vel_CM': dict_CM['init_conduct_vel'], 'c_CM': dict_CM['c'], 'b_CM': dict_CM['b'],
                        'a_CM': dict_CM['a']})
        dict_CM.update(dict_PM)
        dict_CM.update({'VR_PM': dict_CM['VR'], 'VT_PM': dict_CM['VT'], 'decay_const_PM': dict_CM['decay_const'],
                        'init_conduct_vel_PM': dict_CM['init_conduct_vel'], 'c_PM': dict_CM['c'], 'b_PM': dict_CM['b'],
                        'a_PM': dict_CM['a']})
        pop_items = ['VR', 'VT', 'decay_const', 'init_conduct_vel', 'c', 'b', 'a']
        for i in pop_items:
            dict_CM.pop(i)
        return dict_CM

    def set_params(self, dictionary):
        dictionary = dict(dictionary)
        for k in dictionary:
            eval_string = 'self.set_' + k + '(dictionary["' + k + '"])'
            eval(eval_string)

    def get_type(self):
        return self.type

    def get_bpm(self):
        return self.pacemaker.bpm

    def get_bpm_sd(self):
        return self.pacemaker.bpm_sd

    def get_d4(self):
        return self.pacemaker.d4

    def get_d0(self):
        return self.pacemaker.d0

    def get_d2(self):
        return self.pacemaker.d2

    def get_d3(self):
        return self.pacemaker.d3

    def get_h(self):
        return self.pacemaker.h

    def get_f(self):
        return self.pacemaker.f

    def get_hs(self):
        return self.pacemaker.hs

    def get_hr(self):
        return self.pacemaker.hr

    def get_m(self):
        return self.pacemaker.m

    def get_s(self):
        return self.pacemaker.s

    def get_j(self):
        return self.pacemaker.j

    def get_VT_PM(self):
        return self.pacemaker.VT

    def get_VMin(self):
        return self.pacemaker.VMin

    def get_Vm(self):
        return self.pacemaker.Vm

    def get_VR_PM(self):
        return self.pacemaker.VR

    def get_Vh(self):
        return self.pacemaker.Vh

    def get_r(self):
        return self.pacemaker.r

    def get_init_conduct_vel_PM(self):
        return self.pacemaker.init_conduct_vel

    def get_a_PM(self):
        return self.pacemaker.a

    def get_b_PM(self):
        return self.pacemaker.b

    def get_c_PM(self):
        return self.pacemaker.c

    def get_decay_const_PM(self):
        return self.pacemaker.decay_const

    def set_bpm(self, bpm):
        self.pacemaker.bpm = bpm

    def set_bpm_sd(self, bpm_sd):
        self.pacemaker.bpm_sd = bpm_sd

    def set_d4(self, d4):
        self.pacemaker.d4 = d4

    def set_d0(self, d0):
        self.pacemaker.d0 = d0

    def set_d2(self, d2):
        self.pacemaker.d2 = d2

    def set_d3(self, d3):
        self.pacemaker.d3 = d3

    def set_h(self, h):
        self.pacemaker.h = h

    def set_f(self, f):
        self.pacemaker.f = f

    def set_hs(self, hs):
        self.pacemaker.hs = hs

    def set_hr(self, hr):
        self.pacemaker.hr = hr

    def set_m(self, m):
        self.pacemaker.m = m

    def set_s(self, s):
        self.pacemaker.s = s

    def set_j(self, j):
        self.pacemaker.j = j

    def set_VT_PM(self, VT):
        self.pacemaker.VT = VT

    def set_VMin(self, VMin):
        self.pacemaker.VMin = VMin

    def set_Vm(self, Vm):
        self.pacemaker.Vm = Vm

    def set_VR_PM(self, VR):
        self.pacemaker.VR = VR

    def set_Vh(self, Vh):
        self.pacemaker.Vh = Vh

    def set_r(self, r):
        self.pacemaker.r = r

    def set_init_conduct_vel_PM(self, cond_vel):
        self.pacemaker.init_conduct_vel = cond_vel

    def set_a_PM(self, a):
        self.pacemaker.a = a

    def set_b_PM(self, b):
        self.pacemaker.b = b

    def set_c_PM(self, c):
        self.pacemaker.c = c

    def set_decay_const_PM(self, value):
        self.pacemaker.decay_const = value

    def get_ax0(self):
        return self.cardiomyocyte.ax0

    def get_ax1(self):
        return self.cardiomyocyte.ax1

    def get_ax2(self):
        return self.cardiomyocyte.ax2

    def get_ax3(self):
        return self.cardiomyocyte.ax3

    def get_ay0(self):
        return self.cardiomyocyte.ay0

    def get_ay1(self):
        return self.cardiomyocyte.ay1

    def get_ay2(self):
        return self.cardiomyocyte.ay2

    def get_ay3(self):
        return self.cardiomyocyte.ay3

    def get_az0(self):
        return self.cardiomyocyte.az0

    def get_az1(self):
        return self.cardiomyocyte.az1

    def get_az2(self):
        return self.cardiomyocyte.az2

    def get_az3(self):
        return self.cardiomyocyte.az3

    def get_bx(self):
        return self.cardiomyocyte.bx

    def get_by(self):
        return self.cardiomyocyte.by

    def get_bz(self):
        return self.cardiomyocyte.bz

    def get_VR_CM(self):
        return self.cardiomyocyte.VR

    def get_VT_CM(self):
        return self.cardiomyocyte.VT

    def get_Vo(self):
        return self.cardiomyocyte.Vo

    def get_decay_const_CM(self):
        return self.cardiomyocyte.decay_const

    def get_init_conduct_vel_CM(self):
        return self.cardiomyocyte.init_conduct_vel

    def get_a_CM(self):
        return self.cardiomyocyte.a

    def get_b_CM(self):
        return self.cardiomyocyte.b

    def get_c_CM(self):
        return self.cardiomyocyte.c

    def set_t(self, value):
        self.pacemaker.t = value
        self.cardiomyocyte.t = value

    def set_ax0(self, value):
        self.cardiomyocyte.ax0 = value

    def set_ax1(self, value):
        self.cardiomyocyte.ax1 = value

    def set_ax2(self, value):
        self.cardiomyocyte.ax2 = value

    def set_ax3(self, value):
        self.cardiomyocyte.ax3 = value

    def set_ay0(self, value):
        self.cardiomyocyte.ay0 = value

    def set_ay1(self, value):
        self.cardiomyocyte.ay1 = value

    def set_ay2(self, value):
        self.cardiomyocyte.ay2 = value

    def set_ay3(self, value):
        self.cardiomyocyte.ay3 = value

    def set_az0(self, value):
        self.cardiomyocyte.az0 = value

    def set_az1(self, value):
        self.cardiomyocyte.az1 = value

    def set_az2(self, value):
        self.cardiomyocyte.az2 = value

    def set_az3(self, value):
        self.cardiomyocyte.az3 = value

    def set_bx(self, value):
        self.cardiomyocyte.bx = value

    def set_by(self, value):
        self.cardiomyocyte.by = value

    def set_bz(self, value):
        self.cardiomyocyte.bz = value

    def set_VR_CM(self, value):
        self.cardiomyocyte.VR = value

    def set_VT_CM(self, value):
        self.cardiomyocyte.VT = value

    def set_Vo(self, value):
        self.cardiomyocyte.Vo = value

    def set_decay_const_CM(self, value):
        self.cardiomyocyte.decay_const = value

    def set_init_conduct_vel_CM(self, value):
        self.cardiomyocyte.init_conduct_vel = value

    def set_a_CM(self, value):
        self.cardiomyocyte.a = value

    def set_b_CM(self, value):
        self.cardiomyocyte.b = value

    def set_c_CM(self, value):
        self.cardiomyocyte.c = value

    def run_model(self):
        self.pacemaker.run_model()
        self.cardiomyocyte.run_model()
        self.path.update_path()

    def update_ext_voltages(self, key, value):
        self.cardiomyocyte.ext_voltages.update({key: value})

    def get_conduction_vel(self):
        k = 1 / (self.cardiomyocyte.a * np.exp(self.cardiomyocyte.b * self.cardiomyocyte.theta) +
                 (1 - self.cardiomyocyte.a) * np.exp(-1 * self.cardiomyocyte.c * self.cardiomyocyte.theta))
        return k * self.cardiomyocyte.init_conduct_vel

    def get_name(self):
        return self.name

    def get_state(self):
        return self.cardiomyocyte.get_state()

    def get_v(self):
        return self.cardiomyocyte.get_v()

    def get_v_t_ms_ago(self, t):
        return self.get_v_arr()[int(-1 * t / self.dt) - 1]

    def get_state_t_ms_ago(self, t):
        return self.get_state_arr()[int(-1 * t / self.dt) - 1]

    def get_t(self):
        return self.cardiomyocyte.get_t()

    def get_v_arr(self):
        return self.cardiomyocyte.get_v_arr()

    def get_t_arr(self):
        return self.cardiomyocyte.get_t_arr()

    def get_state_arr(self):
        return self.cardiomyocyte.get_state_arr()
