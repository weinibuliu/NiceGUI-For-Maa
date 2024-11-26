from dataclasses import dataclass

from uis.infos import UIBase


@dataclass(frozen=True)
class Tabs:
    manage = "管理"
    setting = "設定"
    about = "關於"


@dataclass(frozen=True)
class Manage:
    class Button:
        add = "添加"
        update = "刷新"
        delete = "刪除"
        task = "任務"
        connect = "連接"
        run = "運行"
        stop = "停止"

    class Add:
        adb_auto = "自動搜尋"
        adb_manual = "手動填寫"
        win32_select = "選擇"

        class Adb:
            class Auto:
                select = "Adb 設備"
                search = "搜尋"
                save = "儲存"

            class Manual:
                name = "設備名稱（選填）"
                path = "Adb 路徑"
                address = "Adb 地址"
                extras = "額外參數"
                tooltip = "如果你不清楚如何填入該項，請保持其為 {} 。"
                advance = "進階選項"
                save = "儲存"
                warning = "改變下面的選項可能會引發某些異常！"
                screencap_methods = "截圖模式"
                input_methods = "控制模式"
                undefined = "未命名設備"

            class Notify:
                saved = "儲存成功"
                unsaved = "儲存失敗"

            class Notification:
                searching = "搜尋中……"
                found = "搜尋成功"
                unfound = "未找到 Adb 設備"
                use = "使用時間"

            class ShowInfos:
                # private
                _standard = __standard = (
                    "**Adb 路徑**\n\nPATH\n\n**Adb 地址**\n\nADDRESS\n\n**額外參數**\n\nEXTRAS"
                )
                _default_path = "用於連接設備的 adb.exe 檔案路徑。"
                _default_address = "連接的 Adb 設備地址（通常形如 127.0.0.1:16384 ）。"
                _default_extras = "實現截圖增強模式所需的參數。截至目前，**只有** MuMu12 模擬器與雷電模擬器需要填寫。其他模擬器請保持為 {} 。"
                _default = (
                    _standard.replace("PATH", _default_path)
                    .replace("ADDRESS", _default_address)
                    .replace("EXTRAS", _default_extras)
                )

                # public
                default = _default
                standard = __standard

        class Win32:
            search = "搜尋"
            save = "儲存"
            advance = "進階選項"
            warning = "改變下面的選項可能會引發某些異常！"

            class Notify:
                saved = "儲存成功"
                unsaved = "儲存失敗"

            class Notification:
                searching = "搜尋中……"
                found = "搜尋成功"
                unfound = "未找到 Windows 視窗"
                use = "使用時間"

    class Delete:
        ensure = "確定 **刪除所選資料** 嗎？"
        del_yes = "確認"
        del_no = "取消"
        success = "删除成功。"
        faild = "删除失敗！"

    class Config:
        config = "配置"
        app = "應用"
        task = "任務"

        class Dialog:
            app_select = "選擇應用"
            res_select = "選擇资源"
            app_author = "應用作者"
            app_version = "應用版本"
            app_meaasge = "應用介紹"
            app_url = "應用連結"
            to_task = "前往任務介面"

            task_select = "選擇任務"
            task_name = "任務名稱"
            task_option = "任務選項"

            add = "添加"
            delete = "删除"
            save = "儲存"
            update = "刷新"

            config_name = "配置名稱"
            _continue = "繼續"
            cancel = "取消"

            class Notify:
                updated = "刷新成功。"
                error = "內部錯誤。"
                noapps = "應用清單讀取異常"
                option_name_error = " 選項异常，请聯繫應用開發者。"
                option_out_range = f"選項數量超出範圍。請嘗試更新 UI 版本或前往 UI 倉庫 issue 回饋。 (當前UI 版本 :{UIBase.version})"
                added = " 任務添加成功。"
                unadded = "任務添加失敗。"
                deleted = "任務删除成功。"
                undeleted = "任務删除失敗。"
                saved = "儲存成功。"
                unsaved = "儲存失敗。"

    class Update:
        # notify = "刷新成功。"
        None

    class Connect:
        result = "連接结果"

        class Notify:
            connected = "連接成功。"
            unconneted = "連接失敗。"

    class Run:
        appname = "應用名稱"
        configname = "配置名稱"
        create_time = "創建時間"
        undefined = "未定義"

        class Button:
            run = "運行"
            update = "刷新"
            delete = "删除"
            start = "開始"
            stop = "停止"

        class Notify:
            deleted = "配置删除成功。"
            undeleted = "配置删除失敗。"
            updated = "刷新成功。"
            unupdated = "刷新失敗。"
            error = "內部錯誤。"
            toolkited = "Toolkit 初始化成功。"
            untoolkited = "Toolkit 初始化失敗。"
            connected = "控制器連接成功。"
            unconneted = "控制器連接失敗。"
            resed = "載入资源成功。"
            unresed = "載入资源失敗。"
            taskered = "Tasker 建構成功。"
            untaskered = "Tasker 建構失敗。"
            doing = "任務正在執行……"
            done = "任務執行完成。"
            undone = "任務執行失敗"
            stopped = "任務成功終止。"
            unstopped_tasker = "終止失敗: Tasker 不存在。"
            unstopped = "終止失敗。"

    class Device:
        class Adb:
            sample = "Adb 示例"
            name = "設備名稱"
            path = "Adb 路径"
            address = "Adb 地址"
            task = "任務"
            updated = "Adb 清單更新成功"
            uninited = "Adb 清單初始化失敗。"
            unupdated = "Adb 清單更新失敗。"

        class Win32:
            name = "視窗名稱"
            hwnd = "視窗句柄"
            task = "任務"
            updated = "Win32 清單更新成功。"
            uninited = "Win32 清單初始化失敗。"
            unupdated = "Win32 清單更新失敗。"


@dataclass(frozen=True)
class Setting:
    class Language:
        language = "顯示語言"
        notify = "UI 即將重啟以完成更改。"
        notify_en = "The UI will restart to complete the changes."

    class Dark:
        dark = "明暗主題"
        dark_dict = {None: "跟隨系統", False: "亮色主題", True: "深色主題"}
        notify = "UI 即將重启以完成更改。"

    class Maa:
        maa = "MaaFramework 設定"
        version = "MaaFw 版本: "
        gpu_select = "GPU 加速"
        gpu_disable = "禁用（使用 CPU）"
        gpu_auto = "自動選擇"

    class RunNotify:
        notify = "運行时通知設定"
        toolkit = "Toolkit 初始化"
        resource = "资源載入"
        controller = "控制器連接"
        tasker = " Tasker 建構"

    class Startup:
        startup = "啟動时設定"
        show = "自動使用預設瀏覽器開啟頁面"
        guide = "啟用引导页（重啟 UI 后生效）"

    class Reload:
        reload = "重啟 UI"
        notify = "UI 即將重啟……"


@dataclass(frozen=-True)
class About:
    class UI:
        repo = "倉庫地址"
        issue = "問題回饋"
        release = "檢查更新"
        version = "目前版本"

    class App:
        name = "應用名稱"
        repo = "倉庫地址"
        issue = "問題回饋"
        release = "檢查更新"
        version = "目前版本"
