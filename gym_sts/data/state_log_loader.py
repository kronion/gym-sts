import json
from typing import TextIO


class StateLogLoader:
    def __init__(self):
        self.data = []

    def load_file(self, fh: TextIO):
        objs = json.load(fh)

        # Discard first entry, as we don't know what came before it
        # For each subsequent entry, format as (before, action, after)
        for i in range(1, len(objs)):
            self.data.append(
                {
                    "state_before": objs[i - 1]["state_after"],
                    "action": objs[i]["action"],
                    "state_after": objs[i]["state_after"],
                }
            )
