import argparse
from PIL import Image
import numpy as np
import cv2
import svgwrite


def posterize_image(img, colors):
    """Posterize the image to a specified number of colors."""
    img = img.convert('RGB')  # Ensure the image is in RGB mode
    return img.convert('P', palette=Image.ADAPTIVE, colors=colors)


def get_unique_colors(paletted_img):
    """Get unique color indices from the paletted image."""
    img_array = np.array(paletted_img)
    unique_indices = np.unique(img_array)
    # Exclude background index if present
    return unique_indices[unique_indices != 0]


def create_mask(paletted_img, index):
    """Create a binary mask for a specific color index."""
    img_array = np.array(paletted_img)
    mask = (img_array == index).astype(np.uint8) * 255
    return mask


def trace_mask(mask, simplify):
    """Trace contours in the mask and simplify them."""
    # Updated for OpenCV 4.x compatibility
    contours, _ = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    simplified_contours = []
    for contour in contours:
        epsilon = simplify * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        simplified_contours.append(approx)
    return simplified_contours


def contours_to_svg_paths(contours, color):
    """Convert contours to SVG path elements."""
    path_data = ""
    for contour in contours:
        points = contour.squeeze().tolist()
        if len(points) > 0:
            path_data += f"M {points[0][0]} {points[0][1]} "
            for p in points[1:]:
                path_data += f"L {p[0]} {p[1]} "
            path_data += "Z "
    return svgwrite.path.Path(d=path_data, fill=color, stroke="none", fill_rule="evenodd")


def convert_to_svg(input_path, output_path, colors=8, simplify=0.01):
    """Convert an image file (PNG, GIF, JPG) to a posterized SVG file."""
    # Load the image
    img = Image.open(input_path)

    # Handle GIF (use first frame only) and convert to RGB
    if img.format == 'GIF':
        # Ensure no transparency issues
        img = img.convert('RGBA').convert('RGB')
    else:
        img = img.convert('RGB')  # Convert JPG/PNG to RGB

    # Posterize the image
    paletted_img = posterize_image(img, colors)
    palette = paletted_img.getpalette()

    # Ensure the palette is not None
    if palette is None:
        raise ValueError(
            "Palette is missing. Ensure the image is in 'P' mode.")

    unique_indices = get_unique_colors(paletted_img)

    # Create SVG drawing with the same size as the input image
    dwg = svgwrite.Drawing(output_path, profile='tiny', size=img.size)

    # Process each unique color
    for index in unique_indices:
        # Create binary mask for this color
        mask = create_mask(paletted_img, index)

        # Trace and simplify contours
        contours = trace_mask(mask, simplify)

        # Get the RGB color from the palette and convert to hex
        color_rgb = palette[index * 3:index * 3 + 3]
        color_hex = f"#{color_rgb[0]:02x}{color_rgb[1]:02x}{color_rgb[2]:02x}"

        # Convert contours to SVG path and add to drawing
        path = contours_to_svg_paths(contours, color_hex)
        dwg.add(path)

    # Save the SVG file
    dwg.save()


if __name__ == "__main__":
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(
        description="Convert PNG, GIF, or JPG to posterized SVG for vinyl cutting")
    parser.add_argument("input", help="Input image file path (PNG, GIF, JPG)")
    parser.add_argument("output", help="Output SVG file path")
    parser.add_argument("--colors", type=int, default=8,
                        help="Number of colors for posterization (default: 8)")
    parser.add_argument("--simplify", type=float, default=0.01,
                        help="Simplification tolerance as a factor of contour arc length (default: 0.01)")
    args = parser.parse_args()

    # List of supported formats
    supported_formats = ['PNG', 'GIF', 'JPEG']

    # Check if input format is supported
    img = Image.open(args.input)
    if img.format not in supported_formats:
        print(
            f"Error: Unsupported input format '{img.format}'. Supported formats: {', '.join(supported_formats)}")
        exit(1)

    # Run the conversion
    convert_to_svg(args.input, args.output, args.colors, args.simplify)
