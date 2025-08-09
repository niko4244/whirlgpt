import os
import json
from vector_to_mask import svg_path_to_shapely, draw_mask_from_geometries
from PIL import Image
from tqdm import tqdm

def preprocess_svg_annotations(svg_json_dir, image_dir, output_json_dir, output_mask_dir, img_size=(1024, 1024)):
    """
    Args:
        svg_json_dir (str): Folder with JSON files containing svg paths + labels.
        image_dir (str): Folder containing source images.
        output_json_dir (str): Folder to save Detectron2-style JSON annotations.
        output_mask_dir (str): Folder to save rasterized mask PNG files.
        img_size (tuple): Size to rasterize masks.
    """
    os.makedirs(output_json_dir, exist_ok=True)
    os.makedirs(output_mask_dir, exist_ok=True)

    json_files = [f for f in os.listdir(svg_json_dir) if f.endswith(".json")]
    for json_file in tqdm(json_files):
        json_path = os.path.join(svg_json_dir, json_file)
        with open(json_path, "r") as f:
            data = json.load(f)

        image_path = data["image_path"]
        image_name = os.path.basename(image_path)
        base_name = os.path.splitext(image_name)[0]

        record = {
            "file_name": image_path,
            "image_id": base_name,
            "height": data["height"],
            "width": data["width"],
            "annotations": []
        }

        for idx, obj in enumerate(data["annotations"]):
            label = obj["label"]
            svg_path_str = obj["svg_path"]

            polygon = svg_path_to_shapely(svg_path_str)
            if polygon.is_empty:
                continue

            # Rasterize mask for this object
            mask = draw_mask_from_geometries([polygon], img_size=img_size)

            mask_filename = f"{base_name}_mask_{idx}.png"
            mask_path = os.path.join(output_mask_dir, mask_filename)
            Image.fromarray(mask).save(mask_path)

            # Save annotation referencing the mask file
            record["annotations"].append({
                "label": label,
                "mask_path": mask_path,
            })

        out_json_path = os.path.join(output_json_dir, f"{base_name}.json")
        with open(out_json_path, "w") as f:
            json.dump(record, f, indent=2)
