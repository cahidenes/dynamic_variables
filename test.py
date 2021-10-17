import dynamic_variables
import time

gui1 = dynamic_variables.VariableTweaker()
gui1.add_slider('slidervar', 5, 0, 10, 0.1)
gui1.add_text('textvar', 'asdf')
gui1.add_dropdown('dropdownvar', 1, [1, 'abc', True, False])
gui1.add_boolean('booleanvar', True)
gui1.add_color('colorvar', (12, 63, 85))

gui1.init_gui()

# gui2 = dynamic_variables.VariableTweaker()
# gui2.add_slider('var1', 5, 0, 10, 1)
# gui2.init_gui()

while True:
    print(gui1.slidervar, gui1.textvar, gui1.booleanvar, gui1.dropdownvar)
    time.sleep(1)
