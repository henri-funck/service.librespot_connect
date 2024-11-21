import time
import xbmc
import xbmcgui

import event_handler
import ffmpeg
import scheduler
import spotify
import utils


def _get_player():
    while True:
        with Player():
            yield


PLAYER = _get_player()


class Player(xbmc.Player):
    @utils.logged_method
    def __init__(self):
        self._dnd_kodi = utils.get_setting("dnd_kodi") == "true"
        self._event_handler = event_handler.EventHandler(self)
        self._scheduler = scheduler.Scheduler(self._event_handler.get_onevent())
        self._file = ffmpeg.get_file()
        self._list_item = xbmcgui.ListItem(path=self._file)
        self._list_item.setProperties(
            {
                "inputstream": "inputstream.ffmpeg",
            }
        )
        self._info_tag_music = self._list_item.getMusicInfoTag()
        self._is_paused = False
        self._is_playing_file = False
        if not self._dnd_kodi or not self.isPlaying():
            self._scheduler.start()

    @utils.logged_method
    def __enter__(self):
        return self

    @utils.logged_method
    def __exit__(self, *_):
        self.on_event_stopped()
        self._scheduler.exit()
        self._event_handler.exit()
        # The line below enables garbage collection of the player
        del self._event_handler

    def _on_playback_ended(self):
        is_playing_file = self._is_playing_file
        self._is_playing_file = False
        if is_playing_file:
            self._scheduler.restart()
        else:
            self._scheduler.start()

    @utils.logged_method
    def onAVStarted(self):
        if self.isPlaying and self.getPlayingFile() == self._file:
            self._is_playing_file = True
            self.on_playback_started()
        else:
            self._is_playing_file = False
            if self._dnd_kodi:
                self._scheduler.stop()
            else:
                self._scheduler.start()

    @utils.logged_method
    def onPlayBackEnded(self):
        self._on_playback_ended()

    @utils.logged_method
    def onPlayBackError(self):
        self._on_playback_ended()

    @utils.logged_method
    def onPlayBackStopped(self):
        self._on_playback_ended()

    def _seek(self, position=0.0, then=0.0, **_):
        if not self._is_paused:
            self.seekTime(position - then + time.time())

    @utils.logged_method
    def on_event_paused(self, **kwargs):
        if not self._is_paused:
            self._is_paused = True
            self.pause()

    @utils.logged_method
    def on_event_playing(self, position=0.0, then=0.0, **_):
        self._is_paused = False
        if self._is_playing_file:
            self._seek(position, then)
        else:
            self._position = position
            self._then = then
            self.play(self._file, self._list_item)

    @utils.logged_method
    def on_event_position_correction(self, **kwargs):
        self._seek(**kwargs)

    @utils.logged_method
    def on_event_seeked(self, **kwargs):
        self._seek(**kwargs)

    @utils.logged_method
    def on_event_stopped(self, **_):
        if self._is_playing_file:
            self._is_playing_file = False
            # The line below takes less time than self.stop()
            xbmc.executebuiltin("PlayerControl(stop)")

    @utils.logged_method
    def on_event_track_changed(
        self, album="", art="", artist="", duration=0, title="", **_
    ):
        fanart = spotify.get_fanart(art)
        self._list_item.setArt({"fanart": fanart, "thumb": art})
        self._info_tag_music.setAlbum(album)
        self._info_tag_music.setArtist(artist)
        self._info_tag_music.setDuration(duration)
        self._info_tag_music.setTitle(title)
        if self._is_playing_file:
            self.updateInfoTag(self._list_item)

    @utils.logged_method
    def on_playback_started(self):
        self._seek(self._position, self._then)
