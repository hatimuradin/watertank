import threading
import time


class GlobalParameters:
    def __init__(
        self,
        water_tank_max_volume,
        water_tank_min_desired_volume,
        initial_water_volume,
        initial_temp_degree,
        cold_water_temp,
        hot_water_temp,
        min_desired_temp,
        max_desired_temp,
    ) -> None:
        self.water_tank_max_volume = water_tank_max_volume  # litter
        self.water_tank_min_desired_volume = water_tank_min_desired_volume  # litter
        self.initial_water_volume = initial_water_volume  # litter
        self.initial_temp_degree = initial_temp_degree  # centigrad
        self.cold_water_temp = cold_water_temp  # centigrad
        self.hot_water_temp = hot_water_temp  # centigrad
        self.min_desired_temp = min_desired_temp  # centigrad
        self.max_desired_temp = max_desired_temp  # centigrad
        self.input_cold_water_tape_flow = 1  # litter/second
        self.input_hot_water_tape_flow = 1  # litter/second
        self.output_water_tape_flow = 2  # litter/second

        self.simulate_tick_time = 0.1  # simulation interval time in seconds
        self.control_tick_time = 0.1  # control tick time in seconds

        self.GPIO_volume_sensor = (
            self.initial_water_volume
        )  # gpio input for volume sensor
        self.GPIO_temp_sensor = self.initial_temp_degree  # gpio input for temp sensor
        self.GPIO_input_cold_water_tape = False  # gpio input for cold input water tape
        self.GPIO_input_hot_water_tape = False  # gpio input for hot input water tape
        self.GPIO_output_water_tape = False  # gpio output for output water tape
        self.temp_telorance = 1

        self.GPIO_lock = threading.Lock()
        self.temp_is_ok = False


class GPIOSimulator:
    """
    This class responsible for returning value from GPIO pins like real situation
    """

    def __init__(self, params=None) -> None:
        self.params = params
        self.thread_volume_simulator = None
        self.thread_temp_simulator = None

    def volume_simulator(self):

        while True:
            self.params.GPIO_lock.acquire()
            if self.params.GPIO_input_cold_water_tape:
                self.params.GPIO_volume_sensor += (
                    self.params.simulate_tick_time
                    * self.params.input_cold_water_tape_flow
                )
            if self.params.GPIO_input_hot_water_tape:
                self.params.GPIO_volume_sensor += (
                    self.params.simulate_tick_time
                    * self.params.input_hot_water_tape_flow
                )
            if self.params.GPIO_output_water_tape:
                self.params.GPIO_volume_sensor -= (
                    self.params.simulate_tick_time * self.params.output_water_tape_flow
                )
            print("Current Tank Volume: ", self.params.GPIO_volume_sensor)

            self.params.GPIO_lock.release()
            time.sleep(self.params.simulate_tick_time)

    def temp_simulator(self):

        while True:
            self.params.GPIO_lock.acquire()
            if self.params.GPIO_input_cold_water_tape:
                self.params.GPIO_temp_sensor = (
                    self.params.GPIO_volume_sensor * self.params.GPIO_temp_sensor
                    + self.params.simulate_tick_time
                    * self.params.input_cold_water_tape_flow
                    * self.params.cold_water_temp
                ) / (
                    self.params.GPIO_volume_sensor
                    + self.params.simulate_tick_time
                    * self.params.input_cold_water_tape_flow
                )
            if self.params.GPIO_input_hot_water_tape:
                self.params.GPIO_temp_sensor = (
                    self.params.GPIO_volume_sensor * self.params.GPIO_temp_sensor
                    + self.params.simulate_tick_time
                    * self.params.input_hot_water_tape_flow
                    * self.params.hot_water_temp
                ) / (
                    self.params.GPIO_volume_sensor
                    + self.params.simulate_tick_time
                    * self.params.input_hot_water_tape_flow
                )
            print("Current Tank Temp: ", self.params.GPIO_temp_sensor)

            self.params.GPIO_lock.release()
            time.sleep(self.params.simulate_tick_time)

    def run(self):
        self.thread_volume_simulator = threading.Thread(target=self.volume_simulator)
        self.thread_temp_simulator = threading.Thread(target=self.temp_simulator)
        self.thread_volume_simulator.start()
        self.thread_temp_simulator.start()


class WatertankController:
    """
    This class responsible for logical function to deal with problem goal.
    """

    def __init__(self, params=None) -> None:
        self.params = params
        self.thread_temp_controller = None
        self.thread_volume_controller = None

    def control_volume(self):
        while True:
            self.params.GPIO_lock.acquire()
            if (
                self.params.GPIO_volume_sensor > self.params.water_tank_max_volume
            ) and (self.params.GPIO_output_water_tape == False):
                self.params.GPIO_output_water_tape = True
                print("Opening output tape!")
            if (
                self.params.GPIO_volume_sensor
                < self.params.water_tank_min_desired_volume
            ) and (self.params.GPIO_output_water_tape == True):
                self.params.GPIO_output_water_tape = False
                print("Closing output tape!")
            if self.params.temp_is_ok and self.params.GPIO_input_cold_water_tape:
                self.params.GPIO_input_cold_water_tape = False
                print("Closing cold water tape!")
            if self.params.temp_is_ok and self.params.GPIO_input_hot_water_tape:
                self.params.GPIO_input_hot_water_tape = False
                print("Closing hot water tape!")
            if (
                self.params.temp_is_ok
                and self.params.GPIO_volume_sensor
                < self.params.water_tank_min_desired_volume
            ):
                print("Opening cold and hot tapes equally")
                self.params.GPIO_input_cold_water_tape = True
                self.params.GPIO_input_hot_water_tape = True
            if (
                self.params.temp_is_ok
                and (
                    self.params.GPIO_volume_sensor
                    > self.params.water_tank_min_desired_volume
                )
                and (
                    self.params.GPIO_input_cold_water_tape
                    and self.params.GPIO_input_hot_water_tape
                )
            ):
                print("Temp and volume are ok, closing input tapes")
                self.params.GPIO_input_cold_water_tape = False
                self.params.GPIO_input_hot_water_tape = False

            self.params.GPIO_lock.release()
            time.sleep(self.params.control_tick_time)

    def control_temp(self):
        while True:
            self.params.GPIO_lock.acquire()
            if (self.params.GPIO_temp_sensor < self.params.min_desired_temp) and (
                self.params.GPIO_input_hot_water_tape == False
            ):
                self.params.temp_is_ok = False
                self.params.GPIO_input_hot_water_tape = True
                print("Opening hot tape!")

            elif (self.params.GPIO_temp_sensor > self.params.max_desired_temp) and (
                self.params.GPIO_input_cold_water_tape == False
            ):
                self.params.temp_is_ok = False
                self.params.GPIO_input_cold_water_tape = True
                print("Opening cold water tape!")
            elif (self.params.GPIO_temp_sensor > self.params.min_desired_temp) and (
                self.params.GPIO_temp_sensor < self.params.max_desired_temp
            ):
                self.params.temp_is_ok = True
                print("Temp is ok!")
            self.params.GPIO_lock.release()
            time.sleep(self.params.control_tick_time)

    def run(self):
        self.thread_temp_controller = threading.Thread(target=self.control_temp)
        self.thread_volume_controller = threading.Thread(target=self.control_volume)
        self.thread_temp_controller.start()
        self.thread_volume_controller.start()
