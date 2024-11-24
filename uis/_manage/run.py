import ast
import asyncio

from nicegui import ui

from utils import maafw
from utils.tool.files import Read, Write
from utils.tool.singleton import singleton
from uis.i18n import language_type
from .._setting.run_notify import CheckBoxes
from uis._setting.maa_setting import GPUSelect


@singleton
class Button:
    def __init__(self, language: str) -> None:
        self.i18n = language_type(language).Manage.Run
        self.button = ui.button(self.i18n.Button.run, icon="play_arrow").props(
            "no-caps"
        )
        self.button.on_click(NewDialog(language).open)

    def enable(self):
        self.button.enable()

    def disable(self):
        self.button.disable()


@singleton
class NewDialog:
    def __init__(self, language: str) -> None:
        i18n = language_type(language).Manage.Run.Button
        with ui.dialog().classes("w-full") as self.dialog, ui.card().style(
            "width: 500px; height: 550px; max-width: none"
        ):

            with ui.row():
                self.update = (
                    ui.button(i18n.update, icon="update")
                    .props("no-caps")
                    .classes("w-25")
                )
                self.delete = (
                    ui.button(i18n.delete, icon="delete")
                    .props("no-caps")
                    .classes("w-25")
                )
                self.run = RunButton(language)
                self.stop = StopButton(language)
                self.run.disable()
                self.stop.disable()
            config = ConfigTable(language)
            self.delete.disable()
            self.update.on_click(config.update_on_click)
            self.delete.on_click(config.delete_on_click)

    def open(self):
        self.dialog.open()

    def close(self):
        self.dialog.close()


@singleton
class ConfigTable:
    def __init__(self, language: str) -> None:
        self.language = language
        self.i18n = i18n = language_type(language).Manage.Run
        columns = []
        for c_list in [
            ["config_name", i18n.configname],
            ["app_name", i18n.appname],
            ["create_time", i18n.create_time],
        ]:
            column = c_list[0]
            label = c_list[1]
            columns.append(
                {
                    "name": column,
                    "label": label,
                    "field": column,
                    "required": True,
                    "align": "center",
                }
            )
            apps = self.read()
        self.table = ui.table(
            columns=columns,
            rows=apps,
            selection="multiple",
            row_key="create_time",
            pagination=5,
        ).classes("w-full")
        self.table.on_select(self.table_on_select)

    def read(self):
        data: dict[dict] | int | None = Read().devices("apps")
        if type(data) == int:
            return 0
        elif data is None:
            apps = [
                {
                    "config_name": "Undefined",
                    "app_name": "Undefined",
                    "create_time": "Undefined",
                }
            ]
            return apps

        app_keys: list = data.keys()
        apps: list[dict] = []
        # str some datas,because ui.table doesn't accept list[list] or list[dict] as param.
        for a_k in app_keys:
            app_dict = {}
            for key in data[a_k].keys():
                if key in ["task"]:
                    app_dict.update({key: str(data[a_k][key])})
                else:
                    app_dict.update({key: data[a_k][key]})
            apps.append(app_dict)
        return apps

    def table_on_select(self):
        self.change_buttons_statu()

    def change_buttons_statu(self):
        dialog = NewDialog(self.language)
        if self.table.selected == []:
            dialog.delete.disable()
            dialog.run.disable()
        elif (
            len(self.table.selected) == 1
            and self.table.selected[0]["create_time"] != "Undefined"
        ):
            dialog.delete.enable()
            dialog.run.enable()
        elif len(self.table.selected) > 1:
            dialog.delete.enable()
            dialog.run.disable()

    def update(self):
        apps = self.read()
        self.table.rows = apps
        self.table.selected = []
        self.table.update()

    def update_on_click(self):
        self.update()
        ui.notify(self.i18n.Notify.updated, position="bottom-right", type="positive")

    def delete_on_click(self):
        apps: list[dict] = self.table.selected
        del_key = []
        for app in apps:
            create_time = app["create_time"]
            if create_time == "Undefined":
                return
            del_key.append(create_time)
        Write().json("del_app", "", del_key=del_key)
        ui.notify(self.i18n.Notify.deleted, position="bottom-right", type="info")
        self.update()


@singleton
class RunButton:
    def __init__(self, language: str) -> None:
        self.language = language
        self.i18n = language_type(language).Manage
        self.button = (
            ui.button(self.i18n.Button.run, icon="play_arrow")
            .props("no-caps")
            .props("align='left'")
            .classes("justify-start")
        )
        self.button.on_click(MaaCore(self.language).run)

    def enable(self):
        self.button.enable()

    def disable(self):
        self.button.disable()


@singleton
class StopButton:
    def __init__(self, language: str) -> None:
        self.language = language
        self.i18n = language_type(language).Manage
        self.button = (
            ui.button(self.i18n.Button.stop, icon="cancel")
            .props("no-caps")
            .props("align='left'")
            .classes("justify-start")
        )
        self.button.on_click(MaaCore(language).stop)

    def enable(self):
        self.button.enable()

    def disable(self):
        self.button.disable()


@singleton  # If possible,replace it.
class MaaCore:
    def __init__(
        self,
        language: str,
    ) -> None:
        self.language = language
        self.i18n = language_type(language).Manage.Run.Notify

    async def run(self) -> bool | None:
        from .device import AdbTable, Win32Table

        i18n = self.i18n
        device_select: dict = (
            AdbTable(self.language).table.selected
            + Win32Table(self.language).table.selected
        )[0]
        app: dict = ConfigTable(self.language).table.selected[0]

        device_id = device_select["id"]
        adbs, win32s = Read().devices("adbs"), Read().devices("win32s")
        device = None
        if adbs is not None and type(adbs) != int and device is None:
            if device_id in adbs.keys():
                device = adbs[device_id]
        if win32s is not None and type(win32s) != int:
            if device_id in win32s.keys():
                device = win32s[device_id]
        if device is None:
            ui.notify(
                f"{i18n.error} (200)",
                position="bottom-right",
                type="negative",
            )
            return
        device_keys = device.keys()

        # Init toolkit
        statu = await maafw.init_toolkit()
        if type(statu) == int:
            ui.notify(
                f"{i18n.untoolkited} ({statu})",
                position="bottom-right",
                type="negative",
            )
            return
        if CheckBoxes(self.language).toolkit_stat.value:
            ui.notify(i18n.toolkited, position="bottom-left", type="positive")

        # Connect
        ctrl = None
        if "address" in device_keys:
            (path, address, screencap, input, config) = (
                device["path"],
                device["address"],
                device["screencap"],
                device["input"],
                device["config"],
            )
            ctrl = await maafw.connect_adb(path, address, screencap, input, config)
        elif "hwnd" in device_keys:
            ctrl = await maafw.connect_win32()
        else:
            ui.notify(f"{i18n.error} (201)", position="bottom-right", type="negative")
            return
        if ctrl is None:
            ui.notify(i18n.unconneted, position="bottom-right", type="negative")
            return
        if CheckBoxes(self.language).controller_statu.value:
            ui.notify(i18n.connected, position="bottom-left", type="positive")

        # Load resource
        res = None
        res = await maafw.load_resource(
            app["resource"],
            app["app_path"],
            app["app_name"],
            GPUSelect(self.language).gpu_select.value,
        )
        if type(res) == int or type(res) == str:
            ui.notify(
                f"{i18n.unresed} ({res})", position="bottom-right", type="negative"
            )
            return
        elif res is None:
            ui.notify(f"{i18n.error} (202)", position="bottom-right", type="negative")
            return
        if CheckBoxes(self.language).resorce_statu.value:
            ui.notify(i18n.resed, position="bottom-left", type="positive")

        # Bind tasker
        self.tasker = None
        self.tasker = await maafw.bind_tasker(res, ctrl)
        if type(self.tasker) == int:
            ui.notify(
                f"{i18n.untaskered} ({self.tasker})",
                position="bottom-right",
                type="negative",
            )
            return
        elif self.tasker is None:
            ui.notify(f"{i18n.error} (202)", position="bottom-right", type="negative")
            return
        if CheckBoxes(self.language).tasker_statu.value:
            ui.notify(i18n.taskered, position="bottom-left", type="positive")

        # Run task
        StopButton(self.language).enable()
        self.notification = ui.notification(
            i18n.doing,
            position="bottom-right",
            type="info",
            spinner=True,
            timeout=None,
            close_button=True,
        )
        tasks: str = app["task"]
        tasks = ast.literal_eval(tasks)
        statu = await maafw.run_task(self.tasker, tasks)
        if type(statu) == int:
            self.notification.message = f"{i18n.undone} ({statu})"
            self.notification.type = "negative"
            self.notification.spinner = False
            await asyncio.sleep(3)
            self.notification.dismiss()
            return
        RunButton(self.language).enable()
        StopButton(self.language).disable()
        self.notification.message = i18n.done
        self.notification.type = "positive"
        self.notification.spinner = False
        await asyncio.sleep(3)
        self.notification.dismiss()
        return True

    async def stop(self):
        i18n = self.i18n
        # Stop Task
        notification = self.notification
        if self.tasker is None:
            notification.message = i18n.unstopped_tasker
            notification.type = "negative"
            notification.spinner = False
        elif not await maafw.stop_task(self.tasker):
            notification.message = i18n.unstopped
            notification.type = "negative"
            notification.spinner = False
        else:
            RunButton(self.language).enable()
            StopButton(self.language).disable()
            ConfigTable(self.language).table.set_visibility(True)
            notification.message = i18n.stopped
            notification.type = "warning"
            notification.spinner = False
        await asyncio.sleep(3)
        notification.dismiss()
