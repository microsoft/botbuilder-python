from datetime import datetime, timedelta
from .time_transform_evaluator import TimeTransformEvaluator
from ..expression_type import ADDSECONDS

class AddSeconds(TimeTransformEvaluator):
    def __init__(self):
        super().__init__(ADDSECONDS, AddSeconds.func)

    @staticmethod
    def func(time: datetime, interval: int):
        return time + timedelta(seconds=interval)
