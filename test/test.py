import dynamic_variables as dv
import time


def print_everything():
    print(slider)
    print(text)
    print(dropdown)
    print(boolean)
    print(color.tuple)


dv.add_slider('slider', 0, 10)
dv.add_text('text')
dv.add_dropdown('dropdown', ['option 1', 'option 2', 'option 3'])
dv.add_boolean('boolean')
dv.add_color('color')
dv.add_button('button', print_everything)
dv.init_gui(theme='dark', color='sweetkind')


while True:
    time.sleep(1)
