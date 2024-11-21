from nicegui import ui

from utils.tool.singleton import singleton
from uis.i18n import language_type
from utils.tool.files import Read, Wirte
from . import delete, run, update

ui_config = Read().ui_config()
show_adb: bool = ui_config["show_adb"]
show_win32 = ui_config["show_win32"]


@singleton
class AdbTable:
    def __init__(self, language: str):
        self.language = language
        i18n = self.i18n = language_type(language).Manage.Device.Adb
        adbs = self.read()
        if type(adbs) == int:
            ui.notify(
                f"{self.i18n.uninited} {adbs}",
                position="bottom-right",
                type="negative",
            )
            return
        columns = []
        for c_list in [
            ["name", i18n.name],
            ["path", i18n.path],
            ["address", i18n.address],
            ["id", "id"],
        ]:
            column = c_list[0]
            label = c_list[1]
            if column in ["id"]:
                columns.append(
                    {
                        "name": column,
                        "classes": "hidden",
                        "headerClasses": "hidden",
                    }
                )
            else:
                columns.append(
                    {
                        "name": column,
                        "label": label,
                        "field": column,
                        "required": True,
                        "align": "center",
                    }
                )
        with ui.row().classes("w-full"):
            self.checkbox = ui.checkbox("Adb", value=show_adb)
            self.checkbox.on_value_change(self.update)
            self.table = (
                ui.table(
                    columns=columns,
                    rows=adbs,
                    selection="multiple",
                    pagination=5,
                )
                .classes("w-full")
                .bind_visibility_from(self.checkbox, "value")
            )
        self.checkbox.on_value_change(self.change_buttons_statu)
        self.table.on_select(self.change_buttons_statu)

    def update(self) -> None | int:
        Wirte().json("ui_config", data={"show_adb": self.checkbox.value})
        adbs = self.read()
        if type(adbs) == int:
            return 201
        self.table.rows = adbs
        self.table.selected = []
        self.change_buttons_statu()
        self.table.update()

    def change_buttons_statu(self):
        length = len(self.table.selected + Win32Table(self.language).table.selected)
        if length > 0:
            delete.Button(self.language).enable()
            if length == 1:
                run.Button(self.language).enable()
            else:
                run.Button(self.language).disable()
        else:
            delete.Button(self.language).disable()
            run.Button(self.language).disable()

        # If sample exists,disable buttons.
        for data in self.table.selected + Win32Table().table.selected:
            d_k = data.keys()
            if "address" in d_k:
                if data["address"] == "0.0.0.0:0000":
                    delete.Button(self.language).disable()
                    run.Button(self.language).disable()
                    break
            if "hwnd" in d_k:
                if data["hwnd"] == "0x00000":
                    delete.Button(self.language).disable()
                    run.Button(self.language).disable()
                    break
        # If checkboxes are all False,disable buttons.
        if not self.checkbox.value and not Win32Table(self.language).checkbox.value:
            update.Button(self.language).disable()
        else:
            update.Button(self.language).enable()

    def selected(self) -> list[dict] | int:
        selected = self.table.selected
        if selected == []:
            return 201
        return selected

    def read(self) -> list[dict] | int:
        data: dict | int | None = Read().devices("adbs")
        if type(data) == int:
            return 0
        if data is None:
            adbs = [
                {
                    "name": self.i18n.sample,
                    "path": "D:/MyPlayer/adb.exe",
                    "address": "0.0.0.0:0000",
                    "task": "Undefined",
                    "id": "00000000",
                }
            ]
            return adbs
        adbs: list[dict] = []
        keys: list[str] = list(data.keys())
        for key in keys:
            adbs.append(data[key])

        # str some datas,because ui.table doesn't accept list[list] or list[dict] as param.
        final_adbs = []
        for adb in adbs:
            adb_dict = {}
            adb_keys = adb.keys()
            for key in adb_keys:
                if key in []:
                    adb_dict.update({key: str(adb[key])})
                else:
                    adb_dict.update({key: adb[key]})
            final_adbs.append(adb_dict)

        return final_adbs


@singleton
class Win32Table:
    def __init__(self, language: str) -> None:
        self.language = language
        i18n = self.i18n = language_type(language).Manage.Device.Win32
        win32s = []
        win32s = self.read()
        if type(win32s) == int:
            ui.notify(
                f"{self.i18n.uninited} {win32s}",
                position="bottom-right",
                type="negative",
            )
            return
        columns = []
        for c_list in [
            ["name", i18n.name],
            ["hwnd", i18n.hwnd],
        ]:
            column = c_list[0]
            label = c_list[1]
            if column in ["id"]:
                columns.append(
                    {
                        "name": column,
                        "classes": "hidden",
                        "headerClasses": "hidden",
                    }
                )
            else:
                columns.append(
                    {
                        "name": column,
                        "label": label,
                        "field": column,
                        "required": True,
                        "align": "center",
                    }
                )
        with ui.row().classes("w-full"):
            self.checkbox = ui.checkbox("Win32", value=show_win32)
            self.checkbox.on_value_change(self.update)
            self.table = (
                ui.table(
                    columns=columns,
                    rows=win32s,
                    selection="multiple",
                    pagination=5,
                )
                .classes("w-full")
                .bind_visibility_from(self.checkbox, "value")
            )
        self.checkbox.on_value_change(self.change_buttons_statu)
        self.table.on_select(self.change_buttons_statu)

    def update(self) -> None | int:
        Wirte().json("ui_config", data={"show_win32": self.checkbox.value})
        win32s = self.read()
        if type(win32s) == int:
            return 201
        self.table.rows = win32s
        self.table.selected = []
        self.change_buttons_statu()
        self.table.update()

    def change_buttons_statu(self):
        length = len(self.table.selected + AdbTable(self.language).table.selected)
        if length > 0:
            delete.Button(self.language).enable()
            if length == 1:
                run.Button(self.language).enable()
            else:
                run.Button(self.language).disable()

        else:
            delete.Button(self.language).disable()
            run.Button(self.language).disable()

        # If sample exists,disable buttons.
        for data in self.table.selected + AdbTable().table.selected:
            d_k = data.keys()
            if "address" in d_k:
                if data["address"] == "0.0.0.0:0000":
                    delete.Button(self.language).disable()
                    run.Button(self.language).disable()
                    break
            if "hwnd" in d_k:
                if data["hwnd"] == "0x00000":
                    delete.Button(self.language).disable()
                    run.Button(self.language).disable()
                    break
        # If checkboxes are all False,disable buttons.
        if not self.checkbox.value and not AdbTable(self.language).checkbox.value:
            update.Button(self.language).disable()
        else:
            update.Button(self.language).enable()

    def selected(self) -> list[dict] | int:
        selected = self.table.selected
        if selected == []:
            return 201
        return selected

    def read(self) -> list[dict] | int:
        data: dict | None = Read().devices("win32s")
        if type(data) == int:
            return 0
        if data is None:
            win32s = [
                {
                    "name": "Github Desktop",
                    "hwnd": "0x00000",
                    "task": "Undefined",
                    "id": "00000000",
                }
            ]
            return win32s
        win32s: list[dict] = []
        keys: list[str] = list(data.keys())
        for key in keys:
            win32s.append(data[key])

        # str some datas,because ui.table doesn't accept list[list] or list[dict] as param.
        final_win32s = []
        for win32 in win32s:
            win32_dict = {}
            win32_keys = win32.keys()
            for key in win32_keys:
                if key in []:
                    win32_dict.update({key: str(win32[key])})
                else:
                    win32_dict.update({key: win32[key]})
            final_win32s.append(win32_dict)

        return final_win32s
