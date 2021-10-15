import tkinter as tk
import tkinter.font as tkfont
import threading


def get_setter(obj, name):
    def setter(scale_value):
        setattr(obj, name, scale_value)
    return setter


def get_text_callback(obj, name, entry):
    def callback():
        obj.window.after(10, lambda: setattr(obj, name, entry.get()))
        return True
    return callback


def get_boolean_callback(obj, name, var):
    def callback():
        setattr(obj, name, var.get())
    return callback


class VariableTweaker:
    def __init__(self):
        self.create_requests = []
        self.window = None

    def add_slider(self, name, value, min_value, max_value, step):
        self.create_requests.append(('slider', (name, value, min_value, max_value, step)))

    def add_text(self, name, value):
        self.create_requests.append(('text', (name, value)))

    def add_dropdown(self, name, value, options):
        self.create_requests.append(('dropdown', (name, value, options)))

    def add_boolean(self, name, value):
        self.create_requests.append(('boolean', (name, value)))

    def init_gui_thread(self, window_name='Variable Tweaker', label_font_size=15, widget_font_size=10):
        for request_name, parameters in self.create_requests:
            setattr(self, parameters[0], parameters[1])

        self.window = tk.Tk()
        self.window.title(window_name)
        label_font = tkfont.Font(family='Helvetica', size=label_font_size)
        widget_font = tkfont.Font(family='Helvetica', size=widget_font_size)
        option_dropdown_font = tkfont.Font(family='Helvetica', size=int(widget_font_size*0.8))
        variables = []
        for request_name, parameters in self.create_requests:
            frame = tk.Frame(self.window)
            label = tk.Label(frame, text=parameters[0] + ': ', font=label_font)
            label.pack(side='left', fill='x')
            if request_name == 'slider':
                name, value, min_value, max_value, step = parameters
                scl = tk.Scale(frame, from_=min_value, to=max_value, resolution=step, font=widget_font,
                               orient=tk.HORIZONTAL, command=get_setter(self, name))
                scl.set(value)
                scl.pack(expand=True, fill='x')
                variables.append((request_name, name, scl))
            elif request_name == 'text':
                name, value = parameters
                entry = tk.Entry(frame, font=widget_font)
                entry.configure(validate='key', validatecommand=get_text_callback(self, name, entry))
                entry.insert(0, value)
                entry.pack(expand=True, fill='x')
                variables.append((request_name, name, entry))
            elif request_name == 'dropdown':
                name, value, options = parameters
                variable = tk.Variable(value=value, name=name)
                optionmenu = tk.OptionMenu(frame, variable, *options, command=get_setter(self, name))
                optionmenu.config(font=widget_font)
                frame.nametowidget(optionmenu.menuname).config(font=option_dropdown_font)
                optionmenu.pack(expand=True, fill='x')
                variables.append((request_name, name, optionmenu))
            elif request_name == 'boolean':
                name, value = parameters
                var = tk.BooleanVar(value=value)
                checkbutton = tk.Checkbutton(frame, text=name, variable=var, font=widget_font)
                checkbutton.configure(command=get_boolean_callback(self, name, var))
                checkbutton.pack(expand=True, fill='both')
                variables.append((request_name, name, checkbutton))
            frame.pack(expand=True, fill='x')

        def constant_checker():
            for request_name, variable_name, widget in variables:
                new_value = getattr(self, variable_name)
                if request_name == 'slider':
                    if new_value != widget.get():
                        widget.set(new_value)
                # elif request_name == 'text':
                #     if new_value != widget.get():
                #         widget.delete(0, len(widget.get()))
                #         widget.insert(0, new_value)
                # elif request_name == 'dropdown':
                #     if new_value != widget.get():
                #         widget.set(new_value)
                # elif request_name == 'boolean':
                #     if new_value != widget.get():
                #         widget.set(new_value)

            self.window.after(100, constant_checker)

        self.window.after(100, constant_checker)
        self.window.mainloop()

    def init_gui(self):
        threading.Thread(target=self.init_gui_thread, daemon=True).start()
