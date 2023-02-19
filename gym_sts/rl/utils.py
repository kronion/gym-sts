import enum
import os
import typing as tp
import urllib
from multiprocessing import Queue

from gym import spaces
from ray import logger
from ray._private.storage import _load_class
from ray.air.integrations.wandb import (
    WANDB_PROCESS_RUN_INFO_HOOK,
    WandbLoggerCallback,
    _clean_log,
    _QueueItem,
    _WandbLoggingProcess,
)
from ray.tune.experiment import Trial


def assert_contains(space: spaces.Space, element: tp.Any):
    """Use with post-mortem debugging to see where in the space the error is."""
    if isinstance(space, spaces.Dict):
        assert isinstance(element, tp.Mapping)

        for key, subspace in space.items():
            assert_contains(subspace, element[key])
    assert space.contains(element)


class _CustomQueueItem(enum.Enum):
    FILE = enum.auto()


class _CustomWandbLoggingProcess(_WandbLoggingProcess):
    def __init__(
        self,
        logdir: str,
        queue: Queue,
        exclude: tp.List[str],
        to_config: tp.List[str],
        *args,
        save_base_path: tp.Optional[str] = None,
        **kwargs,
    ):
        super().__init__(logdir, queue, exclude, to_config, *args, **kwargs)
        self.save_base_path = save_base_path

    def run(self):
        # Since we're running in a separate process already, use threads.
        os.environ["WANDB_START_METHOD"] = "thread"
        run = self._wandb.init(*self.args, **self.kwargs)
        run.config.trial_log_path = self._logdir

        # Run external hook to process information about wandb run
        if WANDB_PROCESS_RUN_INFO_HOOK in os.environ:
            try:
                _load_class(os.environ[WANDB_PROCESS_RUN_INFO_HOOK])(run)
            except Exception as e:
                logger.exception(
                    f"Error calling {WANDB_PROCESS_RUN_INFO_HOOK}: {e}", exc_info=e
                )

        while True:
            item_type, item_content = self.queue.get()
            if item_type == _QueueItem.END:
                break

            if item_type == _QueueItem.CHECKPOINT:
                self._handle_checkpoint(item_content)
                continue

            if item_type == _CustomQueueItem.FILE:
                self._handle_file_save(item_content)
                continue

            assert item_type == _QueueItem.RESULT
            log, config_update = self._handle_result(item_content)
            try:
                self._wandb.config.update(config_update, allow_val_change=True)
                self._wandb.log(log)
            except urllib.error.HTTPError as e:
                # Ignore HTTPError. Missing a few data points is not a
                # big issue, as long as things eventually recover.
                logger.warn("Failed to log result to w&b: {}".format(str(e)))
        self._wandb.finish()

    def _handle_file_save(self, file_path: str):
        self._wandb.save(file_path, base_path=self.save_base_path)


class CustomWandbLoggerCallback(WandbLoggerCallback):
    _logger_process_cls = _CustomWandbLoggingProcess

    def __init__(
        self,
        *args,
        save_base_path: tp.Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.save_base_path = save_base_path

    def log_trial_start(self, trial: Trial):
        config = trial.config.copy()

        config.pop("callbacks", None)  # Remove callbacks

        exclude_results = self._exclude_results.copy()

        # Additional excludes
        exclude_results += self.excludes

        # Log config keys on each result?
        if not self.log_config:
            exclude_results += ["config"]

        # Fill trial ID and name
        trial_id = trial.trial_id if trial else None
        trial_name = str(trial) if trial else None

        # Project name for Wandb
        wandb_project = self.project

        # Grouping
        wandb_group = self.group or trial.experiment_dir_name if trial else None

        # remove unpickleable items!
        config = _clean_log(config)

        wandb_init_kwargs = dict(
            id=trial_id,
            name=trial_name,
            resume=False,
            reinit=True,
            allow_val_change=True,
            group=wandb_group,
            project=wandb_project,
            config=config,
        )
        wandb_init_kwargs.update(self.kwargs)

        self._trial_queues[trial] = Queue()
        self._trial_processes[trial] = self._logger_process_cls(
            logdir=trial.logdir,
            queue=self._trial_queues[trial],
            exclude=exclude_results,
            to_config=self._config_results,
            save_base_path=self.save_base_path,
            **wandb_init_kwargs,
        )
        self._trial_processes[trial].start()

    def log_trial_result(self, iteration: int, trial: Trial, result: tp.Dict):
        print("TRIAL RESULT")
        self._trial_queues[trial].put(
            (_CustomQueueItem.FILE, f"{self.save_base_path}/*")
        )
        super().log_trial_result(iteration, trial, result)

    def log_trial_save(self, trial: Trial):
        print("TRIAL SAVE")
        self._trial_queues[trial].put(
            (_CustomQueueItem.FILE, f"{self.save_base_path}/*")
        )
        super().log_trial_save(trial)

    def log_trial_end(self, trial: Trial, failed: bool = False):
        print("TRIAL END")
        self._trial_queues[trial].put(
            (_CustomQueueItem.FILE, f"{self.save_base_path}/*")
        )
        super().log_trial_end(trial, failed=failed)
