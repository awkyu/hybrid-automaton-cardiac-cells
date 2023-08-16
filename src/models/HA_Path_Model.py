from src.models.HA_PacemakerCell_Model import PacemakerCell
from src.models.HA_Cardiomyocyte_Model import CardiomyocyteCell


class Path:
    def __init__(self, cell1, cell2, l, dt):
        self.cell_i = cell1
        self.cell_j = cell2
        self.cell_i.update_ext_voltages(self.cell_j.get_name(), 0)
        self.cell_j.update_ext_voltages(self.cell_i.get_name(), 0)
        self.l = l
        self.path_state = 'idle'
        self.ti = 0
        self.tj = 0
        self.tij = 0
        self.tji = 0
        self.delta_ij = self.l / self.cell_i.get_conduction_vel()
        self.delta_ji = self.l / self.cell_j.get_conduction_vel()
        self.last = 0
        self.starti = False
        self.startj = False
        self.dt = dt
        self.t = 0

    def reset(self):
        self.t = 0
        self.path_state = 'idle'
        self.ti = 0
        self.tj = 0
        self.tij = 0
        self.tji = 0
        self.cell_i.update_ext_voltages(self.cell_j.get_name(), 0)
        self.cell_j.update_ext_voltages(self.cell_i.get_name(), 0)

    def update_l(self, new_l):
        self.l = new_l
        self.delta_ij = self.l / self.cell_i.get_conduction_vel()
        self.delta_ji = self.l / self.cell_j.get_conduction_vel()

    def update_path(self):
        eval('self.' + self.path_state + '()')
        self.t += self.dt

    def idle(self):
        if self.cell_i.get_state() == 'q0' or self.cell_j.get_state() == 'q0':
            self.path_state = 'ready'

    def ready(self):
        if self.cell_i.get_state() == 'q2':
            self.path_state = 'celli'
            self.ti = 0
        elif self.cell_j.get_state() == 'q2':
            self.path_state = 'cellj'
            self.tj = 0

    def celli(self):
        ti_dot = 1
        if self.ti >= self.delta_ij:
            self.last = 'i'
            self.starti = True
            self.path_state = 'relayi'
        elif (self.last != 'i' or self.cell_i.get_state_t_ms_ago(self.delta_ij) != 'q2') and (self.cell_j.get_state() == 'q2'):
            self.path_state = 'cellij'
            self.tij = 0
        elif self.last == 'j' and self.cell_j.get_state_t_ms_ago(self.delta_ji) == 'q2':
            self.path_state = 'anni'
        self.ti += ti_dot * self.dt

    def relayi(self):
        vout_i = self.cell_i.get_v_t_ms_ago(self.delta_ij)
        self.cell_j.update_ext_voltages(self.cell_i.get_name(), vout_i)
        if type(self.cell_i) is PacemakerCell:
            if self.cell_i.get_state() == 'q3' or self.cell_j.get_state() == 'q2':
                self.cell_j.update_ext_voltages(self.cell_i.get_name(), 0)
                self.path_state = 'idle'
                self.starti = False
        elif type(self.cell_i) is CardiomyocyteCell:
            if self.cell_i.get_state() == 'q4' or self.cell_j.get_state() == 'q2':
                self.cell_j.update_ext_voltages(self.cell_i.get_name(), 0)
                self.path_state = 'idle'
                self.starti = False

    def cellj(self):
        tj_dot = 1
        if self.tj >= self.delta_ji:
            self.last = 'j'
            self.startj = True
            self.path_state = 'relayj'
        elif (self.last != 'j' or self.cell_j.get_state_t_ms_ago(self.delta_ji) != 'q2') and (self.cell_i.get_state() == 'q2'):
            self.path_state = 'cellji'
            self.tji = 0
        elif self.last == 'i' and self.cell_i.get_state_t_ms_ago(self.delta_ij) == 'q2':
            self.path_state = 'anni'
        self.tj += tj_dot * self.dt

    def relayj(self):
        vout_j = self.cell_j.get_v_t_ms_ago(self.delta_ji)
        self.cell_i.update_ext_voltages(self.cell_j.get_name(), vout_j)
        if type(self.cell_j) is PacemakerCell:
            if self.cell_j.get_state() == 'q3' or self.cell_i.get_state() == 'q2':
                self.cell_i.update_ext_voltages(self.cell_j.get_name(), 0)
                self.path_state = 'idle'
        elif type(self.cell_j) is CardiomyocyteCell:
            if self.cell_j.get_state() == 'q4' or self.cell_i.get_state() == 'q2':
                self.cell_i.update_ext_voltages(self.cell_j.get_name(), 0)
                self.path_state = 'idle'

    def cellij(self):
        tij_dot = 1
        if self.cell_i.get_conduction_vel() * (self.tij + self.ti) + self.cell_j.get_conduction_vel() * self.tij >= self.l:
            self.path_state = 'anni'
        self.tij += tij_dot * self.dt

    def cellji(self):
        tji_dot = 1
        if self.cell_j.get_conduction_vel() * (self.tji + self.tj) + self.cell_i.get_conduction_vel() * self.tji >= self.l:
            self.path_state = 'anni'
        self.tji += tji_dot * self.dt

    def anni(self):
        if self.cell_i.get_state() == 'q0' or self.cell_j.get_state() == 'q0':
            self.last = 0
            self.path_state = 'ready'
