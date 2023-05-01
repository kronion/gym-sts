from typing import Optional

from pydantic import BaseModel, validator


class ResetParams(BaseModel):
    """
    Pydantic model for validating reset() arguments.
    """

    seed: Optional[int]
    sts_seed: Optional[str]
    rng_state: Optional[tuple]
    reboot: bool = False

    @validator("rng_state")
    def seed_and_rng_state_are_mutually_exclusive(cls, v, values, **kwargs):
        if values.get("seed") is not None and v is not None:
            raise ValueError("seed and rng_state cannot both be provided")
        return v
