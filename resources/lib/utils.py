import os
import subprocess
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

_ADDON_HOME = xbmcvfs.translatePath(xbmcaddon.Addon().getAddonInfo("profile"))
_ADDON_ICON = xbmcaddon.Addon().getAddonInfo("icon")
_ADDON_NAME = xbmcaddon.Addon().getAddonInfo("name")
_ADDON_PATH = xbmcaddon.Addon().getAddonInfo("path")
_DIALOG = xbmcgui.Dialog()
_SETTINGS = {
    "dnd_kodi": "false",
    "loginfo": "false",
    "max_failures": "5",
    "name": "LibrespotConnect@{}",
    "rtp_port": "45654",
}

os.environ["PATH"] += os.pathsep + os.path.join(_ADDON_PATH, "bin")
os.makedirs(_ADDON_HOME, exist_ok=True)
os.chdir(_ADDON_HOME)


def get_setting(key):
    setting = xbmcaddon.Addon().getSetting(key)
    return setting if setting else _SETTINGS[key]


_LOG_LEVEL = xbmc.LOGINFO if get_setting("loginfo") == "true" else xbmc.LOGDEBUG


def log(message, notify=False):
    xbmc.log(f"{_ADDON_NAME}: {message}", _LOG_LEVEL)
    if notify:
        notification(message)


def log_std(std):
    for line in std:
        log(line.rstrip())


def logged_method(method):
    def logger(*args, **kwargs):
        log(f"{method.__module__}.{method.__qualname__}")
        return method(*args, **kwargs)

    return logger


def notification(
    message="", heading=_ADDON_NAME, icon=_ADDON_ICON, sound=False, time=5000
):
    _DIALOG.notification(heading, message, icon, time, sound)


def test_program(command):
    try:
        command = command.split()
        subprocess.run(command, check=True)
    except:
        log(f"Deficient {command[0]}, aborting", True)
        raise SystemExit()
