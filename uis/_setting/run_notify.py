from nicegui import ui

from uis.i18n import language_type
from utils.tool.singleton import singleton
from utils.tool.files import Read, Write

ui_config = Read().ui_config()
toolkit = ui_config["run_toolkit"]
res = ui_config["run_res"]
ctrl = ui_config["run_ctrl"]
tasker = ui_config["run_tasker"]


@singleton
class CheckBoxes:
    def __init__(self, language: str) -> None:
        self.i18n = i18n = language_type(language).Setting.RunNotify
        with ui.card().style("width: 350px; height: 160px"):
            ui.label(i18n.notify)
            with ui.row(align_items="start"):
                self.toolkit_stat = ui.checkbox(i18n.toolkit, value=toolkit)
                self.resorce_statu = ui.checkbox(i18n.resource, value=res)
                self.controller_statu = ui.checkbox(i18n.controller, value=ctrl)
                self.tasker_statu = ui.checkbox(i18n.tasker, value=tasker)

        self.toolkit_stat.on_value_change(
            lambda: self.on_change({"run_toolkit": self.toolkit_stat.value})
        )
        self.resorce_statu.on_value_change(
            lambda: self.on_change({"run_res": self.resorce_statu.value})
        )
        self.controller_statu.on_value_change(
            lambda: self.on_change({"run_ctrl": self.controller_statu.value})
        )
        self.tasker_statu.on_value_change(
            lambda: self.on_change({"run_tasker": self.tasker_statu.value})
        )

    def on_change(self, data: dict):
        Write().json("ui_config", data=data)
