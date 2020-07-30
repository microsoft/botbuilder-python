from datetime import datetime, timedelta
from .time_transform_evaluator import TimeTransformEvaluator
from ..expression_type import ADDHOURS

class AddHours(TimeTransformEvaluator):
    def __init__(self):
        super().__init__(ADDHOURS, AddHours.func)

    @staticmethod
    def func(time: datetime, interval: int):
        return time + timedelta(hours=interval)
