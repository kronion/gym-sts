import typing as tp

import tensorflow as tf

from ray.rllib.models import ModelCatalog
# from ray.rllib.models.tf import tf_modelv2
from ray.rllib.models.tf import fcnet

TensorType = tf.Tensor

class MaskedModel(fcnet.FullyConnectedNetwork):

    def forward(
        self,
        input_dict: dict[str, TensorType],
        state: list[TensorType],
        seq_lens: TensorType,
    ) -> tp.Tuple[TensorType, list[TensorType]]:
        logits, state = super().forward(input_dict, state, seq_lens)

        mask = input_dict["obs"]["valid_action_mask"]
        mask = tf.cast(mask, tf.bool)
        logits = tf.where(mask, logits, tf.float32.min)

        return logits, state

def register():
  ModelCatalog.register_custom_model("masked", MaskedModel)
