from nicegui import ui

from . import device
from utils.tool.files import Write
from uis.i18n import language_type
from utils.tool.singleton import singleton


@singleton
class Button:
    def __init__(self, language: str) -> None:
        self.i18n = language_type(language).Manage
        self.button = (
            ui.button(self.i18n.Button.delete, icon="delete")
            .props("no-caps")
            .props('align="left"')
            .classes("justify-start")
        )
        self.button.on_click(NewDialog(language).open)

    def enable(self):
        self.button.enable()

    def disable(self):
        self.button.disable()


@singleton
class NewDialog:
    def __init__(self, language: str) -> None:
        self.language = language
        self.i18n = language_type(language).Manage.Delete

    def open(self):
        i18n = self.i18n
        with ui.dialog() as self.dialog, ui.card():
            with ui.column():
                ui.markdown(i18n.ensure)
                with ui.row().classes("w-full justify-center"):
                    yes = ui.button(i18n.del_yes).props("no-caps")
                    no = ui.button(i18n.del_no).props("no-caps")
                    yes.on_click(self.delete)
                    no.on_click(self.close)
        self.dialog.open()

    def close(self):
        self.dialog.close()

    def delete(self) -> list[str] | None:
        i18n = self.i18n
        adb_selected = device.AdbTable(self.language).selected()
        win32_selected = device.Win32Table(self.language).selected()

        adb_del_key = []
        win32_del_key = []
        if type(adb_selected) == list:
            for del_data in adb_selected:
                adb_del_key.append(del_data["id"])  # Use the "id" as index.
        if type(win32_selected) == list:
            for del_data in win32_selected:
                win32_del_key.append(del_data["id"])  # Use the "id" as index.

        for del_key, kind in zip((adb_del_key, win32_del_key), ("adb", "win32")):
            if del_key == []:
                continue
            w_statu = Write().json("del_device", kind, del_key=del_key)
            if w_statu is not None:
                ui.notify(
                    f"{i18n.faild} ({w_statu})",
                    position="bottom-right",
                    type="negative",
                )
                return
            NewDialog(self.language).close()
            device.AdbTable(self.language).update()
            device.Win32Table(self.language).update()

        ui.notify(i18n.success, position="bottom-right", type="info")
        Button().disable()
