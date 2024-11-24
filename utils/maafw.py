# Based on MaaFW Version: 2.2.2

import json
from pathlib import Path
from typing import Literal

from asyncify import asyncify
from maa.tasker import Tasker
from maa.resource import Resource
from maa.toolkit import Toolkit, AdbDevice, DesktopWindow
from maa.controller import AdbController, Win32Controller
from maa.define import MaaAdbScreencapMethodEnum, MaaAdbInputMethodEnum

from utils import custom  # Custom support


class Find:
    @asyncify
    def adb() -> list[AdbDevice] | None:
        raw_adbs = Toolkit.find_adb_devices()
        if raw_adbs == []:
            return None

        adbs: list[AdbDevice] = []
        adbs_address = []
        for adb in raw_adbs:
            if adb.address not in adbs_address:
                adbs.append(adb)
                adbs_address.append(adb.address)
        return adbs

    @asyncify
    def win32() -> list[DesktopWindow]:
        raw_wins: list[DesktopWindow] = Toolkit.find_desktop_windows()
        return raw_wins


@asyncify
def connect_adb(
    adb_path: str | Path,
    address: str,
    screencap_method: int = 0,
    input_method: int = 0,
    config: dict = {},
) -> AdbController | None:
    if screencap_method <= -1:
        screencap_method = MaaAdbScreencapMethodEnum.Default
    if input_method <= -1:
        input_method = MaaAdbInputMethodEnum.Default
    controller = AdbController(
        adb_path, address, screencap_method, input_method, config
    )
    statu = controller.post_connection().wait().succeeded()

    if statu:
        return controller
    else:
        return None


@asyncify
def connect_win32(
    hwnd,
    screencap_method: int = 0,
    input_method: int = 0,
    notification_handler=None,
) -> Win32Controller | None:
    if screencap_method <= -1:
        screencap_method = 4  # DXGI_DesktopDup
    if input_method <= -1:
        input_method = 1  # Seize
    controller = Win32Controller(
        hwnd, screencap_method, input_method, notification_handler
    )
    statu = controller.post_connection().wait().succeeded()

    if statu:
        return controller
    else:
        return None


@asyncify
def init_toolkit(path: Path = Path.cwd()) -> int | None:
    statu = Toolkit.init_option(path)
    if not statu:
        return 0


@asyncify
def load_resource(
    res_path: list[str],
    app_path: str | Path,
    app_name: str | None = None,
    gpu_id: int = -2,
) -> Resource | int:
    resource = Resource()
    # Check gpu id.If gpu id is wrong,disable gpu.
    if type(gpu_id) != int or gpu_id < -2 or gpu_id == -2:
        gpu_statu = resource.set_cpu()
        if not gpu_statu:
            return -2
    elif gpu_id == -1:
        gpu_statu = resource.set_auto_device()
        if not gpu_statu:
            return -1
    else:
        gpu_statu = resource.set_gpu(gpu_id)
        if not gpu_statu:
            return 400 + gpu_id  # return 40x,the x means gpu id selected.
    for res in res_path:
        res = Path(res.replace("{PROJECT_DIR}", str(app_path)))
        if not res.exists():
            return f"100: {str(res)}"
        resource.post_path(res).wait()
    Custom = None
    if app_name is not None:
        if app_name == "Sample":
            Custom = custom.Sample
    if Custom is not None:
        rec: dict
        act: dict
        for rec in Custom.recs:
            statu = None
            if type(rec) == dict:
                rec = list(rec.items())[0]
                if len(rec) != 2:
                    return 300
                rec_name = rec[0]
                rec_cls = res[1]
                statu = resource.register_custom_recognition(rec_name, rec_cls)
                if not statu:
                    return 301
        for act in Custom.acts:
            statu = None
            if type(act) == dict:
                act = list(rec.items())[0]
                if len(act) != 2:
                    return 310
                act_name = act[0]
                act_cls = act[1]
                statu = resource.register_custom_action(act_name, act_cls)
                if not statu:
                    return 311
    return resource


@asyncify
def bind_tasker(res: Resource, ctrl: AdbController | Win32Controller) -> int | Tasker:
    tasker = Tasker()
    statu = tasker.bind(res, ctrl)
    if not statu:
        return 0
    if not tasker.inited:
        return 1
    return tasker


@asyncify
def run_task(tasker: Tasker, tasks: list[dict]) -> int | bool:
    if tasks == []:
        return 200
    for task in tasks:
        entry: str = task["entry"]
        option: dict = task["pipeline_override"]
        option_key = option.keys()
        override = {}
        for o_k in option_key:
            override.update(option[o_k])
        if type(entry) != str or type(override) != dict:
            return 1
        statu = tasker.post_pipeline(entry, override).wait().get()
        if not statu:
            return 0
    return True


@asyncify
def stop_task(tasker: Tasker) -> bool:
    if not tasker:
        return
    statu = tasker.post_stop().wait()
    if not statu:
        return False
    return True


class ReadInterface:
    def __init__(self, app_path: str | Path) -> None:
        interface_path = Path(f"{str(app_path)}/interface.json")
        with open(interface_path, "r", encoding="utf-8") as f:
            self.data: dict = json.load(f)
            self.keys: list[str] = list(self.data.keys())

    def get_all(self) -> dict:
        return self.data

    def get_str(self, target: Literal["author", "version", "messgae", "url"]) -> str:
        if target not in self.keys or self.data[target] == "":
            return "Unknown"
        return self.data[target]

    def get_resource(self) -> dict[str, str] | int:
        if "resource" not in self.keys:
            return 0
        res: list[dict] = self.data["resource"]
        r_dict = {}
        for r in res:
            if "name" not in r.keys() or "path" not in r.keys():
                return -1
            r_name: str = r["name"]
            r_path: list[str] = r["path"]
            r_dict.update({str(r_path): r_name})
        return r_dict

    def get_task(self) -> dict[str, str]:
        if "task" not in self.keys:
            return 0
        tasks: list[dict] = self.data["task"]
        task_dict = {}
        i = 0
        for task in tasks:
            name: str = task["name"]
            entry: str = task["entry"]
            if "option" not in task.keys() or task["option"] == {}:
                option = None
            else:
                option: list[str] = task["option"]
            task_dict.update({f"{i}@@@{name}@@@{entry}@@@{option}@@@ ": name})
            i += 1
        return task_dict

    def get_option(self) -> dict[str, str]:
        if "option" not in self.keys or type(self.data["option"]) != dict:
            return {}
        options = self.data["option"]
        option_keys = options.keys()
        option_dict = {}
        for o_k in option_keys:
            option = options[o_k]["cases"]
            o_d = {}
            i = 0
            for o in option:
                name: str = o["name"]
                override: dict = o["pipeline_override"]
                o_d.update({f"{o_k}@@@{override}@@@{i}": name})
                i += 1
            option_dict.update(o_d)
        return option_dict
