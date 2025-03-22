# Stenciled

`stenciled.py` is a Python script for converting images (PNG, GIF, or JPG) into posterized SVG files suitable for vinyl cutting.

## Usage

### 1. Using `stenciled.py` from the Command Line

The `stenciled.py` script can be executed directly from the command line.

#### Command Syntax

```bash
python stenciled.py <input_image> <output_svg> [--colors COLORS] [--simplify SIMPLIFY]
```

#### Arguments

- `<input_image>`: Path to the input image file (PNG, GIF, or JPG).
- `<output_svg>`: Path to save the output SVG file.
- `--colors`: (Optional) Number of colors for posterization. Default is `2`.
- `--simplify`: (Optional) Simplification tolerance as a factor of contour arc length. Default is `0.01`.

#### Example Usage

1. Convert an image with default settings:

   ```bash
   python stenciled.py input.png output.svg
   ```

2. Convert an image with 4 colors and higher contour simplification:

   ```bash
   python stenciled.py input.jpg output.svg --colors 4 --simplify 0.05
   ```

3. Convert a GIF file (uses the first frame only):
   ```bash
   python stenciled.py animation.gif output.svg
   ```

---

### 2. Using `stenciled.py` as a Module

You can also import `stenciled.py` into your Python scripts to use its functions programmatically.

#### Available Functions

- `posterize_image(img, colors)`: Posterizes an image to a specified number of colors.
- `get_unique_colors(paletted_img)`: Extracts unique color indices from a posterized image.
- `create_mask(paletted_img, index)`: Creates a binary mask for a specific color index.
- `trace_mask(mask, simplify)`: Traces and simplifies contours in a binary mask.
- `convert_to_svg(input_path, output_path, colors=8, simplify=0.01)`: Converts an image file to a posterized SVG.

#### Example Usage

```python
from PIL import Image
from stenciled import posterize_image, get_unique_colors, create_mask, trace_mask, convert_to_svg

# Load an image
img = Image.open("input.png")

# Posterize the image to 4 colors
posterized_img = posterize_image(img, 4)

# Get unique color indices
unique_colors = get_unique_colors(posterized_img)

# Create a binary mask for the first color
mask = create_mask(posterized_img, unique_colors[0])

# Trace and simplify contours
contours = trace_mask(mask, 0.01)

# Convert the image to an SVG file
convert_to_svg("input.png", "output.svg", colors=4, simplify=0.01)
```

#### Use Case

This approach is useful if you want to integrate `stenciled.py` into a larger Python project or customize its behavior.
