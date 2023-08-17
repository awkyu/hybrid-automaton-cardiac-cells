import sys
import os

# print(os.getcwd())
sys.path.append(os.getcwd())

from src.models.HA_PacemakerCell_Model import PacemakerCell
from src.models.HA_Cardiomyocyte_Model import CardiomyocyteCell
from src.models.SubsidiaryPacemakerCell_Model import SubsidiaryPacemakerCell
from src.models.HA_Path_Model import Path
import matplotlib.pyplot as plt
from threading import Thread

from src.gui.CardiacCellsApp import CardiacCells


def main():
    dt = 1  # milliseconds
    # global backend
    # backend = Backend(dt)
    SAN = PacemakerCell(dt, 'SAN')
    test = CardiomyocyteCell(dt, 'test')
    test2 = CardiomyocyteCell(dt, 'test2')
    test_path = Path(SAN, test, 20, dt)
    test_path2 = Path(SAN, test2, 2000, dt)
    print(test_path.delta_ij)
    for i in range(int(5000 / dt)):
        SAN.run_model()
        test.run_model()
        test2.run_model()
        # print(test.ext_voltages)
        test_path.update_path()
        test_path2.update_path()
        # print(test_path.path_state)
    plt.plot(SAN.get_t_arr(), SAN.get_v_arr())
    plt.show()
    plt.plot(test.get_t_arr(), test.get_v_arr())
    plt.show()
    plt.plot(test2.get_t_arr(), test2.get_v_arr())
    plt.show()
    print(SAN.get_v_arr())


if __name__ == "__main__":
    # get_backend_thread = Thread(target=main)
    # get_backend_thread.daemon = True
    # get_backend_thread.start()
    # main()
    CardiacCells().run()
