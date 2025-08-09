import detectron2.utils.comm as comm
from detectron2.engine.hooks import HookBase
import torch
import numpy as np
import os

class TopologyEvalHook(HookBase):
    def __init__(self, eval_period, model, data_loader, output_dir, topology_metric_func):
        """
        Args:
            eval_period (int): How often to run the evaluation (in iterations).
            model (torch.nn.Module): The trained model.
            data_loader (iterable): Data loader for evaluation dataset.
            output_dir (str): Directory to save evaluation outputs.
            topology_metric_func (callable): Function that takes predictions and targets
                and returns a dict of topology metrics.
        """
        self._period = eval_period
        self._model = model
        self._data_loader = data_loader
        self._output_dir = output_dir
        self._topology_metric_func = topology_metric_func

    def after_step(self):
        next_iter = self.trainer.iter + 1
        if next_iter % self._period == 0 or next_iter == self.trainer.max_iter:
            self._run_topology_evaluation()

    def _run_topology_evaluation(self):
        self._model.eval()
        all_metrics = []
        for inputs in self._data_loader:
            with torch.no_grad():
                outputs = self._model(inputs)
            # You must define how to extract predictions and targets from inputs/outputs
            metrics = self._topology_metric_func(inputs, outputs)
            all_metrics.append(metrics)
        
        # Aggregate metrics
        agg_metrics = self._aggregate_metrics(all_metrics)

        # Log metrics
        comm.synchronize()
        if comm.is_main_process():
            print(f"Topology evaluation metrics at iteration {self.trainer.iter}:")
            for k, v in agg_metrics.items():
                print(f"  {k}: {v:.4f}")

    def _aggregate_metrics(self, metrics_list):
        # Average all metrics across batches
        agg = {}
        if not metrics_list:
            return agg
        keys = metrics_list[0].keys()
        for key in keys:
            values = [m[key] for m in metrics_list if key in m]
            agg[key] = float(np.mean(values)) if values else 0.0
        return agg
