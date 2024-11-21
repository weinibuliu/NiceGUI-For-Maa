from dataclasses import dataclass


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


@dataclass(frozen=True)
class Setting:
    pass


@dataclass(frozen=-True)
class About:
    pass
