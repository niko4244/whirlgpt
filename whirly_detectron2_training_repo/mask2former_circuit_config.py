from detectron2.config import get_cfg
from detectron2 import model_zoo

def get_cfg_circuit(num_classes):
    cfg = get_cfg()
    # Load a base Mask2Former config (panoptic segmentation)
    cfg.merge_from_file(model_zoo.get_config_file("COCO-PanopticSegmentation/maskformer_R50_bs16_50ep.yaml"))

    # Dataset
    cfg.DATASETS.TRAIN = ("circuit_vector_train",)
    cfg.DATASETS.TEST = ()

    # Number of classes
    cfg.MODEL.SEM_SEG_HEAD.NUM_CLASSES = num_classes
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = num_classes

    # Output directory
    cfg.OUTPUT_DIR = "./output_circuit"

    # Solver params
    cfg.SOLVER.MAX_ITER = 20000  # adjust as needed
    cfg.SOLVER.BASE_LR = 0.0001
    cfg.SOLVER.WARMUP_ITERS = 1000
    cfg.SOLVER.STEPS = []  # no LR decay for simplicity

    # Mixed precision
    cfg.SOLVER.AMP.ENABLED = True

    # Batch size (adjust for your GPU memory)
    cfg.SOLVER.IMS_PER_BATCH = 4

    # Use multi-gpu if available
    cfg.DATALOADER.NUM_WORKERS = 4

    return cfg
