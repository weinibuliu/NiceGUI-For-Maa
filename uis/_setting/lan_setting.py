import asyncio

from nicegui import ui

from .reload import reload
from uis.i18n import language_type, language_dict
from utils.tool.files import Read, Wirte


class Select:
    def __init__(self, language: str) -> None:
        ui_language = Read().ui_config()["language"]
        self.i18n = language_type(language).Setting.Language
        self.language_select = ui.select(
            language_dict, label=self.i18n.language, value=ui_language
        ).classes("w-40")
        self.language_select.on_value_change(self.select_on_change)
        # self.language_select.disable()  # Disable because i18 is still not completed.

    async def select_on_change(self):
        self.language_select.disable()
        language = self.language_select.value
        i18n = self.i18n
        Wirte().json(target="ui_config", data={"language": language})
        ui.notify(
            message=i18n.notify,
            position="bottom-right",
            type="info",
        )
        if i18n.notify != i18n.notify_en:
            ui.notify(
                message=i18n.notify_en,
                position="bottom-right",
                type="info",
            )

        await asyncio.sleep(1)
        reload()
