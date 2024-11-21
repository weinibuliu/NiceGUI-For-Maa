from maa.context import Context
from maa.custom_recognition import CustomRecognition
from maa.custom_action import CustomAction


class CustomA(CustomRecognition):
    def analyze(self, context: Context, argv: CustomRecognition.AnalyzeArg):
        pass  # Do something.


class CustomB(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg):
        pass  # Do something
