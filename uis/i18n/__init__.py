from typing import List
from dataclasses import dataclass

from . import zh_CN, zh_TW, en_US

language_dict = {"zh_CN": "简体中文", "zh_TW": "繁體中文", "en_US": "English"}


def language_type(language: str = "zh_CN"):
    if language == "zh_CN":
        i18n = zh_CN
    elif language == "zh_TW":
        i18n = zh_TW
    elif language == "en_US":
        i18n = en_US
    else:  # If error,set zh_CN
        i18n = zh_CN
    return i18n
