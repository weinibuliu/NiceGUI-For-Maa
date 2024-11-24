import ast
import time

from nicegui import ui

from utils import maafw
from utils.tool.files import Write, FindDirs
from uis.i18n import language_type
from utils.tool.singleton import singleton
from . import run


@singleton
class Button:
    def __init__(self, language: str) -> None:
        self.language = language
        self.i18n = language_type(language).Manage.Config
        self.button = (
            ui.button(self.i18n.config, icon="manage_search")
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
        NewDialog(self.language).open()


@singleton
class NewDialog:
    def __init__(self, language: str) -> None:
        from .device import AdbTable, Win32Table  # To avoid import error

        self.language = language
        self.i18n = i18n = language_type(language).Manage.Config
        with ui.dialog() as self.dialog, ui.card().style(
            "width: 500px; height: 550px; max-width: none"
        ):
            with ui.tabs().classes("w-full") as self.tabs:
                self.app = ui.tab(name="App", label=i18n.app, icon="apps").props(
                    "no-caps"
                )
                self.task = ui.tab(
                    name="Task", label=i18n.task, icon="check_box"
                ).props("no-caps")
            with ui.tab_panels(self.tabs, value=self.app).classes("w-full"):
                with ui.tab_panel(self.app):
                    apps = {}
                    apps_data = (
                        FindDirs().app()
                    )  # Find all apps,get list[dict[str(path),str(label)]]
                    if apps_data is None:
                        ui.notify(
                            f"{self.i18n.Dialog.Notify.noapps} ({apps_data})",
                            position="bottom-right",
                            type="negative",
                        )
                    else:
                        apps = apps_data
                    with ui.column().classes("w-full"):
                        self.app_select = ui.select(
                            {}, label=i18n.Dialog.app_select, with_input=True
                        ).on_value_change(self.app_change)
                        self.res_select = ui.select(
                            {}, label=i18n.Dialog.res_select, with_input=True
                        ).bind_enabled_from(self.app_select, "value")
                        self.app_table = ui.table(
                            columns=app_table_columns(language),
                            rows=[],
                            row_key="app_author",
                        ).classes("w-full")
                        self.next = (
                            ui.button(i18n.Dialog.to_task, icon="arrow_forward")
                            .props("no-caps")
                            .bind_enabled_from(self.res_select, "value")
                        )
                        self.next.tailwind.align_self("end")
                        self.next.on_click(self.next_on_click)
                        self.app_select.set_options(apps)
                        if len(apps.keys()) == 1:
                            self.app_select.set_value(list(apps.keys())[0])
                with ui.tab_panel(self.task):
                    self.task.disable()
                    self.task_select = ui.select(
                        {}, label=i18n.Dialog.task_select, with_input=True
                    ).classes("w-full")
                    with ui.row().classes("w-fulll"):
                        with ui.column():
                            self.add = (
                                ui.button(i18n.Dialog.add, icon="add")
                                .props("no-caps")
                                .props("align='left'")
                                .classes("justify-start")
                            )
                            self.save = (
                                ui.button(i18n.Dialog.save, icon="save")
                                .props("no-caps")
                                .props("align='left'")
                                .classes("justify-start")
                            )
                        with ui.column():
                            self.delete = (
                                ui.button(i18n.Dialog.delete, icon="delete")
                                .props("no-caps")
                                .props("align='left'")
                                .classes("justify-start")
                            )
                            self.update = (
                                ui.button(i18n.Dialog.update, icon="update")
                                .props("no-caps")
                                .props("align='left'")
                                .classes("justify-start")
                            )
                    with ui.column().classes("w-full"):
                        self.s_a = ui.select({}, label="").classes("w-full")
                        self.s_b = ui.select({}, label="").classes("w-full")
                        self.s_c = ui.select({}, label="").classes("w-full")
                        self.s_d = ui.select({}, label="").classes("w-full")
                        self.s_e = ui.select({}, label="").classes("w-full")
                        self.s_f = ui.select({}, label="").classes("w-full")
                    self.task_table = ui.table(
                        rows=[],
                        columns=task_table_columns(language),
                        selection="multiple",
                        row_key="id",
                    ).classes("w-full")
                    # Init select.
                    self.s_list = [
                        self.s_a,
                        self.s_b,
                        self.s_c,
                        self.s_d,
                        self.s_e,
                        self.s_f,
                    ]
                    for s in self.s_list:
                        s.set_visibility(False)

                # Bind func to ui
                self.add.on_click(self.add_on_click)
                self.delete.on_click(self.delete_on_click)
                self.save.on_click(self.save_on_click)
                self.update.on_click(self.update_on_click)
                self.task_select.on_value_change(self.task_change)
                self.task_table.on_select(self.change_button_statu)

                # Buton statu init
                self.add.disable()
                self.delete.disable()
                self.save.disable()
                self.update.disable()

    def open(self):
        self.dialog.open()

    def close(self):
        self.dialog.close()

    def app_change(self):
        self.task.disable()
        app = self.app_select.value
        read = maafw.ReadInterface(app)
        res = read.get_resource()
        task = read.get_task()
        if type(res) == int or res is None:
            ui.notify(
                f"{self.i18n.Dialog.Notify.error} ({res})",
                position="bottom-right",
                type="negative",
            )
        self.res_select.set_options(res)
        if len(res.keys()) == 1:
            self.res_select.set_value(res.keys()[0])
        self.res_select.on_value_change(self.res_change)
        self.app_table.update_rows(app_table_rows(app))

    def res_change(self):
        if self.res_select.value:
            self.task.enable()
            app = self.app_select.value
            read = maafw.ReadInterface(app)
            task = read.get_task()
            self.task_select.set_options(task)
            self.task.enable()
        else:
            self.task.disable()

    def next_on_click(self):
        app = self.app_select.value
        read = maafw.ReadInterface(app)
        task = read.get_task()
        self.task_select.set_options(task)
        self.task_select.set_value("")
        self.clear_task()  # Clear Task
        self.tabs.value = self.task  # Jump to the task tab
        self.task.enable()

    def task_change(self):
        # value = f"{random int}@@@{entry}@@@{option_name}@@@{option_value}"
        self.add.enable()
        for s in self.s_list:
            s.set_visibility(False)
            s.set_options({})
            s.set_value("{}")
        value: str = self.task_select.value
        if value is not None and value != "":
            value_list = value.split("@@@")
            option = value_list[3]
            option_str: list[str] = ast.literal_eval(option)
            if option is None or option == []:
                return
            if type(option_str) == list:
                option_num = len(option_str)
            else:
                option_num = 0
            self.option_selects(option_num, option_str)

    def option_selects(self, option_num: int = 0, option_str: list[str] = None):
        i18n = self.i18n.Dialog
        for s in self.s_list:
            s.enable()
            s.visible = False
            s.set_options({})
            s.set_value({})
        if option_num == 0 or option_str is None:
            return
        elif option_num < 0 or option_str == [] or len(option_str) != option_num:
            ui.notify(
                f"{i18n.Notify.error} (203)", position="bottom-right", type="negative"
            )
            return
        elif option_num > len(self.s_list):
            ui.notify(
                f"{i18n.Notify.option_out_range} ({len(option_num)}:{len(self.s_list)})",
                position="bottom-right",
                type="warning",
            )

        option = maafw.ReadInterface(self.app_select.value).get_option()
        option_keys = option.keys()
        for s, opton_name in zip(self.s_list[0:option_num], option_str):
            option_dict = {}
            for key in option_keys:
                if f"{opton_name}@@@" in key:
                    option_dict.update({key: option[key]})
            if option_dict == {}:
                ui.notify(
                    f"{i18n.Notify.option_name_error} ({opton_name})",
                    position="bottom-right",
                    type="warning",
                )
                s.disable()
            s.set_visibility(True)
            s.set_options(option_dict)
            s._props["label"] = opton_name

    def add_on_click(self):
        self.add.disable()
        task_name = self.task_select.value
        task_option = {}
        for s in self.s_list:
            if s.value is not None:
                task_name += s.options[s.value] + " "
                task_option.update(eval(s.value.split("@@@")[1]))
        row = task_table_rows({task_name: task_option})
        self.task_table.add_row(row)
        self.task_table.update()
        ui.notify(
            self.i18n.Dialog.Notify.added, position="bottom-right", type="positive"
        )
        self.add.enable()
        self.change_button_statu()

    def delete_on_click(self):
        tasks: list[dict] = self.task_table.selected
        for task in tasks:
            self.task_table.rows.remove(task)

        self.task_table.rows = self.task_table.rows
        self.task_table.selected = []
        self.task_table.update()
        ui.notify(self.i18n.Dialog.Notify.deleted, position="bottom-right", type="info")
        self.delete.disable()
        self.change_button_statu()

    def update_on_click(self):
        self.task_table.selected = []
        self.task_table.update()
        ui.notify(
            self.i18n.Dialog.Notify.updated, position="bottom-right", type="positive"
        )

    def save_on_click(self):
        with ui.dialog().props("persistent") as name_dialog, ui.card():
            with ui.column().props("align='center'"):
                config_name = ui.input(
                    self.i18n.Dialog.config_name,
                    placeholder="Undefined",
                    value="Undefined",
                ).classes("w-full")
                with ui.row():
                    cancel_button = ui.button(
                        self.i18n.Dialog.cancel, icon="cancel"
                    ).props("no-caps")
                    continue_button = ui.button(
                        self.i18n.Dialog._continue, icon="chevron_right"
                    ).props("no-caps")

        name_dialog.open()

        def cancel_on_click():
            name_dialog.close()

        def continue_on_click():
            name_dialog.close()
            self.save.disable()
            rows: list[dict] = self.task_table.rows
            task_list = []
            for row in rows:
                task_dict = {
                    "entry": row["entry"],
                    "pipeline_override": eval(row["override"]),
                }
                task_list.append(task_dict)
            app_path = self.app_select.value
            app_name = self.app_select.options[app_path]
            res = self.res_select.value
            res = ast.literal_eval(res)
            create_time = time.strftime("%Y-%m-%d %H:%M:%S")
            data = {
                create_time: {
                    "config_name": config_name.value,
                    "create_time": create_time,
                    "app_name": app_name,
                    "app_path": app_path,
                    "resource": res,
                    "task": task_list,
                }
            }
            Write().json("add_app", data=data)
            ui.notify(
                self.i18n.Dialog.Notify.saved, position="bottom-right", type="positive"
            )
            self.dialog.close()
            run.ConfigTable(self.language).update()  # Upsate the config table
            self.clear_task()  # Clear the task tab.

        cancel_button.on_click(cancel_on_click)
        continue_button.on_click(continue_on_click)

    def clear_task(self):
        self.tabs.value = self.app
        self.task.disable()
        self.task_table.rows = []
        self.task_table.selected = []
        self.task_table.update()

    def change_button_statu(self):
        selected: list[dict] = self.task_table.selected
        rows: list[dict] = self.task_table.rows
        if type(selected) == list and selected != []:
            self.delete.enable()
        else:
            self.delete.disable()
        if type(rows) == list and len(rows) != []:
            self.save.enable()
            self.update.enable()
        else:
            self.save.disable()
            self.update.enable()


def app_table_columns(language: str) -> list[dict]:
    i18n = language_type(language).Manage.Config.Dialog
    columns = []
    for c_list in [
        ["author", i18n.app_author],
        ["version", i18n.app_version],
        ["url", i18n.app_url],
        ["message", i18n.app_meaasge],
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
    return columns


def app_table_rows(app) -> list[dict]:
    get_str = maafw.ReadInterface(app).get_str
    rows = [
        {
            "author": get_str("author"),
            "version": get_str("version"),
            "url": get_str("url"),
            "message": get_str("messgae"),
        }
    ]
    return rows


def task_table_columns(language: str) -> list[dict]:
    i18n = language_type(language).Manage.Config.Dialog
    columns = []
    for c_list in [
        ["name", i18n.task_name],
        ["option", i18n.task_option],
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
    return columns


def task_table_rows(task: dict) -> dict:
    # Replace some str
    key = list(task.keys())[0]
    raw_str: list[str] = key.split("@@@")

    task_name = raw_str[1]
    task_entry = raw_str[2]
    task_option = str(raw_str[4])
    override = str(task[key])
    task = []
    task = {
        "id": str(round(time.time(), 6)),
        "name": task_name,
        "entry": task_entry,
        "option": task_option,
        "override": override,
    }
    time.sleep(0.00001)  # Sleep to avoid the same time id.
    return task
