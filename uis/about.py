from nicegui import ui

from uis.infos import UIBase, UIInfo, AppInfo
from uis.i18n import language_type


def main(language: str):
    i18n = language_type(language).About
    ui.markdown(
        f"""
        **{UIBase.name}**

        **{i18n.UI.version}: {UIBase.version} ({UIBase.version_type})**

        **基于 [NiceGUI](https://github.com/zauberzeug/nicegui) 开发的 [MaaFramework](https://github.com/MaaXYZ/MaaFramework) 通用UI**

        ****

        **[{i18n.UI.repo}]({UIInfo.repo_url}) | [{i18n.UI.issue}]({UIInfo.issue_url}) | [{i18n.UI.release}]({UIInfo.release_url})**
        """
    )
    if AppInfo.enable:
        ui.markdown(
            f"""
            **{i18n.App.name}: {AppInfo.name}**

            **{i18n.App.version}: {AppInfo.version} ({AppInfo.version_type})**

            **{AppInfo.brief}**

            ****

            **[{i18n.App.repo}]({AppInfo.repo_url}) | [{i18n.App.issue}]({AppInfo.issue_url}) | [{i18n.App.release}]({AppInfo.release_url})**
            """
        )
