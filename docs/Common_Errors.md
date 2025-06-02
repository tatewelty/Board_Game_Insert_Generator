# Common Errors and Debugging

## Generate 2D Shapes
Desired outcome: `SUCCESS: Total shapes created: X`
1) double check the values of 2d elements of your components: `Length`, `Width`, `Side 1`, `Side2`, `Side3`
2) Ensure that triangle dimensions can make a triangle:
    - `1`, `2`, `3123` does not make a real triangle

## Pack 2D Shapes
Desired outcome: `SUCCESS: Packed X of X shapes in 2d space`
1) double check the values of 2d elements of your components: `Length`, `Width`, `Side 1`, `Side2`, `Side3`
2) set your `Min Distance To Box Wall:`, `Min Distance Between Cutouts:`, `Additional Component Buffer:` values to 0
    - After success you can then start increasing those values 
3) try removing shapes and putting them in with the largest area piece first 

## 3D Model
1) Check the height value of your box
2) Check the height value of each component.
    - Values greater than box height will be full extrusions.

## Generate STL
1) make sure to save the file from the popup
    - It defauls to STL files as the type
