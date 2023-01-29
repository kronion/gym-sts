import typing as tp

import torch
from ray.rllib.models import ModelCatalog
from ray.rllib.models.torch import fcnet


class MaskedModel(fcnet.FullyConnectedNetwork):
    def forward(
        self,
        input_dict: dict[str, torch.Tensor],
        state: list[torch.Tensor],
        seq_lens: torch.Tensor,
    ) -> tp.Tuple[torch.Tensor, list[torch.Tensor]]:
        logits, state = super().forward(input_dict, state, seq_lens)

        mask = input_dict["obs"]["valid_action_mask"]
        mask = torch.Tensor(mask).to(torch.bool)
        logits = torch.where(mask, logits, torch.finfo().min)

        return logits, state


def register():
    ModelCatalog.register_custom_model("masked", MaskedModel)
