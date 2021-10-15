import tkinter as tk
import threading


def get_setter(obj, name):
    def setter(scale_value):
        setattr(obj, name, scale_value)
    return setter


class VariableTweaker:
    def __init__(self):
        self.create_requests = []
        self.window = None

    def add_slider(self, name, value, min_value, max_value, step):
        self.create_requests.append(('slider', (name, value, min_value, max_value, step)))

    def init_gui_thread(self):
        for request_name, parameters in self.create_requests:
            setattr(self, parameters[0], parameters[1])

        self.window = tk.Tk()
        variables = []
        for request_name, parameters in self.create_requests:
            if request_name == 'slider':
                name, value, min_value, max_value, step = parameters
                scl = tk.Scale(self.window, from_=min_value, to=max_value, resolution=step,
                               orient=tk.HORIZONTAL, command=get_setter(self, name))
                scl.set(value)
                scl.pack()
                variables.append((name, scl))

        def constant_checker():
            for i, (variable_name, scale) in enumerate(variables):
                new_value = getattr(self, variable_name)
                if new_value != scale.get():
                    variables[i] = (variable_name, scale)
                    scale.set(new_value)
            self.window.after(100, constant_checker)

        self.window.after(100, constant_checker)
        self.window.mainloop()

    def init_gui(self):
        threading.Thread(target=self.init_gui_thread, daemon=True).start()
