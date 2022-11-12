import json
from pathlib import Path
from typing import Dict, List, Tuple

from gym_sts.constants import PROJECT_ROOT
from gym_sts.spaces.old_constants import (
    ALL_EVENTS,
    GLOBALLY_CHECKED_TEXTS,
    MAX_NUM_CUSTOM_TEXTS,
)

REMOVED_STRINGS = ["#r", "#y", "#g", "#b", "#p", "@", "~", "NL"]


# Utility to match event text with normal text
class EventData:
    def __init__(self, file_path: Path):
        with open(file_path, "r") as f:
            self._data = json.load(f)
        self.event_texts: Dict[str, List[str]] = {
            # Hardcoded case for Neow Event as it is not in the events.json but instead
            # in characters.json
            # TODO: Show the individual choices for Neow Event
            "Neow Event": []
        }
        for event_id, event in self._data.items():
            if "OPTIONS" not in event:
                # One of the event texts is malformed; namely, "Proceed Screen" which
                # is not mentioned anywhere
                continue
            results = []
            for desc in event["DESCRIPTIONS"]:
                results.append(self.remove_formatting(desc))
            for opt in event["OPTIONS"]:
                results.append(self.remove_formatting(opt))

            # NOTE: The game uses the event_id keys, internally, NOT the names
            self.event_texts[event_id] = results

        self.sanity_check()

    def remove_formatting(self, text: str):
        for s in REMOVED_STRINGS:
            text = text.replace(s, "")
        return text

    def find_matches(self, event_id: str, text: str) -> List[Tuple[str, bool]]:
        # Returns (str, bool) pairs for matching texts
        # The order in which the elements are output should be deterministic
        match_list = []

        for part in GLOBALLY_CHECKED_TEXTS:
            match_list.append((part, part in text))

        for part in self.event_texts[event_id]:
            match_list.append((part, part in text))

        return match_list

    def sanity_check(self):
        # Simple sanity check to check if we actually read in the data
        assert len(self.event_texts.keys()) > 0
        for event in ALL_EVENTS:
            if event != "NONE":
                if event not in self.event_texts:
                    raise RuntimeError(f"Event {event} not found in event IDs")

                texts = self.event_texts[event]

                # TODO: Cleanup after you figure out how to handle Neow Event
                if len(texts) == 0 and event != "Neow Event":
                    raise RuntimeError(
                        f"Event {event} seemingly has no text associated with it"
                    )

                if len(texts) > MAX_NUM_CUSTOM_TEXTS:
                    raise RuntimeError(
                        f"Event {event} has too many custom texts! "
                        "({len(texts)}/{MAX_NUM_CUSTOM_TEXTS})"
                    )


EVENTS_JSON_PATH = PROJECT_ROOT / "data" / "events.json"
EVENT_DATA = EventData(EVENTS_JSON_PATH)
