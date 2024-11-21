from maa.custom_action import CustomAction
from maa.custom_recognition import CustomRecognition

from custom_src import sample


class Sample:
    recs: list[dict[str, CustomRecognition]] | None = [{"CustomA": sample.CustomA()}]
    acts: list[dict[str, CustomAction]] | None = [{"CustomB": sample.CustomB()}]


class AppA:
    recs: list[dict[str, CustomRecognition]] | None = None
    acts: list[dict[str, CustomAction]] | None = None


class AppB:
    recs: list[dict[str, CustomRecognition]] | None = None
    acts: list[dict[str, CustomAction]] | None = None
