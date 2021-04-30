import time

class Timer:
    def __init__(self, timeInSeconds, timeoutAction):
        self._timerValue = timeInSeconds
        self._startTime = self._currentTime()
        self._timeoutAction = timeoutAction

    def _currentTime(self):
        return int(time.time())

    def setTime(self, time):
        self._timerValue = time

    def _isTimeout(self):
        if self._startTime + self._timerValue < self._currentTime():
            self._startTime = self._currentTime()
            return True
        else:
            return False

    def performActionIfTimeout(self):
        if self._isTimeout():
            self._timeoutAction()