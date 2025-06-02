# Board Game Insert Generator

### Problem:
Many board games don't come with inserts or a clean way to store components.  You're often forced to use bags and rubber bands which is messy and can damage components.
To make this worse, expansions are sold in separate boxes, and their components rarely fit into the base game box.  This means you need to carry multiple boxes to play the game.

### Solution:
This program allows you to generate 3D-printable .stl files for custom inserts that organize and store your components in a single box.  Including base game and expansion components.

<table>
  <tr>
    <td>Before</td>
    <td>After</td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/61890de9-cd34-441f-ac88-44b7c11563b8"></td>
    <td><img src="https://github.com/user-attachments/assets/8ef5a63b-5f54-4a06-9fab-277c18ad0084"></td>
  </tr>
</table>

## How it works

### Part 1: Define Inputs

Start by describing your game box and the components you would like to store.  
For a complete list of parameters and their uses, please check out the [data dictionary:](docs/data_dictionary.md)
- **Units**: choose between millimeters, centimeters, or inches.  All values will be converted to your chosen unit.
- **Global Parameters**
  - **Additional Component Buffer**: extra space added to all sides of each component to ensure a good fit
  - **Min Distance Between Cutouts**: distance you want between each component in the insert
- **Box Parameters**: the size of your box.  No buffer or anything else is added to these dimensions.
- **Components**: The shapes of what you would like to store in the insert.
  - **Rectangular Prism**
  - **Cylindar**
  - **Triangular Prism**
> **Tip**: For odd-shaped items like hex tiles or miniatures, use a rectangular prism that encloses the shape.  This will leave space in corners, making it easier to take the component out.

![image](https://github.com/user-attachments/assets/32b3890e-0c78-4c77-9fe2-d743a9aa5eed)

### Part 2: Generate the Insert
If you run in to any issues in the section check out [Common Errors and Debugging](docs/Common_Errors.md)  
Once you have defined your components, the program will:
1. **Generate 2D Shapes**: Each component is flatteded to its 2D shape
2. **Pack 2D Shapes**: A *lower-left greedy* packing algorithm places components into the box making a full 2D footprint
3. **3D Model**: The 2D layout is converted into a 3D model by extruding each component based on its height
4. **Generate STL**: Generates the final insert as a .stl file

![image](https://github.com/user-attachments/assets/ef96c4c6-7b9b-4483-8c39-0c58edd2ac49)  
After that you'll have saved a .stl file, and will be able to import and print it.
>**Tip**: Make sure to import using the same units as your .stl was generated with

