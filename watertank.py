import threading
import time

water_tank_max_volume = 100 #litter
initial_water_volume = 10 #litter
input_water_tape_flow = 1 #litter/second
output_water_tape_flow = 1 #litter/second
simulate_tick_time = 0.1 #simulation interval time in seconds
control_tick_time = 0.1 #control tick time in seconds

GPIO_volume_sensor = initial_water_volume # gpio input for volume sensor
GPIO_input_water_tape = False # gpio output for input water tape
GPIO_output_water_tape = False # gpio output for output water tape
GPIO_lock = threading.Lock()

class GPIOSimulator():
    """
    This class responsible for returning value from GPIO pins like real situation
    """
    thread_volume_simulator = None

    def volume_simulator(self):
        global GPIO_lock, GPIO_volume_sensor, GPIO_input_water_tape
        global GPIO_output_water_tape, simulate_tick_time
        
        while True:
            GPIO_lock.acquire()
            
            if GPIO_input_water_tape:
                GPIO_volume_sensor += simulate_tick_time*input_water_tape_flow
            if GPIO_output_water_tape:
                GPIO_volume_sensor -= simulate_tick_time*output_water_tape_flow
            print("Current Tank Volume: ", GPIO_volume_sensor)
            
            GPIO_lock.release()
            time.sleep(simulate_tick_time)

    def run(self):
        self.thread_volume_simulator = threading.Thread(target=self.volume_simulator)
        self.thread_volume_simulator.start()

class WatertankController():
    """
    This class responsible for logical function to deal with problem goal.
    """
    def control_volume(self, goal_volume):
        global GPIO_lock, GPIO_volume_sensor, GPIO_input_water_tape
        global GPIO_output_water_tape, control_tick_time
        
        if initial_water_volume < goal_volume:
            GPIO_lock.acquire()
            GPIO_input_water_tape = True
            
            while GPIO_volume_sensor < goal_volume:
                GPIO_lock.release()
                time.sleep(control_tick_time)
                GPIO_lock.acquire()

            print("We reached the goal volume")
            GPIO_input_water_tape = False
            GPIO_lock.release()
        else:
            GPIO_lock.acquire()
            GPIO_output_water_tape = True

            while GPIO_volume_sensor > goal_volume:
                GPIO_lock.release()
                time.sleep(control_tick_time)
                GPIO_lock.acquire()

            print("We reached the goal volume")
            GPIO_output_water_tape = False
            GPIO_lock.release()


def main():
    simulator = GPIOSimulator()
    controller = WatertankController()
    simulator.run()
    controller.control_volume(5)

if __name__ == "__main__":
    main()
