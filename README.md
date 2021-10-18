# Dynamic Variables
Change variables during runtime using simple GUI.
## Installation
    pip install dynamic_variables
## Usage
Here is a minimalist example

    from dynamic_variables import VariableTweaker
    import time
    
    vt = VariableTweaker()
    vt.add_slider('var_name', 0, 0, 10, 0.1)
    vt.init_gui()

    while True:
        print(vt.var_name)
        time.sleep(0.1)

When this program run, a slider appears and `vt.var_name` changes according to this slider.

![Slider Window](https://github.com/cahidenes/visuals/blob/main/dynamic_variables1.png?raw=true)

### Breakdown
`vt = VariableTweaker()` creates an object of VariableTweaker class. This object is used to create dynamic variables and gui.

`vt.add_slider` creates a slider inside the gui and a float variable named `var_name`.
This variable is connected with the slider and changes with the slider, and can be used throughout the code.
Slider is one of 5 widgets. All widgets and their usage covered in widgets section.

`vt.init_gui()` Initializes the GUI.

### Widgets

There are 5 widgets that you can add to GUI. They allow manipulating different types of variables.

![Slider Window]( https://github.com/cahidenes/visuals/blob/main/dynamic_variables2.png?raw=true )

#### Slider
Slider widget allows you to change `int` or `float` variables easily.

    add_slider(variable_name, initial_value, min_value, max_value, step_value)

Example:
    
    vt.add_slider('slider', 5, 0, 10, 0.1)

#### Text
Text widget allows you to change `str` variables.

    add_text(variable_name, initial_value)

Example:
    
    vt.add_text('text', 'this is a text')

#### Dropdown
Dropdown widget allows you to change your variable to any predetermined value.

    add_dropdown(variable_name, initial_value, list_or_tuple_of_options)

Example:

    vt.add_text('dropdown, 'option 1', ['option 1', 'option 2', 'option 3'])

#### Boolean
Boolean widget allows you to change your `bool` variable

    add_boolean(variable_name, initial_value)

Example:

    vt.add_boolean('boolean', True)

#### Color
Color widget allows you to pick colors easily. When clicked on the color, a color picker
shows up for you to choose a color.

    add_color(variable_name, initial_value)

initial_value must be a tuple `(r, g, b)` or a colorcode `#xxxxxx`. Example:

    vt.add_color('color1', (12, 63, 85))
    vt.add_color('color2', '#0c3f55')

When accessing the color variable, `r`, `g`, `b` and `color_code` parts are available.

    print(vt.color.r, vt.color.color_code)

## Example Application

    import cv2 as cv
    from dynamic_variables import VariableTweaker

    # Set up dynamic variables
    vt = VariableTweaker()
    vt.add_text('text', 'Threshold')
    vt.add_slider('x', 0, 0, 100, 1)
    vt.add_slider('y', 0, 0, 100, 1)
    vt.add_slider('scale', 1, 1, 5, 0.01)
    vt.add_slider('thickness', 1, 1, 10, 1)
    vt.add_color('color', (0, 0, 0))
    vt.add_dropdown('threshold_type', 'None', ['None', 'Normal', 'Adaptive Gaussian', 'Adaptive Mean'])
    vt.add_slider('thresh', 100, 0, 255, 1)
    vt.add_slider('block_size', 3, 3, 201, 2)
    vt.add_slider('C', 0, -100, 100, 1)
    vt.init_gui()

    # import image
    image = cv.imread('image.png')

    while cv.waitKey(20) != ord('q'):

        # Apply Threshold
        copy = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        if vt.threshold_type == 'Normal':
            _, copy = cv.threshold(copy, vt.thresh, 255, cv.THRESH_BINARY)
        elif vt.threshold_type == 'Adaptive Gaussian':
            copy = cv.adaptiveThreshold(copy, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, vt.block_size, vt.C)
        elif vt.threshold_type == 'Adaptive Mean':
            copy = cv.adaptiveThreshold(copy, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, vt.block_size, vt.C)
        copy = cv.cvtColor(copy, cv.COLOR_GRAY2BGR)

        # Put text
        copy = cv.putText(copy, vt.text, (vt.x, vt.y), cv.FONT_HERSHEY_SIMPLEX, vt.scale,
                          (vt.color.b, vt.color.g, vt.color.r), vt.thickness)

        # Show image
        cv.imshow('Image', copy)


![Slider Window](https://github.com/cahidenes/visuals/blob/main/demo.gif?raw=true)
