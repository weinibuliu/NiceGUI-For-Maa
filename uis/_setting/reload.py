import asyncio
from pathlib import Path

from nicegui import ui

from uis.i18n import language_type


class Button:
    def __init__(self, language: str) -> None:
        self.i18n = language_type(language).Setting.Reload
        self.button = (
            ui.button(self.i18n.reload, icon="refresh")
            .props("no-caps")
            .props('align="left"')
            .classes("justify-start")
        )
        self.button.on_click(self.notify)

    async def notify(self):
        ui.notify(self.i18n.notify, position="bottom-right", type="info")
        await asyncio.sleep(1)
        reload()


def reload():
    ui_path = Path(Path.cwd(), "ui.py")
    ui_path.touch()
