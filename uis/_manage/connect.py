from nicegui import ui

from utils.maafw import Connect
from utils.tool.files import Read
from utils.tool.singleton import singleton
from uis.i18n import language_type

'''
@singleton
class Button:
    def __init__(self, language: str) -> None:
        # On current version,the Connect Button will not be shown.Because it's designed for multi mange in the futrue version.
        self.language = language
        self.i18n = language_type(language).Manage
        """
        self.button = (
            ui.button(self.i18n.Button.connect, icon="link")
            .props("no-caps")
            .props('align="left"')
            .classes("justify-start")
        )
        """
        # self.button.on_click()

    def enable(self):
        pass
        # self.button.enable()

    def disable(self):
        pass
        # self.button.disable()
'''
