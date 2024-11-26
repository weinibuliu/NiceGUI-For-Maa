from dataclasses import dataclass

from uis.infos import UIBase


@dataclass(frozen=True)
class Tabs:
    manage = "Manage"
    setting = "Setting"
    about = "About"


@dataclass(frozen=True)
class Manage:
    class Button:
        add = "Add"
        update = "Refresh"
        delete = "Delete"
        task = "Task"
        connect = "Connect"
        run = "Run"
        stop = "Stop"

    class Add:
        adb_auto = "Auto"
        adb_manual = "Manual"
        win32_select = "Select"

        class Adb:
            class Auto:
                select = "Adb Device"
                search = "Search"
                save = "Save"

            class Manual:
                name = "Device Name（Optional）"
                path = "Adb Path"
                address = "Adb Address"
                extras = "Extras"
                tooltip = "If you dont't know how to fill it,please keep it as {}"
                advance = "Advance"
                save = "Save"
                warning = "Changing the options below may cause some exceptions!"
                screencap_methods = "Screencap"
                input_methods = "Input"
                undefined = "Unknown Device"

            class Notify:
                saved = "Save successfully."
                unsaved = "Save unsuccessfully."

            class Notification:
                searching = "Searching..."
                found = "Searching successfully."
                unfound = "Adb device not found."
                use = "Use Time"

            class ShowInfos:
                # private
                _standard = __standard = (
                    "**Adb Path**\n\nPATH\n\n**Adb Address**\n\nADDRESS\n\n**Extras**\n\nEXTRAS"
                )
                _default_path = (
                    "The path to the adb.exe file used to connect to the device."
                )
                _default_address = "The Adb device address to connect to (usually something like 127.0.0.1:16384)."
                _default_extras = "Parameters required to implement screenshot enhancement mode. As of now, **only** MuMu12/Leidian Player need to be filled in. For other players, please keep it as {}"
                _default = (
                    _standard.replace("PATH", _default_path)
                    .replace("ADDRESS", _default_address)
                    .replace("EXTRAS", _default_extras)
                )

                # public
                default = _default
                standard = __standard

        class Win32:
            search = "Search"
            save = "Save"
            advance = "Advance"
            warning = "Changing the options below may cause some exceptions!"

            class Notify:
                saved = "Save successfully."
                unsaved = "Save unsuccessfully."

            class Notification:
                searching = "Searching..."
                found = "Searching successfully."
                unfound = "Window not found."
                use = "Use Time"

    class Delete:
        ensure = "Are you sure you want to **delete the selected data**?"
        del_yes = "Confirm"
        del_no = "Cancel"
        success = "Delete successfully."
        faild = "Delete unsuccessfully."

    class Config:
        config = "Config"
        app = "App"
        task = "Task"

        class Dialog:
            app_select = "App"
            res_select = "Resource"
            app_author = "APP Author"
            app_version = "App Version"
            app_meaasge = "Application Introduction"
            app_url = "App Url"
            to_task = "To Task"

            task_select = "Task"
            task_name = "Task Name"
            task_option = "Task Option"

            add = "Add"
            delete = "Delete"
            save = "Save"
            update = "Refresh"

            config_name = "Config Name"
            _continue = "Continue"
            cancel = "Cancel"

            class Notify:
                updated = "Refresh successfully."
                error = "Error"
                noapps = "Read App list unsuccessfully"
                option_name_error = " Option Error.Please contact with App Author."
                option_out_range = f"Option number is out of range.Please try to update UI or go to the UI issue page feedback.(Current UI Version :{UIBase.version})"
                added = "Add successfully."
                unadded = "Add unsuccessfully."
                deleted = "Delete successfully."
                undeleted = "Delete unsuccessfully."
                saved = "Save successfully."
                unsaved = "Save unsuccessfully."

    class Update:
        # notify = "Refresh successfully."
        None

    class Connect:
        result = "Connect Result"

        class Notify:
            connected = "Connect successfully."
            unconneted = "Connect unsuccessfully."

    class Run:
        appname = "App Name"
        configname = "Config Name"
        create_time = "Create Time"
        undefined = "Undefined"

        class Button:
            run = "Run"
            update = "Refresh"
            delete = "Delete"
            start = "Start"
            stop = "Stop"

        class Notify:
            deleted = "Delete successfully."
            undeleted = "Delete unsuccessfully."
            updated = "Refresh successfully."
            unupdated = "Refresh unsuccessfully."
            error = "Error"
            toolkited = "Toolkit initialized."
            untoolkited = "Toolkit uninitialized"
            connected = "Controller connected"
            unconneted = "Controller unconnected."
            resed = "Resource loaded."
            unresed = "Resource unloaded."
            taskered = "Tasker binded."
            untaskered = "Tasker unbinded."
            doing = "Task running..."
            done = "Task succeed."
            undone = "Task failed."
            stopped = "Task stopped."
            unstopped_tasker = "Stop Failed: Tasker not exist.。"
            unstopped = "Stop Failed."

    class Device:
        class Adb:
            sample = "Adb Sample"
            name = "Device Name"
            path = "Adb Path"
            address = "Adb Address"
            task = "Task"
            updated = "Adb table updated."
            uninited = "Adb table uninitialized."
            unupdated = "Adb table unupdated."

        class Win32:
            name = "Window Name"
            hwnd = "HWND"
            task = "Task"
            updated = "Win32 table updated."
            uninited = "Win32 table uninitialized."
            unupdated = "Win32 table unupdated."


@dataclass(frozen=True)
class Setting:
    class Language:
        language = "Language"
        notify = "The UI will restart to complete the changes."
        notify_en = "The UI will restart to complete the changes."

    class Dark:
        dark = "Dark Theme"
        dark_dict = {None: "System", False: "Light Theme", True: "Dark Theme"}
        notify = "The UI will restart to complete the changes."

    class Notify:
        notify = "Runtime Notify Setting"
        toolkit = "Toolkit initialize"
        resource = "Resource load"
        controller = "Controller connect"
        tasker = " Tasker Bind"

    class Startup:
        startup = "Startup"
        show = "Automatically open the page in browser"
        guide = "Enable the boot page (Restart to take effect)"

    class Reload:
        reload = "Restart UI"
        notify = "UI will restart..."


@dataclass(frozen=-True)
class About:
    class UI:
        repo = "Repository"
        issue = "Feedback"
        release = "Check Update"
        version = "Current Version"

    class App:
        name = "App Name"
        repo = "Repository"
        issue = "Feeedback"
        release = "Check Update"
        version = "Current Version"
