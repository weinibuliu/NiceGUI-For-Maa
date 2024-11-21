from nicegui import ui

from utils.tool.singleton import singleton
from uis.i18n import language_type


@singleton
class Button:
    def __init__(self, language: str) -> None:
        self.language = language
        self.i18n = language_type(language).Manage
        self.button = (
            ui.button(self.i18n.Button.update, icon="update")
            .props("no-caps")
            .props("align='left'")
            .classes("justify-start")
        )
        self.button.on_click(self.button_on_click)

    def enable(self):
        self.button.enable()

    def disable(self):
        self.button.disable()

    def button_on_click(self):
        from .device import AdbTable, Win32Table  # To avoid import error.

        if AdbTable(self.language).checkbox.value:
            a_statu = AdbTable(self.language).update()
            if type(a_statu) == int:
                ui.notification(
                    f"{self.i18n.Device.Adb.unupdated} ({a_statu})",
                    position="bottom-right",
                    type="negative",
                    timeout=3,
                )
            else:
                ui.notification(
                    self.i18n.Device.Adb.updated,
                    position="bottom-right",
                    type="positive",
                    timeout=3,
                )

        if Win32Table(self.language).checkbox.value:
            w_statu = Win32Table(self.language).update()
            if type(w_statu) == int:
                ui.notification(
                    f"{self.i18n.Device.Adb.unupdated} ({w_statu})",
                    position="bottom-right",
                    type="negative",
                    timeout=3,
                )
            else:
                ui.notification(
                    self.i18n.Device.Win32.updated,
                    position="bottom-right",
                    type="positive",
                    timeout=3,
                )
