from svgpathtools import svg2paths2
import json
import os

def extract_paths_from_svg(svg_path):
    """
    Extract vector paths and their attributes from an SVG file.

    Args:
        svg_path (str): Path to the SVG file.

    Returns:
        List[Dict]: List of paths with their d-attributes and styles.
    """
    paths, attributes, svg_attr = svg2paths2(svg_path)
    extracted = []
    for path, attr in zip(paths, attributes):
        path_info = {
            "d": path.d(),  # SVG path data string
            "stroke": attr.get("stroke", None),
            "fill": attr.get("fill", None),
            "id": attr.get("id", None),
            "class": attr.get("class", None)
        }
        extracted.append(path_info)
    return extracted

def save_paths_json(paths_data, output_json_path):
    with open(output_json_path, "w") as f:
        json.dump(paths_data, f, indent=2)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract vector paths from SVG")
    parser.add_argument("svg_path", type=str, help="Input SVG file path")
    parser.add_argument("output_json", type=str, help="Output JSON file path")
    args = parser.parse_args()

    paths_data = extract_paths_from_svg(args.svg_path)
    save_paths_json(paths_data, args.output_json)
    print(f"Extracted {len(paths_data)} paths from {args.svg_path} and saved to {args.output_json}")
