from typing import Literal
from dataclasses import dataclass

from maa import ver as maaver


@dataclass(frozen=True)
class UIBase:  # Infos below will affect the whole UI(For example,the website title).
    name: str = "NiceGUI For MaaFW"
    version: str = "2.0.0"
    version_type: Literal["Stable", "Pre-Release", "Alpha", "Beta", "Cannary"] = (
        "Pre-Release"
    )
    maafw_version: str = maaver


@dataclass(frozen=True)
class UIInfo:  # Infos below will show on about page.
    enable: bool = True  # Whether show on about page.
    # Github API.Set value as None to disable update check.
    update_api: str | None = None
    repo_url: str = "https://github.com/weinibuliu/NiceGUI-For-Maa"
    issue_url: str = "https://github.com/weinibuliu/NiceGUI-For-Maa/issues"
    release_url: str = "https://github.com/weinibuliu/NiceGUI-For-Maa/releases"


@dataclass(frozen=True)
# Dont'delete ANY variable below.You can set them as "" or None.
class AppInfo:  # Infos below will show on about page.
    enable: bool = True  # Whether show  on about page.
    # Github API.Set value as None to disable update check.
    update_api: str | None = None
    name: str = "Sample"
    version: str = "0.1.0"
    version_type: Literal["Stable", "Pre-Release", "Alpha", "Beta", "Cannary"] = (
        "Stable"
    )
    brief: str = "Your App brief."
    repo_url: str = ""
    issue_url: str = ""
    release_url: str = ""
