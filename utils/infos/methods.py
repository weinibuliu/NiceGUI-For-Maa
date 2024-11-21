# MAAFW Screencap and Input Methods infos.
from dataclasses import dataclass

# In fact, 0 doesn't mean Defalut.
# If you want to set "Default" in other Python exe,you should keep the param as func's default param.


@dataclass(frozen=True)
class Methods:
    class Adb:
        screen: dict[int, str] = {
            -1: "Default",
            0: "Null",
            1: "EncodeToFileAndPull",
            2: "Encode",
            4: "RawWithGzip",
            8: "RawByNetcat",
            16: "MinicapDirect",
            32: "MinicapStream",
            64: "EmulatorExtras",
        }
        input: dict[int, str] = {
            -1: "Default",
            0: "Null",
            1: "AdbShel",
            2: "MinitouchAndAdbKey",
            4: "Maatouch",
            8: "EmulatorExtras",
        }

    class Win32:
        screen: dict[int, str] = {
            -1: "Default",
            0: "Null",
            1: "Screencap_GDI",
            2: "Screencap_FramePool",
            4: "Screencap_DXGI_DesktopDup",
        }
        input: dict[int, str] = {
            -1: "Default",
            0: "Null",
            1: "Input_Seize",
            2: "Input_SendMessage",
        }
