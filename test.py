import dynamic_variables as dv
import time

dv.create_slider('var1', 5, 0, 10, 1)
dv.create_slider('var2', 1, 0, 10, 1)
dv.init_gui()

while True:
    print(dv.var1, dv.var2)
    time.sleep(0.1)
