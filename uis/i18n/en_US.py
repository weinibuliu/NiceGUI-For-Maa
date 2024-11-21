from dataclasses import dataclass

default_infos = "**Adb Path**\n\nThe path of adb.exe that be used to connect\n\n.**Adb Address**\n\nThe adb connect address.For example,127.0.0.1:5555\n\n**Extras**\n\nThe params that implement screenshot enhancements.As of now,**ONLY** MuMu12 Player and LDPlayer needs to fill in."


@dataclass(frozen=True)
class Tabs:
    manage = "管理"
    setting = "设置"
    about = "关于"


@dataclass(frozen=True)
class Manage:
    class Button:
        add = "添加"
        delete = "删除"
        task = "任务"
        run = "运行"
        stop = "停止"


@dataclass(frozen=True)
class Setting:
    pass


@dataclass(frozen=-True)
class About:
    pass
