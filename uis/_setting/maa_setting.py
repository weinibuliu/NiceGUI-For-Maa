from nicegui import ui
from maa import ver as maa_ver

from utils.tool.files import Read, Write
from utils.tool.gpu import get_gpu
from utils.tool.singleton import singleton
from uis.i18n import language_type


ui_config = Read().ui_config()
gpu = ui_config["gpu"]


def main(language: str):
    i18n = language_type(language).Setting.Maa
    with ui.card():
        ui.label(i18n.maa)
        ui.label(f"{i18n.version} {maa_ver}")
        GPUSelect(language)


@singleton
class GPUSelect:
    def __init__(self, language: str) -> None:
        self.i18n = i18n = language_type(language).Setting.Maa
        self.gpu_select = ui.select({}, label=i18n.gpu_select).classes("w-80")
        self.gpu_select.disable()
        self.gpu_select.on_value_change(self.on_select)
        gpus = get_gpu(language)
        if gpus is not None:
            self.gpu_select.set_options(gpus)
            self.gpu_select.set_value(gpu)
            self.gpu_select.enable()
        else:
            self.gpu_select.set_options({-2: "Disable(Set CPU)"})
            self.gpu_select.set_value(-2)

    def enable(self):
        self.gpu_select.enable()

    def disable(self):
        self.gpu_select.disable()

    def on_select(self):
        Write().json("ui_config", data={"gpu": self.gpu_select.value})
