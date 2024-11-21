from nicegui import ui

from utils.tool.files import Read, Wirte
from uis.i18n import language_type

show = Read().ui_config()["show"]


class CheckBoxes:
    def __init__(self, language: str) -> None:
        with ui.card().style("width: 350px; height: 160px"):
            self.i18n = i18n = language_type(language).Setting.Startup
            ui.label(i18n.startup)
            self.show = ui.checkbox(i18n.show, value=show)
            self.guide = ui.checkbox(i18n.guide, value=False)
            self.guide.disable()  # Disable becuase it is not completed.
            self.show.on_value_change(
                lambda: Wirte().json("ui_config", data={"show": self.checkbox.value})
            )
