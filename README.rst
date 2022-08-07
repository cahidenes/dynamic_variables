Dynamic Variables
=================

Change variables during runtime using simple GUI. ## Installation

::

   pip3 install dynamic_variables

Usage
-----

Here is a minimalist example

.. code:: python

   import dynamic_variables as dv
   import time

   dv.add_slider('var_name', 0, 10)
   dv.init_gui()

   while True:
       print(var_name)
       time.sleep(0.1)

When this program run, a slider appears and ``vt.var_name`` changes
according to this slider.

.. figure:: https://github.com/cahidenes/visuals/blob/main/dynamic_variables2.0_1.png?raw=true
   :alt: Slider Window

Breakdown
~~~~~~~~~

``dv.add_slider`` creates a slider inside the gui and a float variable
named ``var_name``. This variable is connected with the slider and
changes with the slider, and can be used throughout the code. Slider is
one of 6 widgets. All widgets and their usage covered in widgets
section.

``dv.init_gui()`` Initializes the GUI.

Widgets
~~~~~~~

There are 6 widgets that you can add to GUI. They allow manipulating
different types of variables.

.. figure:: https://github.com/cahidenes/visuals/blob/main/dynamic_variables2.0_2.png?raw=true
   :alt: All Widgets

   All Widgets

(dark theme with dark-blue color)

Slider
~~~~~~

Slider widget allows you to change ``int`` or ``float`` variables
easily.

.. code:: python

   add_slider(variable_name, min_value, max_value[, value[, step]])

Example:

.. code:: python

   dv.add_slider('slider', 0, 10, value=5, step=1)

If all values are ``int``, the variable will be an ``int``. Otherwise,
it will be a ``float``.

Text
~~~~

Text widget allows you to change ``str`` variables.

.. code:: python

   add_text(variable_name[, value])

Example:

.. code:: python

   dv.add_text('text', value='this is a text')

Dropdown
^^^^^^^^

Dropdown widget allows you to change your variable to any predetermined
value.

.. code:: python

   add_dropdown(variable_name, list_or_tuple_of_options[, chosen_index])

Example:

.. code:: python

   dv.add_text('dropdown', ['option 1', 'option 2', 3, 4.5], chosen_index=0)

Boolean
~~~~~~~

Boolean widget allows you to change your ``bool`` variable

.. code:: python

   add_boolean(variable_name[, value])

Example:

.. code:: python

   dv.add_boolean('boolean', value=True)

Color
~~~~~

Color widget allows you to pick colors easily. When clicked on the
color, a color picker shows up for you to choose a color.

.. code:: python

   add_color(variable_name[, value])

initial_value must be a tuple ``(r, g, b)`` or a colorcode ``#xxxxxx``.
Example:

.. code:: python

   dv.add_color('color', value=(12, 63, 85))
   dv.add_color('color2', value='#0c3f55')
   ...

When accessing the color variable, ``r``, ``g``, ``b``, ``color_code``
and ``tuple`` parts are available.

.. code:: python

   print(color.r, color.g, color.b, color.color_code, color.tuple)

Button
~~~~~~

Button widget allows you to invoke functions manually.

.. code:: python

   add_button(button_name, function_to_invoke)

Example:

.. code:: python

   def print_hello():
       print('Hello!')

   dv.add_button('Print Hello', print_hello)

Init GUI
~~~~~~~~

To initialize the GUI, call ``dv.init_gui()``. You can feed in some
optional arguments in here:
- window_title: Title of the window. Default is ``Variable Tweaker``.

- font_size: Font size of the labels. Default is ``16``.

- widget_font_size: Font size of the widgets. Default is ``font_size*0.75``.

- default_width: Initial width of the window in pixels (window is resizable). Default is ``500``.

- theme: Theme of the GUI. Options are ``light``, ``dark`` and ``native``. Default is ``dark``.

- color: Color of the theme. Not used when theme is ``native``. Options are ``blue``, ``dark-blue``, ``green``, ``sweetkind``. Default is ``dark-blue``

.. code:: python

   dv.init_gui(window_title='VT', font_size=20, widget_font_size=16, default_width=1000, theme='dark', color='sweetkind')

.. figure:: https://github.com/cahidenes/visuals/blob/main/dynamic_variables2.0_3.png?raw=true
   :alt: Theme Example

   (light theme with green color)



.. figure:: https://github.com/cahidenes/visuals/blob/main/dynamic_variables2.0_4.png?raw=true
   :alt: Theme Example

   (native theme)



Saved Variables
~~~~~~~~~~~~~~~

Dynamic Variables saves all the variables inside system config file.
After closing and reopening the app, your variables are restored (unless
you specify with ``value=...``). This process is unique to every file
(same variable in different files considered different).

Init GUI arguments are also saved. If you use light theme once, the next
theme (unless you specify) will be light.

Example Application
-------------------

.. code:: python

   import cv2 as cv
   import dynamic_variables as dv

   def save_image():
       print('image saved')

   # Set up dynamic variables
   dv.add_boolean('colored')
   dv.add_text('text')
   dv.add_slider('x', 0, 100)
   dv.add_slider('y', 0, 100)
   dv.add_color('color')
   dv.add_dropdown('threshold_type', ['None', 'Normal', 'Adaptive Gaussian', 'Adaptive Mean'])
   dv.add_slider('thresh', 0, 255)
   dv.add_slider('block_size', 3, 201, step=2)
   dv.add_slider('C', -100, 100)
   dv.add_button('Save Image', save_image)
   dv.init_gui()

   # import image
   image = cv.imread('image.png')

   while cv.waitKey(20) != ord('q'):

       copy = image.copy()

       # colored
       if not colored:
           copy = cv.cvtColor(copy, cv.COLOR_BGR2GRAY)

       # Apply Threshold
       if threshold_type == 'Normal':
           _, copy = cv.threshold(copy, thresh, 255, cv.THRESH_BINARY)
       elif threshold_type == 'Adaptive Gaussian':
           copy = cv.adaptiveThreshold(copy, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, block_size, C)
       elif threshold_type == 'Adaptive Mean':
           copy = cv.adaptiveThreshold(copy, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, block_size, C)
       if not colored:
           copy = cv.cvtColor(copy, cv.COLOR_GRAY2BGR)

       # Put text
       copy = cv.putText(copy, text, (x, y), cv.FONT_HERSHEY_SIMPLEX, 3, (color.b, color.g, color.r), 3)

       # Show image
       cv.imshow('Image', copy)

.. figure:: https://github.com/cahidenes/visuals/blob/main/dynamic_variables2.0.gif?raw=true
   :alt: Slider Window

   Slider Window
