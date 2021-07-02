from guizero import App, Text, TextBox, Box, PushButton
from watertank import GlobalParameters, GPIOSimulator, WatertankController
import time


class WaterTankGUI:
    def __init__(self, simulator=None, controller=None) -> None:
        self.simulator = simulator
        self.controller = controller

        self.app = App(layout="grid", height=600, width=800)

        self.parameter_box = Box(self.app, border=1, width=300, height=360, grid=[0, 0])
        self.parameter_box_title = Text(
            self.parameter_box, text="parameter list", color="blue", size=20
        )

        self.water_tank_max_volume_box = Box(
            self.parameter_box, width=300, height=30, grid=[0, 0]
        )
        self.water_tank_max_volume_label = Text(
            self.water_tank_max_volume_box, text="water tank max volume", align="left"
        )
        self.water_tank_max_volume_text = TextBox(
            self.water_tank_max_volume_box, align="left", text=200
        )

        self.water_tank_min_desired_volume_box = Box(
            self.parameter_box, width=300, height=30, grid=[0, 1]
        )
        self.water_tank_min_desired_volume_lable = Text(
            self.water_tank_min_desired_volume_box,
            text="water tank min desired value",
            align="left",
        )
        self.water_tank_min_desired_volume_text = TextBox(
            self.water_tank_min_desired_volume_box, align="left", text=100
        )

        self.initial_water_volume = Box(
            self.parameter_box, width=300, height=30, grid=[0, 2]
        )
        self.initial_water_volume_lable = Text(
            self.initial_water_volume, text="initial water volume", align="left"
        )
        self.initial_water_volume_text = TextBox(
            self.initial_water_volume, align="left", text=120
        )

        self.initial_temp_degree = Box(
            self.parameter_box, width=300, height=30, grid=[0, 3]
        )
        self.initial_temp_degree_lable = Text(
            self.initial_temp_degree,
            text="initial temperature degree",
            align="left",
        )
        self.initial_temp_degree_text = TextBox(self.initial_temp_degree, align="left")

        self.cold_water_temp = Box(
            self.parameter_box, width=300, height=30, grid=[0, 4]
        )
        self.cold_water_temp_lable = Text(
            self.cold_water_temp, text="cold water temp", align="left"
        )
        self.cold_water_temp_text = TextBox(self.cold_water_temp, align="left", text=20)

        self.hot_water_temp = Box(self.parameter_box, width=300, height=30, grid=[0, 5])
        self.hot_water_temp_lable = Text(
            self.hot_water_temp, text="hot water temp", align="left"
        )
        self.hot_water_temp_text = TextBox(self.hot_water_temp, align="left", text=40)

        self.min_desired_temp = Box(
            self.parameter_box, width=300, height=30, grid=[0, 6]
        )
        self.min_desired_temp_lable = Text(
            self.min_desired_temp, text="min desired temp", align="left"
        )
        self.min_desired_temp_text = TextBox(
            self.min_desired_temp, align="left", text=25
        )

        self.max_desired_temp = Box(
            self.parameter_box, width=300, height=30, grid=[0, 7]
        )
        self.max_desired_temp_lable = Text(
            self.max_desired_temp, text="max desired temp", align="left"
        )
        self.max_desired_temp_text = TextBox(
            self.max_desired_temp, align="left", text=35
        )

        self.input_cold_water_tape_flow = Box(
            self.parameter_box, width=300, height=30, grid=[0, 8]
        )
        self.input_cold_water_tape_flow_lable = Text(
            self.input_cold_water_tape_flow,
            text="input cold water tape flow",
            align="left",
        )
        self.input_cold_water_tape_flow_text = TextBox(
            self.input_cold_water_tape_flow, align="left", text=1
        )

        self.input_hot_water_tape_flow = Box(
            self.parameter_box, width=300, height=30, grid=[0, 9]
        )
        self.input_hot_water_tape_flow_lable = Text(
            self.input_hot_water_tape_flow,
            text="input hot water tape flow",
            align="left",
        )
        self.input_hot_water_tape_flow_text = TextBox(
            self.input_hot_water_tape_flow, align="left", text=1
        )

        self.output_water_tape_flow = Box(
            self.parameter_box, width=300, height=30, grid=[0, 9]
        )
        self.output_water_tape_flow_lable = Text(
            self.output_water_tape_flow, text="putput water tape flow", align="left"
        )
        self.output_water_tape_flow_text = TextBox(
            self.output_water_tape_flow, align="left", text=1
        )

        self.sensor_box = Box(self.app, border=1, width=300, height=360, grid=[1, 0])
        self.sensor_box_title = Text(
            self.sensor_box, text="GPIO status", color="blue", size=20
        )

        self.cold_water_tape_status = Box(
            self.sensor_box, width=300, height=70, grid=[0, 0]
        )
        self.cold_water_tape_status_lable = Text(
            self.cold_water_tape_status, text="cold water tape status", align="left"
        )
        self.cold_water_tape_status_text = TextBox(
            self.cold_water_tape_status, align="left"
        )

        self.hot_water_tape_status = Box(
            self.sensor_box, width=300, height=30, grid=[0, 1]
        )
        self.hot_water_tape_status_lable = Text(
            self.hot_water_tape_status, text="hot water tape status", align="left"
        )
        self.hot_water_tape_status_text = TextBox(
            self.hot_water_tape_status, align="left"
        )

        self.output_water_tape_status = Box(
            self.sensor_box, width=300, height=70, grid=[0, 2]
        )
        self.output_water_tape_status_lable = Text(
            self.output_water_tape_status, text="output water tape status", align="left"
        )
        self.output_water_tape_status_text = TextBox(
            self.output_water_tape_status, align="left"
        )

        self.volume_sensor = Box(self.sensor_box, width=300, height=100, grid=[0, 3])
        self.volume_sensor_lable = Text(
            self.volume_sensor, text="volume sensor", align="left"
        )
        self.volume_sensor_text = TextBox(self.volume_sensor, align="left")

        self.temp_sensor = Box(self.sensor_box, width=300, height=30, grid=[0, 4])
        self.temp_sensor_lable = Text(
            self.temp_sensor, text="temprature sensor", align="left"
        )
        self.temp_sensor_text = TextBox(self.temp_sensor, align="left")

        self.start_box = Box(
            self.app, border=1, width=600, height=60, grid=[0, 1, 2, 1]
        )
        self.buttons_box = Box(self.start_box, width="fill", align="bottom")
        self.start_button = PushButton(self.buttons_box, text="start", padx=10, pady=10)
        self.start_button.when_clicked = self.start_clicked

    def convert_to_int(self, string) -> int:
        return int(string)

    def start_clicked(self):
        params = GlobalParameters(
            water_tank_max_volume=self.convert_to_int(
                self.water_tank_max_volume_text._text.get()
            ),
            water_tank_min_desired_volume=self.convert_to_int(
                self.water_tank_min_desired_volume_text._text.get()
            ),
            initial_water_volume=self.convert_to_int(
                self.initial_water_volume_text._text.get()
            ),
            initial_temp_degree=self.convert_to_int(
                self.initial_temp_degree_text._text.get()
            ),
            cold_water_temp=self.convert_to_int(self.cold_water_temp_text._text.get()),
            hot_water_temp=self.convert_to_int(self.hot_water_temp_text._text.get()),
            min_desired_temp=self.convert_to_int(
                self.min_desired_temp_text._text.get()
            ),
            max_desired_temp=self.convert_to_int(
                self.max_desired_temp_text._text.get()
            ),
        )
        self.simulator.params = params
        self.controller.params = params
        self.simulator.run()
        self.controller.run()

    def update_cold_water_tape_status(self):
        self.cold_water_tape_status_text._text.set("4")

    def update_GPIO(self, params=None):
        # print GPIO status to gui
        params.GPIO_lock.acquire()
        self.cold_water_tape_status_text.repeat(100, self.update_cold_water_tape_status)
        self.hot_water_tape_status_text._text.set(str(params.GPIO_input_hot_water_tape))
        self.output_water_tape_status_text._text.set(str(params.GPIO_output_water_tape))
        self.volume_sensor_text._text.set(str(params.GPIO_volume_sensor))
        self.temp_sensor_text._text.set(str(params.GPIO_temp_sensor))
        params.GPIO_lock.release()
        time.sleep(params.simulate_tick_time)
        self.app.after(100, self.update_GPIO)
