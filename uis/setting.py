from nicegui import ui

from ._setting import reload, lan_setting, dark_setting, run_notify, startup


def main(language: str):
    with ui.column():
        reload.Button(language)
        lan_setting.Select(language)
        dark_setting.Select(language)
        with ui.row():
            run_notify.CheckBoxes(language)
            startup.CheckBoxes(language)
