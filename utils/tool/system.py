import locale
import platform
from typing import Literal

# We DON'T upload infos below.
# We just show them on the debug page in ui in order to help user find the question faster.

_language = locale.getdefaultlocale()
language = "zh_CN"
if _language in ["zh_CN", "zh_TW", "en_US"]:
    language = _language

system_type: Literal["Linux", "Windows", "Darwin"]
system_type = platform.system()
system_name = platform.platform()
system_version = platform.version()
system_bit = platform.architecture()[0]

win32able = False
if system_type == "Windows":
    win32able = True
