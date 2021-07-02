from gui import WaterTankGUI
from watertank import GPIOSimulator, WatertankController


def main():
    simulator = GPIOSimulator()
    controller = WatertankController()
    gui = WaterTankGUI(simulator, controller)
    gui.app.display()


if __name__ == "__main__":
    main()
