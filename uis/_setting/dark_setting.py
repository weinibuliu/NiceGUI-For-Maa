import asyncio

from nicegui import ui

from .reload import reload
from utils.tool.files import Read, Wirte
from uis.i18n import language_type


class Select:
    def __init__(self, language: str) -> None:
        dark: bool | None = Read().ui_config()["dark"]
        self.i18n = language_type(language).Setting.Dark
        self.dark_select = ui.select(
            self.i18n.dark_dict, label=self.i18n.dark, value=dark
        ).classes("w-40")
        self.dark_select.on_value_change(self.select_on_change)

    async def select_on_change(self):
        self.dark_select.disable()
        dark = self.dark_select.value
        i18n = self.i18n
        Wirte().json(target="ui_config", data={"dark": dark})
        ui.notify(
            message=i18n.notify,
            position="bottom-right",
            type="info",
        )
        await asyncio.sleep(1)
        reload()
