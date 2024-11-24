import json
from pathlib import Path
from typing import Literal

from utils.tool.system import language, win32able


class Read:
    def __init__(self) -> None:
        configs_path: Path = Path(Path.cwd(), "config")
        if not configs_path.exists():
            configs_path.mkdir()
        self.ui_cofig_path = Path(configs_path, "ui_config.json")
        self.adbs_path = Path(configs_path, "adbs.json")
        self.win32s_path = Path(configs_path, "win32s.json")
        self.apps_path = Path(configs_path, "apps.json")
        if not self.ui_cofig_path.exists():
            with open(self.ui_cofig_path, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "dark": None,
                        "language": language,
                        "show": True,
                        "default_gpu": -1,
                        "run_toolkit": False,
                        "run_res": True,
                        "run_ctrl": True,
                        "run_tasker": True,
                        "show_adb": True,
                        "show_win32": win32able,
                    },
                    f,
                    indent=8,
                )
        for path in (self.adbs_path, self.win32s_path, self.apps_path):
            if not path.exists():
                with open(path, "w", encoding="utf-8") as f:
                    json.dump({}, f, indent=8)

    def ui_config(self) -> dict | None:
        if not self.ui_cofig_path.exists():
            return None
        with open(self.ui_cofig_path, "r", encoding="utf-8") as f:
            data: dict = json.load(f)
        return data

    def devices(self, target: Literal["adbs", "win32s", "apps"]) -> dict | int | None:
        if target == "adbs":
            path = self.adbs_path
        elif target == "win32s":
            path = self.win32s_path
        elif target == "apps":
            path = self.apps_path
        else:
            return 101
        if not path.exists():
            return 0
        with open(path, "r", encoding="utf-8") as f:
            data: dict = json.load(f)
            if data == {}:
                return None
        return data


class Wirte:
    def __init__(self) -> None:
        configs_path: Path = Path(Path.cwd(), "config")
        if not configs_path.exists():
            configs_path.mkdir()
        self.ui_cofig_path = Path(configs_path, "ui_config.json")
        self.adbs_path = Path(configs_path, "adbs.json")
        self.win32s_path = Path(configs_path, "win32s.json")
        self.apps_path = Path(configs_path, "apps.json")

    def json(
        self,
        target: Literal["ui_config", "add_device", "del_device", "add_app", "del_app"],
        kind: Literal["adb", "win32"] = "",
        data: dict = {},
        del_key: list[str] = [],
    ) -> int | None:
        if target == "ui_config":
            path = self.ui_cofig_path
        elif target == "add_device" or target == "del_device":
            if kind == "adb":
                path = self.adbs_path
            elif kind == "win32":
                path = self.win32s_path
            else:
                return 101
        elif target == "add_app" or target == "del_app":
            path = self.apps_path
        else:
            return 100

        if type(data) != dict:
            return 200

        if data == {}:
            n_keys = []
        else:
            n_keys = list(data.keys())

        with open(path, "r", encoding="utf-8") as f:
            originals: dict = json.load(f)
        if originals != {}:
            o_keys = list(originals.keys())
            for key in o_keys:
                if key not in n_keys:
                    data.update({key: originals[key]})
        if del_key:
            for d_k in del_key:
                statu = data.pop(str(d_k), False)
                if not statu:
                    return 103

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=8, ensure_ascii=False)


class FindDirs:
    def __init__(self) -> None:
        self.res_path = Path(f"{Path.cwd()}/res")

    def app(self) -> dict[Path, str] | None:
        apps = {}
        for i in self.res_path.iterdir():
            if i.is_dir():
                if Path(f"{i}/interface.json").exists():
                    apps.update({str(i): str(i.name)})
        if apps == {}:
            return None
        return apps
