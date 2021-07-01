import threading
import time

water_tank_max_volume = 200  # litter
water_tank_min_desired_volume = 100  # litter
initial_water_volume = 80  # litter
initial_temp_degree = 25  # centigrad
cold_water_temp = 10  # centigrad
hot_water_temp = 50  # centigrad
min_desired_temp = 20  # centigrad
max_desired_temp = 40  # centigrad
input_cold_water_tape_flow = 1  # litter/second
input_hot_water_tape_flow = 1  # litter/second
output_water_tape_flow = 2  # litter/second
simulate_tick_time = 0.1  # simulation interval time in seconds
control_tick_time = 0.1  # control tick time in seconds
temp_is_ok = False

GPIO_volume_sensor = initial_water_volume  # gpio input for volume sensor
GPIO_temp_sensor = initial_temp_degree  # gpio input for temp sensor
GPIO_input_cold_water_tape = False  # gpio input for cold input water tape
GPIO_input_hot_water_tape = False  # gpio input for hot input water tape
GPIO_output_water_tape = False  # gpio output for output water tape

temp_telorance = 1

GPIO_lock = threading.Lock()


class GPIOSimulator:
    """
    This class responsible for returning value from GPIO pins like real situation
    """

    thread_volume_simulator = None
    thread_temp_simulator = None

    def volume_simulator(self):
        global GPIO_lock, GPIO_volume_sensor, GPIO_input_cold_water_tape, GPIO_input_hot_water_tape, GPIO_output_water_tape, simulate_tick_time

        while True:
            GPIO_lock.acquire()
            if GPIO_input_cold_water_tape:
                GPIO_volume_sensor += simulate_tick_time * input_cold_water_tape_flow
            if GPIO_input_hot_water_tape:
                GPIO_volume_sensor += simulate_tick_time * input_hot_water_tape_flow
            if GPIO_output_water_tape:
                GPIO_volume_sensor -= simulate_tick_time * output_water_tape_flow
            print("Current Tank Volume: ", GPIO_volume_sensor)

            GPIO_lock.release()
            time.sleep(simulate_tick_time)

    def temp_simulator(self):
        global GPIO_lock, GPIO_volume_sensor, GPIO_input_cold_water_tape, GPIO_input_hot_water_tape, GPIO_output_water_tape, simulate_tick_time, GPIO_temp_sensor

        while True:
            GPIO_lock.acquire()
            if GPIO_input_cold_water_tape:
                GPIO_temp_sensor = (
                    GPIO_volume_sensor * GPIO_temp_sensor
                    + simulate_tick_time * input_cold_water_tape_flow * cold_water_temp
                ) / (
                    GPIO_volume_sensor + simulate_tick_time * input_cold_water_tape_flow
                )
            if GPIO_input_hot_water_tape:
                GPIO_temp_sensor = (
                    GPIO_volume_sensor * GPIO_temp_sensor
                    + simulate_tick_time * input_hot_water_tape_flow * hot_water_temp
                ) / (
                    GPIO_volume_sensor + simulate_tick_time * input_hot_water_tape_flow
                )
            print("Current Tank Temp: ", GPIO_temp_sensor)

            GPIO_lock.release()
            time.sleep(simulate_tick_time)

    def run(self):
        self.thread_volume_simulator = threading.Thread(target=self.volume_simulator)
        self.thread_temp_simulator = threading.Thread(target=self.temp_simulator)
        self.thread_volume_simulator.start()
        self.thread_temp_simulator.start()


class WatertankController:
    """
    This class responsible for logical function to deal with problem goal.
    """

    thread_temp_controller = None
    thread_volume_controller = None

    def control_volume(self):
        global GPIO_lock, GPIO_volume_sensor, GPIO_input_cold_water_tape, GPIO_input_hot_water_tape, GPIO_output_water_tape, control_tick_time

        while True:
            GPIO_lock.acquire()
            if (GPIO_volume_sensor > water_tank_max_volume) and (
                GPIO_output_water_tape == False
            ):
                GPIO_output_water_tape = True
                print("Opening output tape!")
            if (GPIO_volume_sensor < water_tank_min_desired_volume) and (
                GPIO_output_water_tape == True
            ):
                GPIO_output_water_tape = False
                print("Closing output tape!")
            if temp_is_ok and GPIO_input_cold_water_tape:
                GPIO_input_cold_water_tape = False
                print("Closing cold water tape!")
            if temp_is_ok and GPIO_input_hot_water_tape:
                GPIO_input_hot_water_tape = False
                print("Closing hot water tape!")
            if temp_is_ok and GPIO_volume_sensor < water_tank_min_desired_volume:
                print("Opening cold and hot tapes equally")
                GPIO_input_cold_water_tape = True
                GPIO_input_hot_water_tape = True
            if (
                temp_is_ok
                and (GPIO_volume_sensor > water_tank_min_desired_volume)
                and (GPIO_input_cold_water_tape and GPIO_input_hot_water_tape)
            ):
                print("Temp and volume are ok, closing input tapes")
                GPIO_input_cold_water_tape = False
                GPIO_input_hot_water_tape = False

            GPIO_lock.release()
            time.sleep(control_tick_time)

    def control_temp(self):
        global GPIO_lock, GPIO_input_cold_water_tape, GPIO_input_hot_water_tape, GPIO_output_water_tape, control_tick_time, temp_is_ok

        while True:
            GPIO_lock.acquire()
            if (GPIO_temp_sensor < min_desired_temp) and (
                GPIO_input_hot_water_tape == False
            ):
                temp_is_ok = False
                GPIO_input_hot_water_tape = True
                print("Opening hot tape!")

            elif (GPIO_temp_sensor > max_desired_temp) and (
                GPIO_input_cold_water_tape == False
            ):
                temp_is_ok = False
                GPIO_input_cold_water_tape = True
                print("Opening cold water tape!")
            elif (GPIO_temp_sensor > min_desired_temp) and (
                GPIO_temp_sensor < max_desired_temp
            ):
                temp_is_ok = True
                print("Temp is ok!")
            GPIO_lock.release()
            time.sleep(control_tick_time)

    def run(self):
        self.thread_temp_controller = threading.Thread(target=self.control_temp)
        self.thread_volume_controller = threading.Thread(target=self.control_volume)
        self.thread_temp_controller.start()
        self.thread_volume_controller.start()


def main():
    simulator = GPIOSimulator()
    controller = WatertankController()
    simulator.run()
    controller.run()


if __name__ == "__main__":
    main()
