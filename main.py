# MaaFw 启动入口

from pathlib import Path

from maa.resource import Resource
from maa.controller import AdbController
from maa.tasker import Tasker
from maa.toolkit import Toolkit


from utils.tool import Find, Connect

# 获取脚本运行路径
main_path = Path.cwd()


def main(
    tasks: list[dict] = {},
    res_paths: list[Path] = "",
    connect_kind: str = "Adb",
    connect_config: dict = {},
):
    # 处理跨平台路径问题
    user_path = Path(f"{main_path}/cache")
    res_path = Path(res_path)
    adb_path = Path(adb_path)

    # Toolkit 初始化
    Toolkit.init_option(user_path)

    # 加载资源
    resource = Resource()
    resource.post_path(res_path).wait()

    # Controller 初始化
    # TODO

    # Tasker 初始化
    tasker = Tasker()
    tasker.bind(resource, controller)
    if not tasker.inited:
        print("Failed to init.")
        exit()

    # 执行任务
    for task in tasks:
        tasker.post_pipeline(task["entry"], task["pipeline_override"]).wait().get()


if __name__ == "__main__":
    main()
