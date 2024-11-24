import socket
import subprocess
import threading

import ffmpeg
import utils

utils.test_program("librespot --version")


class Librespot:
    @utils.logged_method
    def __init__(self, onevent):
        name = utils.get_setting("name").format(socket.gethostname())
        self._command = [
            "librespot",
            "--backend", "pipe",
            "--bitrate", "320",
            "--device-type", "tv",
            "--disable-audio-cache",
            "--disable-credential-cache",
            "--name", name,
            "--onevent", onevent,
            "--quiet",
        ]
        self._ffmpeg = ffmpeg.FFmpeg()

    @utils.logged_method
    def run(self):
        librespot = subprocess.Popen(
            self._command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        threading.Thread(target=lambda: utils.log_std(librespot.stderr)).start()
        self._ffmpeg.run(librespot.stdout)
        return librespot
