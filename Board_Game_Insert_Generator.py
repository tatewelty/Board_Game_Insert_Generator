##TODO: input validation to make sure not negatives or 0 values.
##TODO: highlight cells that are 0
##TODO: put all functions in helper file
##TODO: Say how many shapes got generated
##TODO: say type and count of shapes generated
##TODO: add another packing algorithm
##TODO: how do 0 values work with packing algorithm
##TODO: add a way to visualize the 2d shape pack model
##TODO: log that 3d model was created
##TODO: display 3d model in app
##TODO: say stl succlssfully generated
##TODO: add a lot of error handling for shapes and stuff.


## imports
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
import json
from tkinter import filedialog
import math
from shapely.geometry import Polygon, Point
import json
from shapely.geometry import Polygon, Point
import numpy as np
import math
from shapely import affinity
import matplotlib.pyplot as plt
from shapely.geometry import box as shapely_box
import trimesh

##variable definitions

# allow for measurement unit conversion
measurement_unit_conversion = {
    "mm": 1,
    "cm": 10,
    "in": 25.4
}

old_unit = 'mm'



#allow for components to be added
component_rows = []
component_options = [
    'Rectangular Prism',
    'Cylinder',
    'Triangular Prism'
]

##function definitions
# input tab
def convert_value(value_str, from_unit, to_unit):
    """
    Convert numeric value from unit A to unit B:
    convert value to mm (base unit since conversion factor = 1)
    then convert to desired unit
    null value (starting value) will return 0.0
    """
    try:
        value=float(value_str)
        value_base_unit = value*measurement_unit_conversion[from_unit]
        converted_value = value_base_unit/measurement_unit_conversion[to_unit]
        return f"{converted_value:.6f}"
    except ValueError:
        return"0.0"
    
def measurement_unit_changed(*args):
    """
    changes the values within the app
    has old_unit stored
    Box Parameters
        goes through each _value (length, width, height)
            converts values, delete old value, insert new value
        changes the _measurement_unit to the new unit
    Components
        entries are row based for components
            converts values, delete old, innsert new
            use label config for the unit of measurement
    updates the old_unit to new_unit so process can be run again
    """
    global old_unit
    new_unit = selected_measurement_unit.get()

    #update main box values
    for entry in [length_value, width_value, height_value]:
        current_value = entry.get()
        new_value = convert_value(current_value, old_unit, new_unit)
        entry.delete(0, tk.END)
        entry.insert(0, new_value)
    length_value_measurement_unit.config(text=new_unit)
    width_value_measurement_unit.config(text=new_unit)
    height_value_measurement_unit.config(text=new_unit)

    #update component values
    for row in component_rows:
        for entry, unit_label in row["entries"]:
            current_value = entry.get()
            new_value=convert_value(current_value, old_unit, new_unit)
            entry.delete(0, tk.END)
            entry.insert(0, new_value)
            unit_label.config(text=new_unit)
    
    #update general parameters
    for entry, unit_label in [(distance_wall, distance_wall_measurement_unit),
                         (distance_cutout, distance_cutout_measurement_unit),
                         (component_tolerance, component_tolerance_measurement_unit)]:
        current_value = entry.get()
        new_value = convert_value(current_value, old_unit, new_unit)
        entry.delete(0, tk.END)
        entry.insert(0, new_value)
        unit_label.config(text=new_unit)

     #update old_unit       
    old_unit = new_unit

def numeric_input_validation(char):
    """
    Only allow numbers to be included
    . also included for decimals
    Will be used at keystroke level, so need to allow backspace/delete"""
    if char == '':
        return True
    try:
        float(char)
        return True
    except ValueError:
        return False
    
def add_component_row():
    """
    adds a new row at the bottom of the app
        row contains component type from dropdown
    """
    component_row_number = 9 + len(component_rows)
    row_frame = ttk.Frame(frame)
    row_frame.grid(row=component_row_number, column = 0, columnspan=7, sticky='w', pady=2)

    def delete_row():
        """
        deletes the row
        """
        row_frame.destroy()
        component_rows[:] = [r for r in component_rows if r["frame"]!= row_frame]
    
    #delete button col 0
    delete_button = ttk.Button(row_frame, text='🗑️', width=2, command=delete_row)   #🗑️
    delete_button.grid(row=0, column=0, padx=2)
    

    #dropdown col 1
    comp_type_var = tk.StringVar(value=component_options[0])
    component_dropdown=ttk.OptionMenu(row_frame, comp_type_var, comp_type_var.get(), *component_options)
    component_dropdown.grid(row=0, column=1, padx=2)

    entry_widgets=[]

    def update_component_inputs(*args):
        """
        updates the component row when a new component type selected
        trace from comp_type_var.trace_add for if a change to component type happened
            delete everything in the row
            get the value from the dropdown (triangular/rectangular prism, cylander)
                populate fields based on which component type was selected
                create within the app the fields and values

        """
        for widget in row_frame.grid_slaves():
            if int(widget.grid_info()['column'])>1: 
                widget.destroy()
        entry_widgets.clear()

        #get dropdown value
        selected = comp_type_var.get()
        inputs = []

        #dimensions for each dropdown value
        if selected == "Rectangular Prism":
            inputs=["Length", "Width", "Height"]
        elif selected == "Cylinder":
            inputs=["Radius", "Height"]
        elif selected == 'Triangular Prism':
            inputs=["Side 1", "Side 2", "Side 3", "Height"]
        
        #visually create inputs row wise.  i*3 works for adding more inputs (text, input, unit, text2, input2, unit2, etc...)
        for i, label in enumerate(inputs):
            #text displaying in app
            ttk.Label(row_frame, text=label + ":").grid(row=0, column=2 + i*3, padx=2)

            #add entry of text box
            entry = ttk.Entry(row_frame, width=15, validate = 'key', validatecommand=keystroke_registered)
            entry.grid(row=0, column=3 +i*3,padx=2)
            entry.insert(0,float(0))

            #add unit label
            unit_label = ttk.Label(row_frame, text=selected_measurement_unit.get())
            unit_label.grid(row=0, column=4+i*3, padx=2)
            entry_widgets.append((entry, unit_label))

    #callback for update_component_inputs
    comp_type_var.trace_add('write', update_component_inputs)
    update_component_inputs()
    #row number, component type, dimensions
    component_rows.append({"frame":row_frame, "var": comp_type_var, "entries": entry_widgets})

def collect_parameters():
    """
    collects all parameters
    was super useful when using json method, but less useful now
    """
    data = {}
    data['unit'] = selected_measurement_unit.get()

    data['constants'] = {
        'distance_to_wall': distance_wall.get(),
        'distance_between_cutouts': distance_cutout.get(),
        'component_tolerance': component_tolerance.get(),
        'circle_resolution': circle_resolution.get()
    }

    data['box']={
        'box_length':length_value.get(),
        'box_width':width_value.get(),
        'box_height':height_value.get()
    }

    components = []
    for row in component_rows:
        comp_type = row['var'].get()
        comp_data = {'type': comp_type}
        entries = row['entries']

        if comp_type == 'Rectangular Prism':
            labels = ['length', 'width', 'height']
        elif comp_type == 'Cylinder':
            labels = ['radius', 'height']
        elif comp_type == 'Triangular Prism':
            labels = ['side1', 'side2', 'side3', 'height']
        else:
            labels = []
        for label, (entry, _) in zip(labels, entries):
            comp_data[label] = entry.get()
        components.append(comp_data)
    data['components'] = components
    return data

#Generate insert tab
def create_2d_shape(params):
    """
    Generates 2d shapes based off parameters
    includes tolerance and circle resolution
    """
    # Extract parameters
    tol = float(params['constants']['component_tolerance'])
    res = int(params['constants']['circle_resolution'])
    components = params['components']

    # For example, generate shapes for all components and return as a list
    shapes = []

    for component in components:
        shape_type = component['type']

        if shape_type == 'Rectangular Prism':
            length = float(component['length']) + tol
            width = float(component['width']) + tol
            shape = Polygon([(0,0), (length,0), (length,width), (0,width)])

        elif shape_type == 'Cylinder':
            radius = float(component['radius']) + tol/2
            shape = Point(0,0).buffer(radius, resolution=res)

        elif shape_type == 'Triangular Prism':
            side1 = float(component['side1']) + tol
            side2 = float(component['side2']) + tol
            side3 = float(component['side3']) + tol
            A = (0, 0)
            B = (side1, 0)
            # Calculate angle at A using law of cosines
            cos_angle = (side1**2 + side3**2 - side2**2) / (2 * side1 * side3)
            cos_angle = max(-1, min(1, cos_angle))
            angle = math.acos(cos_angle)
            C = (side3 * math.cos(angle), side3 * math.sin(angle))
            shape = Polygon([A, B, C])

        else:
            raise ValueError(f"Unknown component type: {shape_type}")

        shapes.append(shape)
    if (len(components) == len(shapes)):
        generate_2d_text_helper.set(f"SUCCESS: Total shapes created: {len(shapes)}")
    else:
        generate_2d_text_helper.set(f"FAIL: Please check your Components in Input Parameters tab")
    return shapes

def pack_shapes(shapes, components, box_length, box_width, spacing_to_wall, spacing_to_component):
    """
    grab dimensions of polygons made in create_2d_shape
    make sure at least spacing_to_wall away from all walls
    make sure at least spacing_to_component away from other components
    place those shapes in 2d plane bounded by box dimensions
    """
    placed_shapes = []

    for shape, comp in zip(shapes, components):
        shape_bounds = shape.bounds
        shape_length = shape_bounds[2] - shape_bounds[0]
        shape_width = shape_bounds[3] - shape_bounds[1]

        found_position = False
        y = spacing_to_wall
        while y + shape_width <= box_width - spacing_to_wall:
            x = spacing_to_wall
            while x + shape_length <= box_length - spacing_to_wall:
                # Align shape to (x, y)
                candidate = affinity.translate(shape, xoff=x - shape_bounds[0], yoff=y - shape_bounds[1])
                ##add spacing to component as a buffer
                buffered_candidate = candidate.buffer(spacing_to_component / 2.0)

                ## if not overlapping then place the shape
                if all(not buffered_candidate.intersects(other[0]) for other in placed_shapes):
                    placed_shapes.append((candidate,comp))
                    found_position = True
                    break
                x += 1
            if found_position:
                break
            y += 1

        if not found_position:
            print("Shape couldn't be placed")

    if (len(placed_shapes)==len(shapes)):
        pack_shapes_text_helper.set(f'SUCCESS: Packed {len(placed_shapes)} of {len(shapes)} shapes in 2d space')
    else:
        pack_shapes_text_helper.set(f'FAIL: Only packed {len(placed_shapes)} of {len(shapes)} shapes in 2d space.  Check non height parameters')
    return placed_shapes

def shapely_to_trimseh(shape, height):
    """
    convert 2d shape to 3d extrusion
    """
    if shape.geom_type !='Polygon':
        raise ValueError("Only polygons can be extruded.  not {shape.geom_type}")
    return trimesh.creation.extrude_polygon(shape, height)

def generate_insert(box_length, box_width, box_height, placed_shapes):
    """
    generate the 3d box
    extrude the 3d components from locations they are packed
    generates the final insert
    """
    box_mesh = trimesh.creation.box((box_length, box_width, box_height))
    box_mesh.apply_translation((box_length/2, box_width/2, box_height/2))  ## set corner not center to origin
    cutouts = []
    #each component extrude by its height
    for shape, comp in placed_shapes:
        component_height = float(comp.get('height'))
        cutout = shapely_to_trimseh(shape, height=component_height)
        cutouts.append(cutout)
    all_cutouts = trimesh.util.concatenate(cutouts)
    final_insert = box_mesh.difference(all_cutouts)
    generate_3d_text_helper.set('SUCCESS: Generated 3d model from 2d')
    return final_insert

def output_stl(file):
    """
    save output as stl file
    opens file explorer for selection
    """
    
    file_path = filedialog.asksaveasfilename(
        defaultextension='.stl',
        filetypes=[('STL files', '*.stl'), ('All files', '*.*')],
        title='Save Board Game Insert STL',
        initialfile='board_game_insert.stl'
    )
    if file_path:
        with open(file_path, 'w') as f:
            file.export(file_path)
        print(f"parameters saved to {file_path}")
        export_model_text_helper.set(f'Generated .stl in desired location.  Make sure you inport to 3d software with correct units: {selected_measurement_unit.get()}')

##create the gui
#overall app and title
root = tk.Tk()
root.title("Board Game Insert Generator")

#allow for multiple tabs
style = ttk.Style()
style.configure("TNotebook.Tab", font=('TkDefaultFont', 20, 'bold'))
notebook = ttk. Notebook(root)
notebook.pack(padx=10, pady=10, fill='both', expand=True)

#make an input tab
input_tab = ttk.Frame(notebook)
notebook.add(input_tab, text = "Input Parameters")
frame = ttk.Frame(input_tab)
frame.pack(padx=10, pady=10)

# generate tab
generate_tab = ttk.Frame(notebook)
notebook.add(generate_tab, text='Generate Insert')
generate_frame = ttk.Frame(generate_tab)
generate_frame.pack(padx=10, pady=10)

#add keystroke within gui
keystroke_registered = (root.register(numeric_input_validation), '%P')

# for section text.  Larger, bold, and underlined
section_font = tkfont.Font(family='TkDefaultFont', size=12, weight='bold', underline=1)

#setting default unit of measurement.  mm because conversion factor of 1
selected_measurement_unit = tk.StringVar(value='mm')
generate_2d_text_helper = tk.StringVar()
generate_2d_text_helper.set('Not yet ran')
pack_shapes_text_helper = tk.StringVar()
pack_shapes_text_helper.set('run Generate 2D Shapes before this')
generate_3d_text_helper = tk.StringVar()
generate_3d_text_helper.set('run Pack 2D Shapes before this')
export_model_text_helper = tk.StringVar()
export_model_text_helper.set('run 3D Model before this')

#callback for measurement_unit_changed
selected_measurement_unit.trace_add('write', measurement_unit_changed)

## SECTION: General Parameters
## row 0-4
ttk.Label(frame, text="General Parameters:", font=section_font).grid(row=0, column=0, sticky='w')

#change unit of measurement
ttk.Label(frame, text="Units:").grid(row=1, column=0, sticky='w')
unit_menu=ttk.OptionMenu(frame, selected_measurement_unit, selected_measurement_unit.get(), 'mm', 'cm', 'in')
unit_menu.grid(row=1, column=1, sticky='w')

##Minimum distance to a wall
ttk.Label(frame, text='Min Distance To Box Wall:').grid(row=2, column=0, sticky='w')
distance_wall = ttk.Entry(frame, width = 15, validate = 'key', validatecommand=keystroke_registered)
distance_wall.grid(row=2, column=1, sticky='w')
distance_wall.insert(0,float(5))
distance_wall_measurement_unit = ttk.Label(frame, text=selected_measurement_unit.get())
distance_wall_measurement_unit.grid(row=2, column=2, sticky='w')

##Minimum distance between cutouts
ttk.Label(frame, text='Min Distance Between Cutouts:').grid(row=2, column=3, sticky='w')
distance_cutout = ttk.Entry(frame, width = 15, validate = 'key', validatecommand=keystroke_registered)
distance_cutout.grid(row=2, column=4, sticky='w')
distance_cutout.insert(0,float(3))
distance_cutout_measurement_unit = ttk.Label(frame, text=selected_measurement_unit.get())
distance_cutout_measurement_unit.grid(row=2, column=5, sticky='w')

##Minimum distance between cutouts
ttk.Label(frame, text='Additional Component Buffer:').grid(row=3, column=0, sticky='w')
component_tolerance = ttk.Entry(frame, width = 15, validate = 'key', validatecommand=keystroke_registered)
component_tolerance.grid(row=3, column=1, sticky='w')
component_tolerance.insert(0,float(1.5))
component_tolerance_measurement_unit = ttk.Label(frame, text=selected_measurement_unit.get())
component_tolerance_measurement_unit.grid(row=3, column=2, sticky='w')

##Minimum distance between cutouts
ttk.Label(frame, text='Circle Resolution (bigger better):').grid(row=3, column=3, sticky='w')
circle_resolution = ttk.Entry(frame, width = 15, validate = 'key', validatecommand=keystroke_registered)
circle_resolution.grid(row=3, column=4, sticky='w')
circle_resolution.insert(0,int(64))


## SECTION: Box Parameters
## row5-6
ttk.Label(frame, text="Box Parameters:", font=section_font).grid(row=5, column=0, sticky='w')

# Box Length variable
# text displaying in app 'Box Length'
ttk.Label(frame, text='Box Length:').grid(row=6, column=0, sticky='w')

#add an entry of text box
length_value = ttk.Entry(frame, width=15, validate="key", validatecommand=keystroke_registered)
length_value.grid(row=6, column=1, sticky='w')
length_value.insert(0,float(1))

#add the unit displaying in app '{unit}'
length_value_measurement_unit = ttk.Label(frame, text=selected_measurement_unit.get())
length_value_measurement_unit.grid(row=6, column=2, sticky='w')

# Box Width variable
#text displaying in app 'Box Width'
ttk.Label(frame, text='Box Width:').grid(row=6, column=3, sticky='w')

#add an entry of text box
width_value=ttk.Entry(frame, width=15, validate="key", validatecommand=keystroke_registered)
width_value.grid(row=6, column=4, sticky='w')
width_value.insert(0,float(1))

#add the unit displaying in app '{unit}'
width_value_measurement_unit = ttk.Label(frame, text=selected_measurement_unit.get())
width_value_measurement_unit.grid(row=6, column = 5, sticky='w')

#Box Height variable
#text displaying in app 'Box Height'
ttk.Label(frame, text='Box Height:').grid(row=6, column=6, sticky='w')

#add an entry of text box
height_value=ttk.Entry(frame, width=15, validate="key", validatecommand=keystroke_registered)
height_value.grid(row=6, column=7, sticky='w')
height_value.insert(0,float(1))

#add the unit displaying in app '{unit}'
height_value_measurement_unit = ttk.Label(frame, text=selected_measurement_unit.get())
height_value_measurement_unit.grid(row=6, column=8, sticky = 'w')

## SECTION: Components
ttk.Label(frame, text="Components:", font=section_font).grid(row=7, column=0, sticky='w')

#add button for making a new component
add_button = ttk.Button(frame, text='Add Component', command=add_component_row)
add_button.grid(row=8, column=0, sticky='w', pady=10)

##TAB Generate Insert
generate_2d_button = ttk.Button(generate_frame, text="Generate 2D Shapes", command=lambda: create_2d_shape(collect_parameters()))
generate_2d_button.grid(row=1, column=0, pady=10, sticky='w')
generate_2d_text = ttk.Label(generate_frame, textvariable=generate_2d_text_helper)
generate_2d_text.grid(row=1, column = 1, sticky='w')


pack_shapes_button = ttk.Button(
    generate_frame,
    text="Pack 2D Shapes",
    command=lambda: pack_shapes(
        create_2d_shape(collect_parameters()),
        collect_parameters()['components'],
        float(length_value.get()),
        float(width_value.get()),
        float(distance_wall.get()),
        float(distance_cutout.get()))
)
pack_shapes_button.grid(row=2, column=0, pady=10, sticky='w')
pack_shapes_text = ttk.Label(generate_frame, textvariable=pack_shapes_text_helper)
pack_shapes_text.grid(row=2, column = 1, sticky='w')

generate_3d_button = ttk.Button(generate_frame, text="3D Model", command=lambda: generate_insert(
    float(length_value.get()),
    float(width_value.get()),
    float(height_value.get()),
    pack_shapes(
        create_2d_shape(collect_parameters()),
        collect_parameters()['components'],
        float(length_value.get()),
        float(width_value.get()),
        float(distance_wall.get()),
        float(distance_cutout.get()))
))
generate_3d_button.grid(row=3, column=0, pady=10, sticky='w')
generate_3d_text = ttk.Label(generate_frame, textvariable=generate_3d_text_helper)
generate_3d_text.grid(row=3, column = 1, sticky='w')

export_model_button = ttk.Button(generate_frame, text="Generate STL", command=lambda: output_stl(
    generate_insert(
    float(length_value.get()),
    float(width_value.get()),
    float(height_value.get()),
    pack_shapes(
        create_2d_shape(collect_parameters()),
        collect_parameters()['components'],
        float(length_value.get()),
        float(width_value.get()),
        float(distance_wall.get()),
        float(distance_cutout.get()))
)
))
export_model_button.grid(row=4, column=0, pady=10, sticky='w')
export_model_text = ttk.Label(generate_frame, textvariable=export_model_text_helper)
export_model_text.grid(row=4, column = 1, sticky='w')

root.mainloop()