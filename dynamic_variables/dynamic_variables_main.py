import os.path
import tkinter as tk
import tkinter.font as tk_font
from tkinter import ttk
from tkinter import colorchooser
import threading
import re
import inspect
import sys
import appdirs
import atexit
import base64
import csv
from ast import literal_eval
import customtkinter as ctk
import math


window_name = 'Variable Tweaker'
window = None
create_requests = []
imported_modules = []
defaults = {}


def get_slider_callback(name, value_label, type, precision):
    def slider_callback(scale_value):
        scale_value = type(scale_value)
        mysetattr(name, scale_value)

        if value_label is not None:
            if type is float:
                value_label.configure(text=f'{scale_value:.{precision}f}')
            else:
                value_label.configure(text=f'{scale_value}')
    return slider_callback


def get_option_callback(name):
    def option_callback(value):
        mysetattr(name, value)
    return option_callback


def get_text_callback(name, entry):
    def callback():
        window.after(10, lambda: mysetattr(name, entry.get()))
        return True
    return callback


def get_boolean_callback(name, var, radiobutton):
    def callback():
        try:
            radiobutton.config(text=('True' if var.get() else 'False'))
            mysetattr(name, var.get())
        except:
            val = radiobutton.get() == 1
            mysetattr(name, val)
            var.set(val)
    return callback


def get_color_callback(name, color, button):
    def color_callback():
        color.set(colorchooser.askcolor(color=color.color_code, title='Choose Color')[0])
        mysetattr(name, color)
        try:
            button.config(bg=color.color_code, activebackground=color.__highlight_color__())
        except:
            button.configure(fg_color=color.color_code, hover_color=color.__highlight_color__())
    return color_callback


def add_slider(name, min_value, max_value, value=None, step=None):

    if step is None:
        if isinstance(max_value, float) or isinstance(min_value, float) or max_value - min_value < 10.1:
            step = 10**(int(math.log10((max_value - min_value)/100)))
        else:
            step = int(1)

    tip = float if isinstance(min_value, float) or isinstance(max_value, float) or \
            (value is not None and isinstance(value, float)) or (step is not None and isinstance(step, float)) else int

    if value is None:
        try:
            value = int(defaults[name])
        except:
            try:
                value = float(defaults[name])
            except:
                pass
        if value is not None and not (min_value <= value <= max_value):
            value = None
    type_error = 'must be int or float, not'
    if not isinstance(name, str):
        raise TypeError(f'name must be str, not {name.__class__.__name__}')
    if value is not None and not isinstance(value, int) and not isinstance(value, float):
        raise TypeError(f'value {type_error} {value.__class__.__name__}')
    if not isinstance(min_value, int) and not isinstance(min_value, float):
        raise TypeError(f'min_value {type_error} {min_value.__class__.__name__}')
    if not isinstance(max_value, int) and not isinstance(max_value, float):
        raise TypeError(f'max_value {type_error} {max_value.__class__.__name__}')
    if step is not None and not isinstance(step, int) and not isinstance(step, float):
        raise TypeError(f'step {type_error} {step.__class__.__name__}')
    if min_value >= max_value:
        raise ValueError(f'min_value is not less than max_value: {min_value} < {max_value} not holds')
    if value is not None and not (min_value <= value <= max_value):
        raise ValueError(f'value must be between min and max values: {min_value} <= {value} <= {max_value} not holds')

    if value is None:
        value = tip((max_value + min_value)/2)

    __init_imported_modules()
    if isinstance(min_value, float) or isinstance(max_value, float) or isinstance(step, float):
        value = float(value)
    mysetattr(name, value)
    try:
        n = int(f'{step:e}'.split('-')[1])
    except Exception as e:
        n = 0
    create_requests.append(('slider', (name, value, min_value, max_value, step, tip, n)))


def add_text(name, value=None):
    if value is None:
        try:
            value = defaults[name]
        except:
            value = ''

    if not isinstance(name, str):
        raise TypeError(f'name must be str, not {name.__class__.__name__}')
    if not isinstance(value, str):
        raise TypeError(f'value must be str, not {value.__class__.__name__}')
    __init_imported_modules()
    mysetattr(name, value)
    create_requests.append(('text', (name, value)))


def add_dropdown(name, options, chosen_index=None):
    if chosen_index is None:
        try:
            chosen_index = int(defaults[name])
            if not (0 <= chosen_index < len(options)):
                chosen_index = 0
        except:
            chosen_index = 0
    if not isinstance(name, str):
        raise TypeError(f'name must be str, not {name.__class__.__name__}')
    if not isinstance(options, list) and not isinstance(options, tuple):
        raise TypeError(f'options must be list or tuple, not {options.__class__.__name__}')
    if not isinstance(chosen_index, int):
        raise TypeError(f'chosen_index must be int, not {chosen_index.__class__.__name__}')
    if not (0 <= chosen_index < len(options)):
        raise ValueError(f'chosen_index must be between 0 and {len(options)-1}')
    __init_imported_modules()
    mysetattr(name, options[chosen_index])
    create_requests.append(('dropdown', (name, chosen_index, options)))


def add_boolean(name, value=None):
    if value is None:
        try:
            value = literal_eval(defaults[name])
        except Exception as e:
            value = True
    if not isinstance(name, str):
        raise TypeError(f'name must be str, not {name.__class__.__name__}')
    if not isinstance(value, bool):
        raise TypeError(f'value must be bool, not {name.__class__.__name__}')
    __init_imported_modules()
    mysetattr(name, value)
    create_requests.append(('boolean', (name, value)))


def add_color(name, value=None):
    if value is None:
        try:
            value = literal_eval(defaults[name])
        except Exception as e:
            value = (0, 0, 0)
    if not isinstance(name, str):
        raise TypeError(f'name must be str, not {name.__class__.__name__}')
    if isinstance(value, str):
        if not re.match('#[1234567890abcdefABCDEF]{6}', value):
            raise ValueError('value must be in #XXXXXX format')
    else:
        try:
            r, g, b = value
            if not isinstance(r, int) or not isinstance(g, int) or not isinstance(b, int):
                raise TypeError('r, g and b must be integers')
            if not (0 <= r <= 255, 0 <= g <= 255, 0 <= b <= 255):
                raise ValueError('r, g, and b must be in range of [0, 255]')
        except ValueError:
            raise ValueError('value must be (r, g, b) or #XXXXXX color format')
    __init_imported_modules()
    mysetattr(name, Color(value))
    create_requests.append(('color', (name, value)))


def add_button(name, function):
    if not isinstance(name, str):
        raise TypeError(f'name must be str, not {name.__class__.__name__}')
    if not inspect.isfunction(function):
        raise TypeError(f'function must be function, not {name.__class__.__name__}')
    params = inspect.signature(function).parameters
    for param in params:
        if params[param].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD and \
                params[param].default == inspect.Parameter.empty:
            raise ValueError(f'function "{function.__name__}" must not have any positional '
                             f'argument without a default value, but there is "{param}"')
    __init_imported_modules()
    create_requests.append(('button', (name, function)))


def __init_imported_modules():
    global imported_modules
    if not imported_modules:
        this_module = sys.modules['dynamic_variables']
        modules = list(sys.modules.values())
        for module in modules:
            for module_attribute in dir(module):
                if getattr(module, module_attribute) is this_module:
                    imported_modules.append(module)


def mysetattr(name, value):
    for module in imported_modules:
        setattr(module, name, value)


def __init_gui_thread__(window_title, font_size, widget_font_size, default_width, use_native_gui, theme, color_theme):

    ctk.set_appearance_mode(theme)
    ctk.set_default_color_theme(color_theme)

    global window
    if use_native_gui:
        window = tk.Tk()
    else:
        window = ctk.CTk()
    window.title(window_title)
    label_font = tk_font.Font(family='Roboto', size=font_size, weight='bold')
    widget_font = tk_font.Font(family='Roboto', size=widget_font_size)
    variables = []
    for request_name, parameters in create_requests:
        if use_native_gui:
            frame = tk.Frame(window, bd=4, relief=tk.FLAT)
        else:
            frame = ctk.CTkFrame(window)
        if request_name != 'button':
            if use_native_gui:
                label = tk.Label(frame, text=parameters[0] + ': ', font=label_font)
            else:
                label = ctk.CTkLabel(frame, text=parameters[0] + ': ', text_font=tk_font.Font(family='Roboto', size=font_size, weight='bold'))
            label.pack(side='left', fill='x', padx=5, pady=5)
        if request_name == 'slider':
            name, value, min_value, max_value, step, tip, precision = parameters
            if use_native_gui:
                scl = tk.Scale(frame, from_=min_value, to=max_value, resolution=step, font=widget_font,
                               orient=tk.HORIZONTAL, command=get_slider_callback(name, None, tip, 0))
            else:
                value_label = ctk.CTkLabel(frame, text=f'{value:.{precision}f}', text_font=('Helvetica', widget_font_size), width=30+widget_font_size*len(str(max_value)))
                value_label.pack(side='left')
                scl = ctk.CTkSlider(frame, from_=min_value, to=max_value, number_of_steps=math.ceil((max_value - min_value)/step),
                               orient=tk.HORIZONTAL, command=get_slider_callback(name, value_label, tip, precision))
            scl.set(value)
            scl.pack(expand=True, fill='x', padx=5)
            variables.append((request_name, name, scl))
        elif request_name == 'text':
            name, value = parameters
            if use_native_gui:
                entry = tk.Entry(frame, font=widget_font, justify='center')
            else:
                entry = ctk.CTkEntry(frame, text_font=widget_font, justify='center')
            entry.configure(validate='key', validatecommand=get_text_callback(name, entry))
            entry.insert(0, value)
            entry.pack(expand=True, fill='x', padx=5)
            variables.append((request_name, name, entry))
        elif request_name == 'dropdown':
            name, chosen_index, options = parameters
            variable = tk.Variable(value=options[chosen_index], name=name)
            if use_native_gui:
                option_menu = tk.OptionMenu(frame, variable, *options, command=get_option_callback(name))
                option_menu.config(font=widget_font)
                frame.nametowidget(option_menu.menuname).config(font=widget_font)
            else:
                option_menu = ctk.CTkOptionMenu(master=frame, values=options, variable=variable, command=get_option_callback(name), text_font=('Helvetica', widget_font_size))
            option_menu.pack(expand=True, fill='x', padx=5)
            variables.append((request_name, name, option_menu))
        elif request_name == 'boolean':
            name, value = parameters
            var = ctk.BooleanVar(value=value)
            if use_native_gui:
                checkbutton = tk.Checkbutton(frame, text=('True' if value else 'False'),
                                             variable=var, font=widget_font, indicatoron=False)
            else:
                checkbutton = ctk.CTkSwitch(frame, variable=var, text='', borderwidth=10)
                if value:
                    checkbutton.select()
                else:
                    checkbutton.deselect()

            checkbutton.configure(command=get_boolean_callback(name, var, checkbutton))
            checkbutton.pack(expand=True, fill='both', padx=5, pady=5)
            variables.append((request_name, name, checkbutton))
        elif request_name == 'color':
            name, value = parameters
            color = Color(value)
            if use_native_gui:
                button = tk.Button(frame, bg=color.color_code, activebackground=color.__highlight_color__())
                button.config(command=get_color_callback(name, color, button))
            else:
                button = ctk.CTkButton(frame, fg_color=color.color_code, hover_color=color.__highlight_color__(),
                                       text='', corner_radius=10)
                button.configure(command=get_color_callback(name, color, button))
            button.pack(expand=True, fill='both', padx=5, pady=5)
        elif request_name == 'button':
            name, function = parameters
            if use_native_gui:
                button = tk.Button(frame, command=function, text=name, font=widget_font)
            else:
                button = ctk.CTkButton(frame, command=function, text=name, text_font=('Roboto', font_size), corner_radius=10)
            button.pack(expand=True, fill='both')

        frame.pack(expand=True, fill='both', padx=5, pady=3)
        if use_native_gui:
            ttk.Separator(window, orient='horizontal').pack(fill='x')

    window.geometry(f'{default_width}x{len(create_requests) * int(font_size*1.6 + 40)}')
    window.protocol('WM_DELETE_WINDOW', lambda: (window.destroy(), window.quit()))
    window.mainloop()


def init_gui(window_title='Variable Tweaker', font_size=None, widget_font_size=None, default_width=None, theme=None, color=None):
    if font_size is None:
        try:
            font_size = int(default_args['font_size'])
        except:
            font_size=16
    if widget_font_size is None:
        try:
            widget_font_size = int(default_args['widget_font_size'])
        except:
            widget_font_size = int(font_size*0.75)
    if default_width is None:
        try:
            default_width = int(default_args['default_width'])
        except:
            default_width=500
    if theme is None:
        try:
            theme = default_args['theme']
        except:
            theme = 'dark'
    if color is None:
        try:
            color = default_args['color']
        except Exception as e:
            color = 'dark-blue'

    if theme not in ['dark', 'light', 'native']:
        raise ValueError('theme should be dark, light or native')
    if color not in ['blue', 'dark-blue', 'green', 'sweetkind']:
        raise ValueError('color should be blue, dark-blue, green or sweetkind')

    with open(args_dir, 'w', newline='') as file:
        writer = csv.writer(file)
        if font_size is not None:
            writer.writerow(['font_size', font_size])
        if widget_font_size is not None:
            writer.writerow(['widget_font_size', widget_font_size])
        if default_width is not None:
            writer.writerow(['default_width', default_width])
        if theme is not None:
            writer.writerow(['theme', theme])
        if color is not None:
            writer.writerow(['color', color])

    threading.Thread(target=__init_gui_thread__, daemon=True, args=(window_title, font_size, widget_font_size,
                    default_width, theme=='native', theme, color)).start()

def myHash(text: str):
    hash = 0
    for ch in text:
        hash = (hash * 281 ^ ord(ch) * 997) & 0xFFFFFFFFFFFFFFFF
    return hash

def exit_handler():
    if imported_modules:
        module = imported_modules[0]
        with open(file_dir, 'w', newline='') as file:
            writer = csv.writer(file)
            for type, values in create_requests:
                if type == 'dropdown':
                    writer.writerow([values[0]] + [values[2].index(getattr(module, values[0]))])
                elif type != 'button':
                    writer.writerow([values[0]] + [getattr(module, values[0])])


class Color:
    def __init__(self, value):
        self.r, self.g, self.b, self.color_code = 0, 0, 0, '#000000'
        self.tuple = (self.r, self.g, self.b)
        self.set(value)

    def __str__(self):
        return f'({self.r}, {self.g}, {self.b})'

    def set(self, value=(0, 0, 0)):
        if isinstance(value, str):
            value = value.replace('#', '')
            a = int(value, 16)
            self.b = a & 0xff
            self.g = (a >> 8) & 0xff
            self.r = (a >> 16) & 0xff
            self.color_code = '#' + value
            self.tuple = (self.r, self.g, self.b)
        elif isinstance(value, tuple):
            self.tuple = value
            self.r, self.g, self.b = value
            self.color_code = '#{:06x}'.format((self.r << 16) | (self.g << 8) | self.b)

    def __highlight_color__(self):
        return '#{:06x}'.format((min(self.r + 20, 255) << 16) | ((min(self.g + 20, 255) << 8) | min(self.b + 20, 255)))

atexit.register(exit_handler)

config_dir = appdirs.user_config_dir('dynamic_variables')
if not os.path.exists(config_dir):
    os.makedirs(config_dir)

hash = base64.b64encode((myHash(sys.argv[0]) % ((sys.maxsize + 1) * 2)).to_bytes(9, 'big'), altchars=b'_-').decode()
file_dir = config_dir + '/' + hash
if os.path.exists(file_dir):
    with open(file_dir, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            defaults[row[0]] = row[1]


default_args = {}
args_dir = config_dir + '/' + 'args'
if os.path.exists(args_dir):
    with open(args_dir, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            default_args[row[0]] = row[1]



