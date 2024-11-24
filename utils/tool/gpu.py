import subprocess

from .system import system_type
from uis.i18n import language_type


def get_gpu(language: str, system: str = system_type) -> dict[int, str] | None:
    i18n = language_type(language).Setting.Maa
    gpus = {-2: i18n.gpu_disable, -1: i18n.gpu_auto}
    # Windows
    if system == "Windows":
        gpu_ids = subprocess.check_output(
            "wmic path win32_videocontroller get deviceid", shell=True, text=True
        )
        gpu_names = subprocess.check_output(
            "wmic path win32_videocontroller get name", shell=True, text=True
        )
        gpu_ids = gpu_ids.strip().split("\n")[2:]
        gpu_names: str = gpu_names.strip().split("\n")[2:]
        for id, name in zip(gpu_ids, gpu_names):
            id = int(id.split("r")[-1])  # id will like VideoController1
            id -= 1
            gpus.update({id: name})
        return gpus
    else:
        return None
