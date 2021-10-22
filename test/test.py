import dynamic_variables
import time

def hehe(b=1, *args, **kwargs):
    print(gui1.color.color_code)

gui1 = dynamic_variables.VariableTweaker()
gui1.add_slider('slider', 5, 0, 10, 0.1)
gui1.add_text('text', 'this is a text')
gui1.add_dropdown('dropdown', 'option 1', ['option 1', 'option 2', 'option 3'])
gui1.add_boolean('boolean', True)
gui1.add_color('color', (12, 63, 85))
gui1.add_button('button_name', hehe)
gui1.init_gui()

# gui2 = dynamic_variables.VariableTweaker()
# gui2.add_slider('var1', 5, 0, 10, 1)
# gui2.init_gui()

while True:
    time.sleep(1)
