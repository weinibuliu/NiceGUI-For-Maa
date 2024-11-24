from nicegui import ui

from ._setting import (
    reload,
    lan_setting,
    dark_setting,
    run_notify,
    startup,
    maa_setting,
)


def main(language: str):
    with ui.column():
        reload.Button(language)
        with ui.row():
            lan_setting.Select(language)
            dark_setting.Select(language)
        maa_setting.main(language)
        with ui.row():
            run_notify.CheckBoxes(language)
            startup.CheckBoxes(language)
