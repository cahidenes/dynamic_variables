import dynamic_variables
import time

gui1 = dynamic_variables.VariableTweaker()
gui1.add_slider('var1', 5, 0, 10, 0.1)
gui1.add_slider('var2', 1, 0, 10, 0.1)

gui1.init_gui()

# gui2 = dynamic_variables.VariableTweaker()
# gui2.add_slider('var1', 5, 0, 10, 1)
# gui2.init_gui()

while True:
    print(gui1.var1, gui1.var2)
    time.sleep(1)
