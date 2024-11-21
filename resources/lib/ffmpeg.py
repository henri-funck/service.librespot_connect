import subprocess
import threading

import utils


def get_file():
    return f"rtp://127.0.0.1:{utils.get_setting('rtp_port')}"


class FFmpeg:
    @utils.logged_method
    def __init__(self):
        self._command = (
            f"ffmpeg"
            f" -hide_banner -nostats"
            f" -avioflags direct -fflags nobuffer -re"
            f" -f s16le -ac 2 -ar 44100 -channel_layout stereo -i -"
            f" -acodec pcm_s16be"
            f" -f rtp {get_file()}"
        ).split()

    @utils.logged_method
    def run(self, stdin):
        ffmpeg = subprocess.Popen(
            self._command,
            stdin=stdin,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        threading.Thread(target=utils.log_std, args=[ffmpeg.stdout]).start()
