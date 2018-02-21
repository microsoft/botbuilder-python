
class ReceiveDelegate:
    def __init__(self, target):
        self._target = target

    def call(self, activity):
        self._target.receive(activity)