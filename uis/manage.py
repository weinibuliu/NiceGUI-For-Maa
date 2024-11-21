from nicegui import ui

from ._manage import add, config, device, delete, run, update


def main(language: str):
    with ui.column().classes("w-full"):
        with ui.row():
            add.Button(language)
            update.Button(language)
            delete.Button(language).disable()
            config.Button(language)
            run.Button(language).disable()
        device.AdbTable(language)
        device.Win32Table(language)
