import threading
from mouseControl import MouseCoordinator
from timeControl import Timer

class MouseCoordinatorThread(threading.Thread):
    def __init__(self, time):
        threading.Thread.__init__(self)
        self._id = 1
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._mouseCoordinator = MouseCoordinator()
        self._timer = Timer(time, self._mouseCoordinator.shadowMouseMove)

    def _acquireLock(self):
        self._lock.acquire()

    def _releaseLock(self):
        self._lock.release()

    def updateTime(self, newTime):
        self._acquireLock()
        self._timer.setTime(newTime)
        self._releaseLock()

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            self._acquireLock()
            self._timer.performActionIfTimeout()
            self._releaseLock()