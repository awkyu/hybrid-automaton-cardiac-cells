from src.models.HA_PacemakerCell_Model import PacemakerCell
from src.models.HA_Cardiomyocyte_Model import CardiomyocyteCell
from src.models.SubsidiaryPacemakerCell_Model import SubsidiaryPacemakerCell
from src.models.HA_Path_Model import Path
import matplotlib.pyplot as plt
from threading import Thread
import multiprocessing


class Backend:
    def __init__(self, dt):
        self.current_cells = {}
        self.current_selected_cell = ""
        self.current_modfied_params = "{\n}"
        self.current_paths = {}
        self.uid_counter_cell = 0
        self.uid_counter_path = 0
        self.dt = dt
        self.t = 0
        self.counter = 0

    def run_model(self):
        thread_cells = []
        thread_paths = []
        for k in self.current_cells:
            thread_cells.append(Thread(target=self.current_cells[k].run_model))
            # thread_cells.append(multiprocessing.Process(target=self.current_cells[k].run_model))
        for k in self.current_paths:
            thread_paths.append(Thread(target=self.current_paths[k].update_path))
            # thread_paths.append(multiprocessing.Process(target=self.current_paths[k].update_path))
        for thread_worker in thread_cells:
            thread_worker.start()
        for thread_worker in thread_paths:
            thread_worker.start()
        for thread_worker in thread_cells:
            thread_worker.join()
        for thread_worker in thread_paths:
            thread_worker.join()
        # for k in self.current_cells:
            # self.current_cells[k].run_model()
        # for k in self.current_paths:
        #     self.current_paths[k].update_path()
        self.t += self.dt

    def run_model_multiple(self, num):
        for i in range(num):
            self.run_model()

    def get_t(self):
        return self.t

    def get_counter(self):
        return self.counter

    def reset_model(self):
        for k in self.current_cells:
            self.current_cells[k].reset()
        for k in self.current_paths:
            self.current_paths[k].reset()
        self.t = 0
        self.counter = 0

    def get_plot_points(self, cell_name, num_recent_points):
        t_arr = self.current_cells[cell_name].get_t_arr()
        v_arr = self.current_cells[cell_name].get_v_arr()
        plot_points = [(t_arr[i], v_arr[i]) for i in range(len(t_arr))]
        # range_plot_points = plot_points[self.counter-1*num_recent_points:self.counter]
        range_plot_points = plot_points[-1*num_recent_points:]
        self.counter += 1  # TODO: Fix because this is called multiple times per tic (depending on # of active graphs)
        return range_plot_points

    def add_nodalpacemaker(self):
        self.current_cells.update(
            {('nodalpacemaker' + str(self.uid_counter_cell)): PacemakerCell(self.dt,
                                                                            'nodalpacemaker' + str(
                                                                                self.uid_counter_cell))})
        self.uid_counter_cell += 1

    def add_subsidiarypacemaker(self):
        self.current_cells.update(
            {('subsidiarypacemaker' + str(self.uid_counter_cell)): SubsidiaryPacemakerCell(self.dt,
                                                                                           'subsidiarypacemaker' +
                                                                                           str(self.uid_counter_cell))})
        self.uid_counter_cell += 1

    def add_cardiomyocyte(self):
        self.current_cells.update(
            {('cardiomyocyte' + str(self.uid_counter_cell)): CardiomyocyteCell(self.dt,
                                                                               'cardiomyocyte' + str(
                                                                                   self.uid_counter_cell))})
        self.uid_counter_cell += 1

    def get_path_json(self):
        dictionary = {}
        for k in self.current_paths:
            dictionary.update({k: (self.current_paths[k].cell_i.get_name(), self.current_paths[k].cell_j.get_name(),
                                   self.current_paths[k].l)})
        return dictionary

    def get_cells_json(self):
        dictionary = {}
        for k in self.current_cells:
            dictionary.update({k: self.current_cells[k].get_v()})
        # print("Returned Dictionary")
        # print(dictionary)
        return dictionary

    def get_modifiable_cell_params(self, cell_name):
        if cell_name in self.current_cells.keys():
            self.current_selected_cell = cell_name
            return self.current_cells[cell_name].get_dict()

    def update_cell_params(self, cell_name, new_params_dictionary):
        if cell_name in self.current_cells.keys():
            self.current_cells[cell_name].set_params(new_params_dictionary)

    def update_current_cells(self, cell_dict):
        # print("Updating Cells:")
        # print(cell_dict)
        k_list = []
        for k in self.current_cells:
            if k not in cell_dict:
                k_list.append(k)
        for k in k_list:
            self.current_cells.pop(k)
            self.remove_paths_with_cell(k)

    def remove_paths_with_cell(self, cell_name):
        for k in self.current_paths:
            if self.current_paths[k].cell_i.get_name() is cell_name or \
                    self.current_paths[k].cell_j.get_name() is cell_name:
                self.current_paths.pop(k)

    def add_path(self, cell_i_name, cell_j_name, l):
        check = True
        if type(l) is str:
            try:
                l = float(l)
            except:
                check = False
        if type(l) is not int and type(l) is not float:
            check = False
        for k in self.current_paths:
            if (self.current_paths[k].cell_i.get_name() == cell_i_name or self.current_paths[
                k].cell_i.get_name() == cell_j_name) and (
                    self.current_paths[k].cell_j.get_name() == cell_i_name or
                    self.current_paths[k].cell_j.get_name() == cell_j_name):
                check = False
        if cell_i_name == cell_j_name:
            check = False
        if cell_j_name not in self.current_cells.keys() or cell_i_name not in self.current_cells.keys():
            check = False
        if check:
            self.current_paths.update({("path" +
                                        str(self.uid_counter_path)): Path(self.current_cells[cell_i_name],
                                                                          self.current_cells[cell_j_name],
                                                                          l, self.dt)})
            self.uid_counter_path += 1

    def update_paths(self, path_dict):  # path_dict val is a tuple = (cell1_name, cell2_name, length)
        for k in path_dict:
            if k in self.current_paths:
                self.current_paths[k].update_l(path_dict[k][2])

        k_list = []
        for k in self.current_paths:
            if k not in path_dict:
                k_list.append(k)
        for k in k_list:
            self.remove_path_from_cell(k)
            self.current_paths.pop(k)

    def remove_path_from_cell(self, path_name):
        """
        Remove celli and cellj voltages from each other
        """
        cell_i_name = self.current_paths[path_name].cell_i.get_name()
        cell_j_name = self.current_paths[path_name].cell_j.get_name()
        self.current_paths[path_name].cell_i.update_ext_voltages(cell_j_name, 0)
        self.current_paths[path_name].cell_j.update_ext_voltages(cell_i_name, 0)
