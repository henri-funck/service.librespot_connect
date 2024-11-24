import xbmc

import player
import utils


class _Monitor(xbmc.Monitor):
    @utils.logged_method
    def __init__(self):
        self.player = player.get_player()
        next(self.player)

    @utils.logged_method
    def onSettingsChanged(self):
        utils.log("Settings changed")
        next(self.player)

    @utils.logged_method
    def run(self):
        self.waitForAbort()
        self.player.close()


def run():
    _Monitor().run()
