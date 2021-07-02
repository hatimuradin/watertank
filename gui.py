from guizero import App, Text, TextBox, Box, PushButton

app = App(layout="grid", height=600, width=800)

parameter_box = Box(app, border=1, width=300, height=360, grid=[0, 0])
text1 = Text(parameter_box, text="parameter list", color="blue", size=20)

water_tank_max_volume_box = Box(parameter_box, width=300, height=30, grid=[0, 0])
text = Text(water_tank_max_volume_box, text="water tank max volume", align="left")
text_box = TextBox(water_tank_max_volume_box, align="left", text=200)

water_tank_min_desired_volume_box = Box(
    parameter_box, width=300, height=30, grid=[0, 1]
)
text = Text(
    water_tank_min_desired_volume_box, text="water tank min desired value", align="left"
)
text_box = TextBox(water_tank_min_desired_volume_box, align="left", text=100)


initial_water_volume = Box(parameter_box, width=300, height=30, grid=[0, 2])
text = Text(initial_water_volume, text="initial water volume", align="left")
text_box = TextBox(initial_water_volume, align="left", text=120)

initial_temp_degree = Box(parameter_box, width=300, height=30, grid=[0, 3])
text = Text(initial_temp_degree, text="initial temperature degree", align="left")
text_box = TextBox(initial_temp_degree, align="left")

cold_water_temp = Box(parameter_box, width=300, height=30, grid=[0, 4])
text = Text(cold_water_temp, text="cold water temp", align="left")
text_box = TextBox(cold_water_temp, align="left", text=20)

hot_water_temp = Box(parameter_box, width=300, height=30, grid=[0, 5])
text = Text(hot_water_temp, text="hot water temp", align="left")
text_box = TextBox(hot_water_temp, align="left", text=40)

min_desired_temp = Box(parameter_box, width=300, height=30, grid=[0, 6])
text = Text(min_desired_temp, text="min desired temp", align="left")
text_box = TextBox(min_desired_temp, align="left", text=25)

max_desired_temp = Box(parameter_box, width=300, height=30, grid=[0, 7])
text = Text(max_desired_temp, text="max desired temp", align="left")
text_box = TextBox(max_desired_temp, align="left", text=35)

input_cold_water_tape_flow = Box(parameter_box, width=300, height=30, grid=[0, 8])
text = Text(input_cold_water_tape_flow, text="input cold water tape flow", align="left")
text_box = TextBox(input_cold_water_tape_flow, align="left", text=1)

input_hot_water_tape_flow = Box(parameter_box, width=300, height=30, grid=[0, 9])
text = Text(input_hot_water_tape_flow, text="input hot water tape flow", align="left")
text_box = TextBox(input_hot_water_tape_flow, align="left", text=1)

output_water_tape_flow = Box(parameter_box, width=300, height=30, grid=[0, 9])
text = Text(output_water_tape_flow, text="putput water tape flow", align="left")
text_box = TextBox(output_water_tape_flow, align="left", text=1)


sensor_box = Box(app, border=1, width=300, height=360, grid=[1, 0])
text2 = Text(sensor_box, text="GPIO status", color="blue", size=20)

cold_water_tape_status = Box(sensor_box, width=300, height=70, grid=[0, 0])
text = Text(cold_water_tape_status, text="cold water tape status", align="left")
text_box = TextBox(cold_water_tape_status, align="left")


hot_water_tape_status = Box(sensor_box, width=300, height=30, grid=[0, 1])
text = Text(hot_water_tape_status, text="hot water tape status", align="left")
text_box = TextBox(hot_water_tape_status, align="left")

output_water_tape_status = Box(sensor_box, width=300, height=70, grid=[0, 2])
text = Text(output_water_tape_status, text="output water tape status", align="left")
text_box = TextBox(output_water_tape_status, align="left")

volume_sensor = Box(sensor_box, width=300, height=100, grid=[0, 3])
text = Text(volume_sensor, text="volume sensor", align="left")
text_box = TextBox(volume_sensor, align="left")

temp_sensor = Box(sensor_box, width=300, height=30, grid=[0, 4])
text = Text(temp_sensor, text="temprature sensor", align="left")
text_box = TextBox(temp_sensor, align="left")


start_box = Box(app, border=1, width=600, height=60, grid=[0, 1, 2, 1])
buttons_box = Box(start_box, width="fill", align="bottom")
start = PushButton(buttons_box, text="start", align="middle", padx=10, pady=10)


app.display()
