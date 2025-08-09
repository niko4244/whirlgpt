import os
import json
from svgpathtools import parse_path
from shapely.geometry import Polygon, MultiPolygon
from detectron2.structures import BoxMode

def svg_path_to_polygons(svg_path_str):
    """
    Converts an SVG path string to a list of polygons (lists of x,y floats)
    suitable for Detectron2 segmentation.

    Args:
        svg_path_str (str): SVG path data string.

    Returns:
        List[List[float]]: List of polygon coordinates flattened [x1,y1,x2,y2,...].
    """
    path = parse_path(svg_path_str)

    # Sample points along the path
    sampled_points = []
    for segment in path:
        # Sample 20 points per segment
        for t in [i/20 for i in range(21)]:
            pt = segment.point(t)
            sampled_points.append((pt.real, pt.imag))

    # Close polygon if needed
    if sampled_points[0] != sampled_points[-1]:
        sampled_points.append(sampled_points[0])

    polygon = Polygon(sampled_points)
    if not polygon.is_valid:
        polygon = polygon.buffer(0)

    if polygon.is_empty:
        return []

    # Handle MultiPolygon by flattening
    polygons = []
    if isinstance(polygon, MultiPolygon):
        for poly in polygon.geoms:
            exterior_coords = list(poly.exterior.coords)
            flat_coords = [coord for point in exterior_coords for coord in point]
            polygons.append(flat_coords)
    else:
        exterior_coords = list(polygon.exterior.coords)
        flat_coords = [coord for point in exterior_coords for coord in point]
        polygons.append(flat_coords)

    return polygons

def load_circuit_dataset(json_dir, label_map):
    """
    Load circuit dataset annotations from JSON files.

    Args:
        json_dir (str): Directory containing annotation JSON files.
        label_map (dict): Mapping from label strings to category IDs.

    Returns:
        List[dict]: Detectron2 dataset dicts.
    """
    dataset_dicts = []
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

    for idx, json_file in enumerate(json_files):
        json_path = os.path.join(json_dir, json_file)
        with open(json_path, 'r') as f:
            anno = json.load(f)

        record = {}
        record["file_name"] = anno["image_path"]
        record["image_id"] = idx
        record["height"] = anno["height"]
        record["width"] = anno["width"]

        objs = []
        for obj in anno.get("annotations", []):
            label = obj["label"]
            svg_path_str = obj["svg_path"]
            category_id = label_map.get(label)
            if category_id is None:
                continue

            polygons = svg_path_to_polygons(svg_path_str)
            if not polygons:
                continue

            # Compute bounding box from polygons
            all_x = [pt for poly in polygons for idx, pt in enumerate(poly) if idx % 2 == 0]
            all_y = [pt for poly in polygons for idx, pt in enumerate(poly) if idx % 2 == 1]
            xmin, xmax = min(all_x), max(all_x)
            ymin, ymax = min(all_y), max(all_y)
            bbox = [xmin, ymin, xmax, ymax]

            obj_record = {
                "bbox": bbox,
                "bbox_mode": BoxMode.XYXY_ABS,
                "segmentation": polygons,
                "category_id": category_id,
            }
            objs.append(obj_record)

        record["annotations"] = objs
        dataset_dicts.append(record)

    return dataset_dicts
