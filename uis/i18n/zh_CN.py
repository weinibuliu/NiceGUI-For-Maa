from dataclasses import dataclass

from uis.infos import UIBase


@dataclass(frozen=True)
class Tabs:
    manage = "管理"
    setting = "设置"
    about = "关于"


@dataclass(frozen=True)
class Manage:
    class Button:
        add = "添加"
        update = "刷新"
        delete = "删除"
        task = "任务"
        connect = "连接"
        run = "运行"
        stop = "停止"

    class Add:
        adb_auto = "自动搜索"
        adb_manual = "手动填写"
        win32_select = "选择"

        class Adb:
            class Auto:
                select = "Adb 设备"
                search = "搜索"
                save = "保存"

            class Manual:
                name = "设备名称（选填）"
                path = "Adb 路径"
                address = "Adb 地址"
                extras = "额外参数"
                tooltip = "如果你不清楚如何填写该项，请保持其为 {} 。"
                advance = "高级选项"
                save = "保存"
                warning = "改变下面的选项可能会引发某些异常！"
                screencap_methods = "截图模式"
                input_methods = "控制模式"
                undefined = "未命名设备"

            class Notify:
                saved = "保存成功"
                unsaved = "保存失败"

            class Notification:
                searching = "搜索中……"
                found = "搜索成功"
                unfound = "未找到 Adb 设备"
                use = "使用时间"

            class ShowInfos:
                # private
                _standard = __standard = (
                    "**Adb 路径**\n\nPATH\n\n**Adb 地址**\n\nADDRESS\n\n**额外参数**\n\nEXTRAS"
                )
                _default_path = "用于连接设备的 adb.exe 文件路径。"
                _default_address = "连接的 Adb 设备地址（通常形如 127.0.0.1:16384 ）。"
                _default_extras = "实现截图增强模式所需的参数。截至目前，**只有** MuMu12 模拟器与雷电模拟器需要填写。其他模拟器请保持为 {} 。"
                _default = (
                    _standard.replace("PATH", _default_path)
                    .replace("ADDRESS", _default_address)
                    .replace("EXTRAS", _default_extras)
                )

                # public
                default = _default
                standard = __standard

        class Win32:
            search = "搜索"
            save = "保存"
            advance = "高级选项"
            warning = "改变下面的选项可能会引发某些异常！"

            class Notify:
                saved = "保存成功"
                unsaved = "保存失败"

            class Notification:
                searching = "搜索中……"
                found = "搜索成功"
                unfound = "未找到 Windows 窗口"
                use = "使用时间"

    class Delete:
        ensure = "确定 **删除所选数据** 吗？"
        del_yes = "确认"
        del_no = "取消"
        success = "删除成功。"
        faild = "删除失败！"

    class Config:
        config = "配置"
        app = "应用"
        task = "任务"

        class Dialog:
            app_select = "选择应用"
            res_select = "选择资源"
            app_author = "应用作者"
            app_version = "应用版本"
            app_meaasge = "应用介绍"
            app_url = "应用链接"
            to_task = "前往任务界面"

            task_select = "选择任务"
            task_name = "任务名称"
            task_option = "任务选项"

            add = "添加"
            delete = "删除"
            save = "保存"
            update = "刷新"

            config_name = "配置名称"
            _continue = "继续"
            cancel = "取消"

            class Notify:
                updated = "刷新成功。"
                error = "内部错误。"
                noapps = "应用列表读取异常。"
                option_name_error = " 选项异常，请联系应用开发者。"
                option_out_range = f"选项数量超出范围。请尝试更新 UI 版本或前往 UI 仓库 issue 反馈。(当前UI 版本 :{UIBase.version})"
                added = " 任务添加成功。"
                unadded = "任务添加失败。"
                deleted = "任务删除成功。"
                undeleted = "任务删除失败。"
                saved = "保存成功。"
                unsaved = "保存失败。"

    class Update:
        # notify = "刷新成功。"
        None

    class Connect:
        result = "连接结果"

        class Notify:
            connected = "连接成功。"
            unconneted = "连接失败。"

    class Run:
        appname = "应用名称"
        configname = "配置名称"
        create_time = "创建时间"
        undefined = "未定义"

        class Button:
            run = "运行"
            update = "刷新"
            delete = "删除"
            start = "开始"
            stop = "停止"

        class Notify:
            deleted = "配置删除成功。"
            undeleted = "配置删除失败。"
            updated = "刷新成功。"
            unupdated = "刷新失败。"
            error = "内部错误。"
            toolkited = "Toolkit 初始化成功。"
            untoolkited = "Toolkit 初始化失败。"
            connected = "控制器连接成功。"
            unconneted = "控制器连接失败。"
            resed = "加载资源成功。"
            unresed = "加载资源失败。"
            taskered = "Tasker 构建成功。"
            untaskered = "Tasker 构建失败。"
            doing = "任务正在执行……"
            done = "任务执行完成。"
            undone = "任务执行失败"
            stopped = "任务成功终止。"
            unstopped_tasker = "终止失败: Tasker 不存在。"
            unstopped = "终止失败。"

    class Device:
        class Adb:
            sample = "Adb 示例"
            name = "设备名称"
            path = "Adb 路径"
            address = "Adb 地址"
            task = "任务"
            updated = "Adb 列表更新成功"
            uninited = "Adb 列表初始化失败。"
            unupdated = "Adb 列表更新失败。"

        class Win32:
            name = "窗口名称"
            hwnd = "窗口句柄"
            task = "任务"
            updated = "Win32 列表更新成功。"
            uninited = "Win32 列表初始化失败。"
            unupdated = "Win32 列表更新失败。"


@dataclass(frozen=True)
class Setting:
    class Language:
        language = "显示语言"
        notify = "UI 即将重启以完成更改。"
        notify_en = "The UI will restart to complete the changes."

    class Dark:
        dark = "明暗主题"
        dark_dict = {None: "跟随系统", False: "亮色主题", True: "深色主题"}
        notify = "UI 即将重启以完成更改。"

    class Maa:
        maa = "MaaFramework 设置"
        version = "MaaFw 版本: "
        gpu_select = "GPU 加速"
        gpu_disable = "禁用（使用 CPU）"
        gpu_auto = "自动选择"

    class RunNotify:
        notify = "运行时通知设置"
        toolkit = "Toolkit 初始化"
        resource = "资源加载"
        controller = "控制器连接"
        tasker = " Tasker 构建"

    class Startup:
        startup = "启动时设置"
        show = "自动使用默认浏览器打开页面"
        guide = "启用引导页（重启 UI 后生效）"

    class Reload:
        reload = "重启 UI"
        notify = "UI 即将重启……"


@dataclass(frozen=-True)
class About:
    class UI:
        repo = "仓库地址"
        issue = "问题反馈"
        release = "检查更新"
        version = "当前版本"

    class App:
        name = "应用名称"
        repo = "仓库地址"
        issue = "问题反馈"
        release = "检查更新"
        version = "当前版本"
