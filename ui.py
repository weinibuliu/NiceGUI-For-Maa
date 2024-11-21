# Project Author: @weinibuliu https://github.com/weinibuliu
# Project Url:
# The project is open source using the LGPLv3 license.

from nicegui import ui, app

from uis import manage, setting, about
from uis.infos import UIBase
from uis.i18n import language_type
from utils.tool.files import Read

# Read ui config
ui_config = Read().ui_config()
language: str = ui_config["language"]
dark = ui_config["dark"]
show = ui_config["show"]

if language not in ["zh_CN", "zh_TW", "en_US"]:  # If error happen,set language as zh_CN
    language = "zh_CN"


def main(language: str):
    i18n = language_type(language)
    with ui.tabs().classes("w-full") as tabs:
        Manage = ui.tab(name="Manage", label=i18n.Tabs.manage, icon="menu").props(
            "no-caps"
        )
        Setting = ui.tab(
            name="Setting", label=i18n.Tabs.setting, icon="settings"
        ).props("no-caps")
        About = ui.tab(name="About", label=i18n.Tabs.about, icon="info").props(
            "no-caps"
        )
    with ui.tab_panels(tabs, value=Manage).classes("w-full"):
        with ui.tab_panel(Manage):
            manage.main(language)
        with ui.tab_panel(Setting):
            setting.main(language)
        with ui.tab_panel(About):
            about.main(language)


def ready():
    urls = (
        str(app.urls)
        .replace("ObservableSet({", "")
        .replace("})", "")
        .replace("'", "")
        .replace(" ", "")
        .split(",")
    )
    port = urls[0].split(":")[-1]
    localhost = f"http://localhost:{port}"
    print(f"MaaFramework version: {UIBase.maafw_version}")
    print(f"{UIBase.name} version: {UIBase.version}({UIBase.version_type})")
    print(
        f"{UIBase.name} has been deployed on {port} port and ready to go on the link: {localhost} or http://0.0.0.0:{port}"
    )


main(language)
app.urls.on_change(ready)
ui.run(
    port=8020,  # Default deploy at 8020 port
    title=UIBase.name,
    dark=dark,
    show_welcome_message=False,
    show=show,
    reconnect_timeout=10,
)
