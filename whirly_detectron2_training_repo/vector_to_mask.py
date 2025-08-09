import cairocffi as cairo  # or use pycairo if installed
from svgpathtools import parse_path
from shapely.geometry import Polygon, MultiPolygon
from PIL import Image
import numpy as np

def svg_path_to_shapely(svg_path_str):
    """
    Convert an SVG path string to a Shapely geometry (Polygon or LineString).
    This example handles only simple closed paths as polygons.
    """
    path = parse_path(svg_path_str)
    points = []

    for segment in path:
        # Sample points from each segment
        for t in np.linspace(0, 1, num=20):
            pt = segment.point(t)
            points.append((pt.real, pt.imag))

    # Close polygon if needed
    if points[0] != points[-1]:
        points.append(points[0])

    polygon = Polygon(points)
    if not polygon.is_valid:
        polygon = polygon.buffer(0)  # fix minor issues
    return polygon

def draw_mask_from_geometries(geometries, img_size=(1024, 1024), scale=1.0, translate=(0,0)):
    """
    Rasterize Shapely geometries to a binary mask image using Cairo.

    Args:
        geometries (List[shapely.geometry]): List of Polygon or MultiPolygon geometries.
        img_size (tuple): (width, height) of output mask image.
        scale (float): scale factor to apply to coordinates.
        translate (tuple): (x_offset, y_offset) translation applied after scaling.

    Returns:
        np.ndarray: Binary mask array (uint8), 255 inside geometries, 0 outside.
    """
    width, height = img_size
    surface = cairo.ImageSurface(cairo.FORMAT_A8, width, height)
    ctx = cairo.Context(surface)

    # Black background
    ctx.set_source_rgb(0, 0, 0)
    ctx.paint()

    # White fill for geometries
    ctx.set_source_rgb(1, 1, 1)

    for geom in geometries:
        if geom.is_empty:
            continue
        if isinstance(geom, Polygon):
            polygons = [geom]
        elif isinstance(geom, MultiPolygon):
            polygons = geom.geoms
        else:
            continue

        for poly in polygons:
            exterior_coords = [(scale * x + translate[0], scale * y + translate[1]) for x, y in poly.exterior.coords]
            ctx.move_to(*exterior_coords[0])
            for x, y in exterior_coords[1:]:
                ctx.line_to(x, y)
            ctx.close_path()

            for interior in poly.interiors:
                interior_coords = [(scale * x + translate[0], scale * y + translate[1]) for x, y in interior.coords]
                ctx.move_to(*interior_coords[0])
                for x, y in interior_coords[1:]:
                    ctx.line_to(x, y)
                ctx.close_path()

            ctx.fill_preserve()
            ctx.new_path()

    # Convert to numpy array
    buf = surface.get_data()
    mask = np.frombuffer(buf, np.uint8).reshape((height, width))

    return mask

# Example usage
if __name__ == "__main__":
    # Example SVG path string (a simple rectangle)
    example_svg_path = "M10 10 H 90 V 90 H 10 Z"

    polygon = svg_path_to_shapely(example_svg_path)

    # Scale polygon to fit image size (example: scale coords by 1)
    mask = draw_mask_from_geometries([polygon], img_size=(100, 100), scale=1.0)

    # Save mask to PNG
    mask_img = Image.fromarray(mask)
    mask_img.save("example_mask.png")
    print("Mask saved as example_mask.png")
