import pyautogui

pyautogui.FAILSAFE = False
CURSOR_MOVE_DISTANCE = 1

class MouseCoordinator:
    def __init__(self, testMode=False):
        self.yLastMoveOpposite = False
        self.xLastMoveOpposite = False
        self.testMode = testMode

    def _getBoudaries(self):
        width, height = pyautogui.size()
        return width - 1, height - 1

    def _calculatePosition(self, pos, bound, oppositeMove):
        switchOppositeMove = False
        if oppositeMove:
            if pos == 0:
                pos += CURSOR_MOVE_DISTANCE
            else:
                switchOppositeMove = True
                pos -= CURSOR_MOVE_DISTANCE
        else:
            if pos == bound:
                pos -= CURSOR_MOVE_DISTANCE
            else:
                switchOppositeMove = True
                pos += CURSOR_MOVE_DISTANCE

        return switchOppositeMove, pos

    def _calculateXPosition(self, x, xBound):
        switch, newX = self._calculatePosition(
            x, xBound, self.xLastMoveOpposite)
        if switch:
            self.xLastMoveOpposite = not self.xLastMoveOpposite
        return newX

    def _calculateYPosition(self, y, yBound):
        switch, newY = self._calculatePosition(
            y, yBound, self.yLastMoveOpposite)
        if switch:
            self.yLastMoveOpposite = not self.yLastMoveOpposite
        return newY

    def _getNewCoordinates(self):
        width, height = self._getBoudaries()
        currentX, currentY = pyautogui.position()
        if self.testMode:
            print("Current coordinates: ", currentX, currentY)
        return self._calculateXPosition(currentX, width), self._calculateYPosition(currentY, height)

    def _moveMouse(self):
        x, y = self._getNewCoordinates()
        if self.testMode:
            print("New coordinates:", x, y)
        pyautogui.moveTo(x, y)

    def shadowMouseMove(self):
        self._moveMouse()
        self._moveMouse()