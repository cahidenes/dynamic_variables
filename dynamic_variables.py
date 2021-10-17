import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from tkinter import colorchooser
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


def get_boolean_callback(obj, name, var, radiobutton):
    def callback():
        setattr(obj, name, var.get())
        radiobutton.config(text=('True' if var.get() else 'False'))
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

    def add_color(self, name, value):
        self.create_requests.append(('color', (name, value)))

    def init_gui_thread(self, window_name='Variable Tweaker', label_font_size=16, widget_font_size=12):
        for request_name, parameters in self.create_requests:
            setattr(self, parameters[0], parameters[1])

        self.window = tk.Tk()
        self.window.title(window_name)
        label_font = tkfont.Font(family='Helvetica', size=label_font_size, weight='bold')
        widget_font = tkfont.Font(family='Helvetica', size=widget_font_size)
        variables = []
        for request_name, parameters in self.create_requests:
            frame = tk.Frame(self.window, bd=4, relief=tk.FLAT)
            label = tk.Label(frame, text=parameters[0] + ': ', font=label_font)
            label.pack(side='left', fill='x', padx=5, pady=5)
            if request_name == 'slider':
                name, value, min_value, max_value, step = parameters
                scl = tk.Scale(frame, from_=min_value, to=max_value, resolution=step, font=widget_font,
                               orient=tk.HORIZONTAL, command=get_setter(self, name))
                scl.set(value)
                scl.pack(expand=True, fill='x')
                variables.append((request_name, name, scl))
            elif request_name == 'text':
                name, value = parameters
                entry = tk.Entry(frame, font=widget_font, justify='center')
                entry.configure(validate='key', validatecommand=get_text_callback(self, name, entry))
                entry.insert(0, value)
                entry.pack(expand=True, fill='x')
                variables.append((request_name, name, entry))
            elif request_name == 'dropdown':
                name, value, options = parameters
                variable = tk.Variable(value=value, name=name)
                optionmenu = tk.OptionMenu(frame, variable, *options, command=get_setter(self, name))
                optionmenu.config(font=widget_font)
                frame.nametowidget(optionmenu.menuname).config(font=widget_font)
                optionmenu.pack(expand=True, fill='x')
                variables.append((request_name, name, optionmenu))
            elif request_name == 'boolean':
                name, value = parameters
                var = tk.BooleanVar(value=value)
                checkbutton = tk.Checkbutton(frame, text=('True' if value else 'False'),
                                             variable=var, font=widget_font, indicatoron=False)
                checkbutton.configure(command=get_boolean_callback(self, name, var, checkbutton))
                checkbutton.pack(expand=True, fill='both')
                variables.append((request_name, name, checkbutton))
            elif request_name == 'color':
                name, value = parameters
                color = Color(value)
                print(color.colorcode, color.r, color.b, color.g)

                def color_callback():
                    color.set(colorchooser.askcolor(color=color.colorcode, title='Choose Color')[0])
                    button.config(bg=color.colorcode, activebackground=color.__highlight_color__())

                button = tk.Button(frame, bg=color.colorcode, activebackground=color.__highlight_color__(),
                                   command=color_callback)
                button.pack(expand=True, fill='both')

            frame.pack(expand=True, fill='x', padx=3, pady=3)
            ttk.Separator(self.window, orient='horizontal').pack(fill='x')

        # def constant_checker():
        #     self.window.after(100, constant_checker)
        #
        # self.window.after(100, constant_checker)

        self.window.mainloop()

    def init_gui(self):
        threading.Thread(target=self.init_gui_thread, daemon=True).start()


class Color:
    def __init__(self, value):
        self.r, self.g, self.b, self.colorcode = 0, 0, 0, '#000000'
        self.set(value)

    def set(self, value=(0, 0, 0)):
        if isinstance(value, str):
            value = value.replace('#', '')
            a = int(value, 16)
            self.b = a & 0xff
            self.g = (a >> 8) & 0xff
            self.r = (a >> 16) & 0xff
            self.colorcode = '#' + value
        elif isinstance(value, tuple):
            self.r, self.g, self.b = value
            self.colorcode = '#{:06x}'.format((self.r << 16) | (self.g << 8) | self.b)
        else:
            print(type(value))

    def __highlight_color__(self):
        return '#{:06x}'.format((min(self.r + 20, 255) << 16) | ((min(self.g + 20, 255) << 8) | min(self.b + 20, 255)))
