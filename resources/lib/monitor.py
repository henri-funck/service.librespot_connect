import xbmc

import player
import utils


class _Monitor(xbmc.Monitor):
    @utils.logged_method
    def __init__(self):
        next(player.PLAYER)

    @utils.logged_method
    def onSettingsChanged(self):
        utils.log("Settings changed")
        next(player.PLAYER)


def run():
    _Monitor().waitForAbort()
    player.PLAYER.close()
