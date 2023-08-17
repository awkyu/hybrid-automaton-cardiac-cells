from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

import os
import json
from threading import Thread

from src.Backend import Backend


class Logic(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dt = 1
        self.t_max = 5000
        self.backend = Backend(self.dt)
        self.lead_time = 1000  # time (ms) that the simulation stays ahead on (multi-threading efficiency reasons)
        self.sim_lead = 3000

        Clock.schedule_once(self.init_ui, 0)
        self.red_plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.blue_plot = MeshLinePlot(color=[0, 0, 1, 1])
        self.green_plot = MeshLinePlot(color=[0, 1, 0, 1])
        self.white_plot = MeshLinePlot(color=[1, 1, 1, 1])
        self.graph = Graph(xlabel='Time (ms)', ylabel='Membrane Voltage (mV)', x_ticks_minor=100,
                           x_ticks_major=1000, y_ticks_minor=10, y_ticks_major=50,
                           y_grid_label=True, x_grid_label=True, padding=5,
                           x_grid=True, y_grid=True, xmin=0, xmax=self.t_max, ymin=-50, ymax=180)

        self.add_nodalpm_button = Button(text='Add Nodal Pacemaker Cell')
        self.add_subpm_button = Button(text='Add Subsidiary Pacemaker Cell')
        self.add_cm_button = Button(text='Add Cardiomyocyte Cell')
        self.curr_cells_text = TextInput(text='{\n}', multiline=True)
        self.update_cells = Button(text='Update Cell List')
        self.add_nodalpm_button.bind(on_release=self.add_nodalpacemaker)
        self.add_subpm_button.bind(on_release=self.add_subsidiarypacemaker)
        self.add_cm_button.bind(on_release=self.add_cardiomyocyte)
        self.update_cells.bind(on_release=self.update_cells_callback)
        self.cell_i_input = TextInput(text='', multiline=False)
        self.cell_j_input = TextInput(text='', multiline=False)
        self.length_input = TextInput(text='', multiline=False)
        self.add_paths = Button(text='Add Path')
        self.curr_paths_text = TextInput(text='{\n}', multiline=True)
        self.update_paths = Button(text='Update Paths')
        self.add_paths.bind(on_release=self.add_path_callback)
        self.update_paths.bind(on_release=self.update_paths_callback)
        self.cell_selection_input = TextInput(text='', multiline=False)
        self.cell_selection_button = Button(text='Select')
        self.cell_param_text = TextInput(text='{\n}', multiline=True)
        self.cell_update_params_button = Button(text='Update Cell Parameters')
        self.cell_selection_button.bind(on_release=self.select_cell)
        self.cell_update_params_button.bind(on_release=self.update_cell_params)
        self.red_selection = TextInput(text='', multiline=False)
        self.blue_selection = TextInput(text='', multiline=False)
        self.green_selection = TextInput(text='', multiline=False)
        self.white_selection = TextInput(text='', multiline=False)

    def init_ui(self, dt=0):
        self.ids.addcells.add_widget(self.add_nodalpm_button)
        self.ids.addcells.add_widget(self.add_subpm_button)
        self.ids.addcells.add_widget(self.add_cm_button)
        self.ids.currcells.add_widget(self.curr_cells_text)
        self.ids.updatecells.add_widget(self.update_cells)
        self.ids.celli_input.add_widget(self.cell_i_input)
        self.ids.cellj_input.add_widget(self.cell_j_input)
        self.ids.length_input.add_widget(self.length_input)
        self.ids.addpathsbutton.add_widget(self.add_paths)
        self.ids.pathstext.add_widget(self.curr_paths_text)
        self.ids.updatepathsbutton.add_widget(self.update_paths)
        self.ids.cell_selection_input.add_widget(self.cell_selection_input)
        self.ids.cell_selection_button.add_widget(self.cell_selection_button)
        self.ids.cellparams_text.add_widget(self.cell_param_text)
        self.ids.update_cellparams.add_widget(self.cell_update_params_button)
        self.ids.graph.add_widget(self.graph)
        self.ids.red_selection.add_widget(self.red_selection)
        self.ids.blue_selection.add_widget(self.blue_selection)
        self.ids.green_selection.add_widget(self.green_selection)
        self.ids.white_selection.add_widget(self.white_selection)

    def select_cell(self, dt=0):
        self.cell_param_text.text = json.dumps(self.backend.get_modifiable_cell_params(self.cell_selection_input.text),
                                               indent=2)

    def update_cell_params(self, dt=0):
        if self.cell_selection_input.text == self.backend.current_selected_cell:
            self.backend.update_cell_params(self.backend.current_selected_cell, json.loads(self.cell_param_text.text))
            self.cell_param_text.text = json.dumps(
                self.backend.get_modifiable_cell_params(self.cell_selection_input.text),
                indent=2)

    def update_paths_callback(self, dt=0):
        self.backend.update_paths(json.loads(self.curr_paths_text.text))

    def add_path_callback(self, dt=0):
        self.backend.add_path(self.cell_i_input.text, self.cell_j_input.text, self.length_input.text)
        self.curr_paths_text.text = json.dumps(self.backend.get_path_json(), indent=2)
        self.cell_j_input.text = ''
        self.cell_i_input.text = ''
        self.length_input.text = ''

    def add_nodalpacemaker(self, dt=0):
        self.backend.add_nodalpacemaker()
        self.curr_cells_text.text = json.dumps(self.backend.get_cells_json(), indent=2)

    def add_subsidiarypacemaker(self, dt=0):
        self.backend.add_subsidiarypacemaker()
        self.curr_cells_text.text = json.dumps(self.backend.get_cells_json(), indent=2)

    def add_cardiomyocyte(self, dt=0):
        self.backend.add_cardiomyocyte()
        self.curr_cells_text.text = json.dumps(self.backend.get_cells_json(), indent=2)

    def update_cells_callback(self, dt=0):
        self.backend.update_current_cells(json.loads(self.curr_cells_text.text))
        self.curr_cells_text.text = json.dumps(self.backend.get_cells_json(), indent=2)

    def start(self):
        if self.red_selection.text in self.backend.current_cells.keys():
            self.graph.add_plot(self.red_plot)
        if self.blue_selection.text in self.backend.current_cells.keys():
            self.graph.add_plot(self.blue_plot)
        if self.green_selection.text in self.backend.current_cells.keys():
            self.graph.add_plot(self.green_plot)
        if self.white_selection.text in self.backend.current_cells.keys():
            self.graph.add_plot(self.white_plot)
        Clock.schedule_interval(self.get_value, self.dt/1000)

    def stop(self):
        Clock.unschedule(self.get_value)

    def reset(self):
        self.backend.reset_model()
        self.graph.xmin = 0
        self.graph.xmax = self.t_max

    def get_value(self, dt):
        # if self.backend.get_counter()*self.dt + self.lead_time > self.backend.get_t():
        #     model_thread = Thread(target=self.backend.run_model_multiple, args=[int(self.sim_lead/self.dt)])
        #     model_thread.start()
        #     # self.backend.run_model_multiple(int(self.sim_lead/self.dt))
        self.backend.run_model()
        if self.red_selection.text in self.backend.current_cells.keys():
            self.red_plot.points = self.backend.get_plot_points(self.red_selection.text, int(self.t_max/self.dt))
        if self.blue_selection.text in self.backend.current_cells.keys():
            self.blue_plot.points = self.backend.get_plot_points(self.blue_selection.text, int(self.t_max/self.dt))
        if self.green_selection.text in self.backend.current_cells.keys():
            self.green_plot.points = self.backend.get_plot_points(self.green_selection.text, int(self.t_max/self.dt))
        if self.white_selection.text in self.backend.current_cells.keys():
            self.white_plot.points = self.backend.get_plot_points(self.white_selection.text, int(self.t_max/self.dt))
        # if self.backend.get_counter()*self.dt > self.t_max:
        if self.backend.get_t() > self.t_max:
            self.graph.xmin += self.dt
            self.graph.xmax += self.dt


class CardiacCells(App):
    def build(self):
        kivy_file = os.getcwd() + '\\src\\gui\\look.kv'
        return Builder.load_file(kivy_file)
