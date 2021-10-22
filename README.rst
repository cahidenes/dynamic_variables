Dynamic Variables
=================

Change variables during runtime using simple GUI.

Installation
------------

::

    pip install dynamic_variables

Usage
-----

Here is a minimalist example

.. code:: python

    from dynamic_variables import VariableTweaker
    import time

    vt = VariableTweaker()
    vt.add_slider('var_name', 0, 0, 10, 0.1)
    vt.init_gui()

    while True:
        print(vt.var_name)
        time.sleep(0.1)

When this program run, a slider appears and ``vt.var_name`` changes
according to this slider.

.. figure:: https://github.com/cahidenes/visuals/blob/main/dynamic_variables1.png?raw=true
   :alt: Slider Window

Breakdown
~~~~~~~~~

``vt = VariableTweaker()`` creates an object of VariableTweaker class.
This object is used to create dynamic variables and gui.

``vt.add_slider`` creates a slider inside the gui and a float variable
named ``var_name``. This variable is connected with the slider and
changes with the slider, and can be used throughout the code. Slider is
one of 5 widgets. All widgets and their usage covered in widgets
section.

``vt.init_gui()`` Initializes the GUI.

Widgets
~~~~~~~

There are 5 widgets that you can add to GUI. They allow manipulating
different types of variables.

.. figure:: https://github.com/cahidenes/visuals/blob/main/dynamic_variables2.png?raw=true
   :alt: Slider Window

Slider
^^^^^^

Slider widget allows you to change ``int`` or ``float`` variables
easily.

.. code:: python

    add_slider(variable_name, initial_value, min_value, max_value, step_value)

Example:

.. code:: python

    vt.add_slider('slider', 5, 0, 10, 0.1)

Text
^^^^

Text widget allows you to change ``str`` variables.

.. code:: python

    add_text(variable_name, initial_value)

Example:

.. code:: python

    vt.add_text('text', 'this is a text')

Dropdown
^^^^^^^^

Dropdown widget allows you to change your variable to any predetermined
value.

.. code:: python

    add_dropdown(variable_name, initial_value, list_or_tuple_of_options)

Example:

.. code:: python

    vt.add_text('dropdown', 'option 1', ['option 1', 'option 2', 3, 4.5])

Boolean
^^^^^^^

Boolean widget allows you to change your ``bool`` variable

.. code:: python

    add_boolean(variable_name, initial_value)

Example:

.. code:: python

    vt.add_boolean('boolean', True)

Color
^^^^^

Color widget allows you to pick colors easily. When clicked on the
color, a color picker shows up for you to choose a color.

.. code:: python

    add_color(variable_name, initial_value)

initial\_value must be a tuple ``(r, g, b)`` or a colorcode ``#xxxxxx``.
Example:

.. code:: python

    vt.add_color('color1', (12, 63, 85))
    vt.add_color('color2', '#0c3f55')

When accessing the color variable, ``r``, ``g``, ``b`` and
``color_code`` parts are available.

.. code:: python

    print(vt.color.r, vt.color.color_code)

Button
^^^^^^

Button widget allows you to invoke functions manually.

.. code:: python

    add_button(button_name, function_to_invoke)

Example:

.. code:: python

    def print_hello():
        print('Hello!')

    vt.add_button('Print Hello', print_hello)

Example Application
-------------------

Please check the github page https://github.com/cahidenes/dynamic_variables for an example application.