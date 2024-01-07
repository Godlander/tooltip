# Usage:

Make sure Python and Pillow are installed, and place the input tooltip texture file in the same directory as the script

### Script Inputs:

`file`: Path to an image file used for the tooltip

`corner`: Corner square side length in pixels

`pad`: Vertical and horizontal padding when displaying ingame

### Script Output:

The script will generate a file `tooltip.glsl` Which should replace the existing one in the resourcepack `shaders/include` Folder

# Examples:

### Green Tooltip

```
python tooltip.py --file green.png --corner 3 --pad 1 1
```

![image](https://github.com/Godlander/tooltip/assets/16228717/ee9c3878-1e77-4ac1-bb0c-5c16804c2a7f)

Ingame:

![image](https://github.com/Godlander/tooltip/assets/16228717/30d308cf-3846-42c4-b2e0-469da82ccb40)

### Gold Tooltip

Due to the decoration on the top and bottom of the tooltip, some extra vertical padding is necessary to make space
```
python tooltip.py --file gold.png --corner 7 --pad 1 3
```

![image](https://github.com/Godlander/tooltip/assets/16228717/aebc2c12-9123-404e-8aee-635b573927d0)

Ingame:

![image](https://github.com/Godlander/tooltip/assets/16228717/9e807257-6e80-4d5b-99f1-041cbc3a759e)

# Credits:
Shader and Tool Commissioned by MatchaXP
