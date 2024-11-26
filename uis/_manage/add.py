import re
import time
import asyncio

from nicegui import ui
from maa.toolkit import AdbDevice, DesktopWindow

from . import device
from utils.tool.system import win32able
from uis.i18n import language_type
from utils.tool.singleton import singleton
from utils.maafw import Find
from utils.tool.files import Write
from utils.infos.methods import Methods


@singleton
class Button:
    def __init__(self, language: str) -> None:
        i18n = language_type(language).Manage.Button
        self.button = ui.button(
            i18n.add, icon="add_box", on_click=NewDialog(language).open
        ).props("no-caps")

    def enable(self):
        self.button.enable()

    def disable(self):
        self.button.disable()


@singleton
class NewDialog:
    def __init__(self, language: str) -> None:
        i18n = language_type(language).Manage.Add
        with ui.dialog().classes("w-full") as self.dialog, ui.card().style(
            "width: 500px; height: 550px; max-width: none"
        ):
            with ui.tabs().classes("w-full") as tabs:
                adb = ui.tab(name="Adb", label="Adb", icon="smartphone").props(
                    "no-caps"
                )
                win32 = ui.tab(
                    name="Win32", label="Win32", icon="desktop_windows"
                ).props("no-caps")
                win32.set_enabled(win32able)
            with ui.tab_panels(tabs, value=adb).classes("w-full"):
                with ui.tab_panel(adb):
                    with ui.tabs().classes("w-full") as adb_tabs:
                        auto = ui.tab(
                            name="Auto", label=i18n.adb_auto, icon="autorenew"
                        ).props("no-caps")
                        manual = ui.tab(
                            name=" Manual", label=i18n.adb_manual, icon="edit"
                        ).props("no-caps")
                    with ui.tab_panels(adb_tabs, value=auto).classes("w-full"):
                        with ui.tab_panel(auto):
                            Adb(language).auto()
                        with ui.tab_panel(manual):
                            Adb(language).manual()
                with ui.tab_panel(win32):
                    with ui.tabs().classes("w-full") as adb_tabs:
                        select = ui.tab(
                            name="Select", label=i18n.win32_select, icon="task_alt"
                        ).props("no-caps")
                    with ui.tab_panels(adb_tabs, value=select).classes("w-full"):
                        with ui.tab_panel(select):
                            Win32(language).select()

    def open(self):
        self.dialog.open()

    def close(self):
        self.dialog.close()


class Adb:
    def __init__(self, language: str) -> None:
        self.language = language
        self.i18n = language_type(language).Manage.Add.Adb

    def auto(self):
        language = self.language
        i18n = self.i18n
        with ui.row().classes("mx-auto items-center"):
            adb_select = (
                ui.select({}, label=i18n.Auto.select, with_input=True)
                .props("stack-lable")
                .classes("w-60")
            )
            adb_select.set_enabled(False)
            with ui.column():
                search = (
                    ui.button(i18n.Auto.search, icon="search")
                    .props("no-caps")
                    .props('align="left"')
                    .classes("justify-start; w-full")
                )
                save = (
                    ui.button(i18n.Auto.save, icon="save")
                    .bind_enabled_from(adb_select, "value")
                    .props("no-caps")
                    .props("align='left'")
                    .classes("justify-start; w-full")
                )

        @ui.refreshable
        def update_target_adb():
            info = adb_select.value
            i18n = self.i18n.ShowInfos
            with ui.column():
                show_infos = ui.markdown()
            if info is None:
                show_infos.set_content(i18n.default)
            else:
                infos: list[str] = info.split(";")
                path, address, extras = infos[0], infos[1], infos[2]
                _standard = i18n.standard
                standard = (
                    _standard.replace("PATH", path)
                    .replace("ADDRESS", address)
                    .replace("EXTRAS", extras)
                )
                show_infos.set_content(standard)

        update_target_adb()
        adb_select.on_value_change(update_target_adb.refresh)

        def click_save(self):
            adb_v: str = adb_select.value
            name: str = adb_select.options[adb_v]
            adb_infos: list[str] = adb_v.split(";")
            _path, _address, _extras = (adb_infos[0], adb_infos[1], eval(adb_infos[2]))
            w_statu = Write().json(
                target="add_device",
                kind="adb",
                data={
                    name: {
                        "id": name,
                        "name": name.split()[0],
                        "path": _path,
                        "address": _address,
                        "config": _extras,
                        "screencap": -1,
                        "input": -1,
                    }
                },
            )
            if w_statu is None:
                ui.notify(i18n.Notify.saved, position="bottom-right", type="positive")
                adb_select.set_options({})
                adb_select.disable()
                device.AdbTable(language).update()
                NewDialog().close()

            else:
                ui.notify(
                    f"{i18n.Notify.unsaved} ({w_statu})",
                    position="bottom-right",
                    type="negative",
                )

        async def find(self) -> list[AdbDevice]:
            adb_select.disable()
            adb_select.set_options({})
            search.disable()

            msg = ui.notification(timeout=None)
            msg.position = "bottom-right"
            msg.message = i18n.Notification.searching
            msg.type = "ongoing"
            msg.spinner = True

            begin_time = time.time()
            adbs = await Find.adb()  # TODO:If timeout?
            if adbs is None:
                msg.message = i18n.Notification.unfound
                msg.type = "negative"
                msg.spinner = False
                search.enable()
                await asyncio.sleep(3)
                msg.dismiss()
                return
            else:
                use_time = round(time.time() - begin_time, 3)
                msg.message = (
                    f"{i18n.Notification.found} ({i18n.Notification.use}: {use_time}s)"
                )
                msg.type = "positive"
                msg.spinner = False

            # Update Select
            options = {}
            for adb in adbs:  # Adb Deduplication
                value = f"{adb.adb_path};{adb.address};{adb.config}"
                label = f"{adb.name} {adb.address}"
                options[value] = label
            adb_select.set_options(options)
            adb_select.set_value(list(options.keys())[0])
            adb_select.enable()
            search.enable()
            await asyncio.sleep(3)
            msg.dismiss()

        search.on_click(find)
        save.on_click(click_save)

    def manual(self):
        i18n = self.i18n
        with ui.row():
            name = ui.input(i18n.Manual.name, placeholder="My Player")
            path = ui.input(
                i18n.Manual.path, placeholder="D:/User/Files/Player/Shell/adb.exe"
            )
            address = ui.input(i18n.Manual.address, placeholder="127.0.0.1:16384")
            extras = ui.input(i18n.Manual.extras, placeholder=r"{}")
            name.props("clearable").props("size=60")
            path.props("clearable").props("size=60")
            address.props("clearable").props("size=60")
            extras.props("clearable").props("size=60").tooltip(
                i18n.Manual.tooltip
            ).set_value("{}")
            with ui.row():
                advance_mode = ui.checkbox(i18n.Manual.advance)
                save = ui.button(i18n.Manual.save, icon="save")
                save.props("no-caps").disable()

            ui.label(i18n.Manual.warning).classes(
                replace="text-warning"
            ).bind_visibility_from(advance_mode, "value")
            screencap_methods = ui.select(
                Methods.Adb.screen, label=i18n.Manual.screencap_methods, value=-1
            )
            input_methods = ui.select(
                Methods.Adb.input, label=i18n.Manual.input_methods, value=-1
            )
            screencap_methods.bind_visibility_from(advance_mode, "value").props(
                "stack-lable"
            ).classes("w-60")
            input_methods.bind_visibility_from(advance_mode, "value").props(
                "stack-lable"
            ).classes("w-60")

        def check():
            if path.value != "":
                path_statu = True
            else:
                path_statu = False
            if address.value != "":
                address_statu = True
            else:
                address_statu = False
            if extras.value == "":
                extras_statu = False
            else:
                extras_statu = re.match(r"{.*}", extras.value)

            statu = path_statu and address_statu and extras_statu
            save.set_enabled(bool(statu))

        def click_save():
            rercord_time = time.strftime("%Y-%m-%d %H:%M:%S")
            if name.value is None or name.value == "":
                _name = i18n.Manual.undefined
            else:
                _name = name.value
            _extras = eval(extras.value)
            w_statu = Write().json(
                target="add_device",
                kind="adb",
                data={
                    rercord_time: {
                        "id": rercord_time,  # Use the current time as id to marks the adb device.
                        "name": _name,
                        "path": path.value,
                        "address": address.value,
                        "config": _extras,
                        "screencap": screencap_methods.value,
                        "input": input_methods.value,
                    }
                },
            )
            if w_statu is None:
                ui.notify(i18n.Notify.saved, position="bottom-right", type="positive")
                path.value = ""
                address.value = ""
                extras.value = "{}"
                device.AdbTable().update()
                NewDialog().close()

            else:
                ui.notify(
                    f"{i18n.Notify.unsaved} ({w_statu})",
                    position="bottom-right",
                    type="negative",
                )

        path.on_value_change(check)
        address.on_value_change(check)
        extras.on_value_change(check)
        save.on_click(click_save)


class Win32:
    def __init__(self, language: str) -> None:
        self.language = language
        self.i18n = language_type(language).Manage.Add.Win32

    def select(self):
        with ui.row():
            hwnd = ui.select({}, label="HWND", with_input=True).classes("w-60")
            hwnd.disable()
            with ui.column():
                serach = (
                    ui.button(self.i18n.search, icon="search")
                    .props("no-caps")
                    .props('align="left"')
                    .classes("justify-start; w-full")
                )
                save = (
                    ui.button(self.i18n.save, icon="save")
                    .bind_enabled_from(hwnd, "value")
                    .props("no-caps")
                    .props("align='left'")
                    .classes("justify-start; w-full")
                )
        with ui.column():
            advance_mode = ui.checkbox(self.i18n.advance)
            ui.label(self.i18n.warning).classes(
                replace="text-warning"
            ).bind_visibility_from(advance_mode, "value")
            screencap_methods = (
                ui.select(Methods.Win32.screen, label="Screencap Methods", value=-1)
                .bind_visibility_from(advance_mode, "value")
                .props("stack-lable")
                .classes("w-60")
            )
            input_methods = (
                ui.select(Methods.Win32.input, label="Input Methods", value=-1)
                .bind_visibility_from(advance_mode, "value")
                .props("stack-lable")
                .classes("w-60")
            )

        async def find() -> list[DesktopWindow]:
            hwnd.disable()
            hwnd.set_options({})

            msg = ui.notification(timeout=None)
            msg.position = "bottom-right"
            msg.message = self.i18n.Notification.searching
            msg.type = "ongoing"
            msg.spinner = True

            begin_time = time.time()
            wins = await Find.win32()  # TODO:If timeout?

            if wins is None:
                msg.message = self.i18n.Notification.unfound
                msg.type = "negative"
                msg.spinner = False
                await asyncio.sleep(3)
                msg.dismiss()
                return
            else:
                msg.message = f"{self.i18n.Notification.found}({self.i18n.Notification.use}: {round(time.time()-begin_time,3)}s)"
                msg.type = "positive"
                msg.spinner = False

            # Update Select
            options = {}
            for win in wins:
                options[f"{hex(win.hwnd)};{win.window_name}"] = (
                    hex(win.hwnd) + " " + win.window_name
                )
            hwnd.set_options(options)
            hwnd.enable()
            await asyncio.sleep(3)
            msg.dismiss()

        def click_save():
            i18n = self.i18n
            rercord_time = str(time.time())
            _hwnd, name = hwnd.value.split(";")[0], hwnd.value.split(";")[1]
            w_statu = Write().json(
                target="add_device",
                kind="win32",
                data={
                    _hwnd: {
                        "id": _hwnd,
                        "hwnd": _hwnd,
                        "name": name,
                        "screencap": screencap_methods.value,
                        "input": input_methods.value,
                    }
                },
            )
            if w_statu is None:
                hwnd.set_value([])
                hwnd.set_options({})
                hwnd.update()
                hwnd.disable()
                device.Win32Table().update()
                NewDialog().close()

            else:
                ui.notify(
                    f"{i18n.Notify.unsaved} ({w_statu})",
                    position="bottom-right",
                    type="negative",
                )

        serach.on_click(find)
        save.on_click(click_save)
