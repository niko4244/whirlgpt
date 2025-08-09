import os
from detectron2.engine import DefaultTrainer
from detectron2.utils.logger import setup_logger
from detectron2.data import MetadataCatalog, DatasetCatalog
from mask2former_custom_loader import load_circuit_dataset  # your loader code file
from mask2former_circuit_config import get_cfg_circuit

# Map your labels here (must match your dataset)
LABEL_MAP = {"wire": 0, "resistor": 1, "capacitor": 2}

def register_dataset(json_dir):
    DatasetCatalog.register("circuit_vector_train", lambda: load_circuit_dataset(json_dir, LABEL_MAP))
    MetadataCatalog.get("circuit_vector_train").set(thing_classes=list(LABEL_MAP.keys()))

class Trainer(DefaultTrainer):
    @classmethod
    def build_evaluator(cls, cfg, dataset_name, output_folder=None):
        # Use default COCO evaluator or implement custom if needed
        from detectron2.evaluation import COCOEvaluator
        if output_folder is None:
            output_folder = os.path.join(cfg.OUTPUT_DIR, "eval")
        return COCOEvaluator(dataset_name, cfg, False, output_folder)

def main():
    json_dir = "/path/to/your/json_annotations"
    register_dataset(json_dir)

    cfg = get_cfg_circuit(num_classes=len(LABEL_MAP))
    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)

    trainer = Trainer(cfg)
    trainer.resume_or_load(resume=False)
    trainer.train()

if __name__ == "__main__":
    setup_logger()
    main()
