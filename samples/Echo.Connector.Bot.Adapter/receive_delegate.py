from microsoft.botbuilder.schema import Activity


class ReceiveDelegate:
    def __init__(self, target):
        self._target = target

    def call(self, activity: Activity):
        self._target.receive(activity)
