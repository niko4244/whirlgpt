# Whirly Detectron2 Training Pipeline

This repository contains tools and scripts to train a Mask2Former model on vector-based circuit diagrams using Detectron2.

---
# Whirly Detectron2 Training Repo

This repository provides a complete pipeline for training and evaluating instance segmentation models tailored for circuit diagram analysis with Whirly.

---

## Features

- **Dataset Conversion Utilities**  
  Scripts to convert SVG- and annotation-based datasets into COCO format compatible with Detectron2.

- **Mask2Former Configurations**  
  Ready-to-use Detectron2 config files customized for schematic component segmentation.

- **Topology Evaluation Harness**  
  Evaluation metrics that go beyond mask IoU, incorporating domain-specific topology correctness validation.

---

## Repo Structure


## Contents

- `pdf_to_png.py`  
  Convert PDF circuit diagrams to PNG images.

- `pdf_to_svg.sh`  
  Bash script to convert PDF pages to SVG files with `pdf2svg`.

- `extract_svg_paths.py`  
  Extract SVG path data into JSON annotations.

- `vector_to_mask.py`  
  Rasterize SVG vector paths into binary masks for training.

- `mask2former_custom_loader.py`  
  Custom Detectron2 dataset loader that converts SVG paths to polygons.

- `mask2former_circuit_config.py`  
  Detectron2 config file for training Mask2Former on circuit diagrams.

- `train_circuit.py`  
  Training script using the custom loader and config.

- `topology_eval_hook.py`  
  Custom Detectron2 hook to compute topology metrics during evaluation.

- `preprocess_dataset.py`  
  Automates dataset preprocessing and mask generation from vector annotations.

- `topology_metrics.py`  
  Template for defining custom topology metric calculations.

---

## Setup

1. **Install dependencies:**

```bash
pip install detectron2 fvcore iopath pycocotools svgpathtools cairocffi pillow tqdm
