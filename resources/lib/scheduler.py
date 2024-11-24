import threading

import librespot
import utils


class Scheduler:
    @utils.logged_method
    def __init__(self, onevent):
        self._librespot = librespot.Librespot(onevent)
        self._failures = 0
        self._max_failures = 5
        self._scheduler = self._schedule()
        self._process = None

    def _monitor(self):
        utils.log("Librespot started")
        with self._process as process:
            process.wait()
            if process.returncode < 0:
                self._failures = 0
            else:
                self._failures += 1
                self.restart()
        utils.log("Librespot stopped")

    def _schedule(self):
        while self._failures < self._max_failures:
            with self._librespot.run() as self._process:
                threading.Thread(target=self._monitor).start()
                try:
                    yield
                finally:
                    self._process.terminate()
                    self._process.wait()
        while True:
            yield

    @utils.logged_method
    def exit(self):
        self._scheduler.close()

    @utils.logged_method
    def restart(self):
        next(self._scheduler)

    @utils.logged_method
    def start(self):
        if self._process is None or self._process.poll() is not None:
            next(self._scheduler)

    @utils.logged_method
    def stop(self):
        if self._process is not None:
            self._process.terminate()
