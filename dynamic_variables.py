import tkinter as tk
import threading

create_requests = []


def get_setter(name):
    def setter(scale_value):
        globals()[name] = scale_value
    return setter


def create_slider(name, value, min_value, max_value, step):
    create_requests.append(('slider', (name, value, min_value, max_value, step)))


def init_gui_thread():

    for request_name, parameters in create_requests:
        globals()[parameters[0]] = parameters[1]

    window = tk.Tk()
    variables = []
    for request_name, parameters in create_requests:
        if request_name == 'slider':
            name, value, min_value, max_value, step = parameters
            globals()[name] = value
            scl = tk.Scale(from_=min_value, to=max_value, resolution=step, orient=tk.HORIZONTAL, command=get_setter(name))
            scl.set(value)
            scl.pack()
            variables.append((name, value, scl))

    def constant_checker():
        for i, (name, last, scale) in enumerate(variables):
            if globals()[name] != last:
                variables[i] = (name, globals()[name], scale)
                scale.set(globals()[name])
        window.after(1000, constant_checker)

    window.after(1000, constant_checker)
    window.mainloop()


def init_gui():
    threading.Thread(target=init_gui_thread).start()
