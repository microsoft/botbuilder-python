from datetime import datetime, timedelta
from .time_transform_evaluator import TimeTransformEvaluator
from ..expression_type import ADDDAYS


class AddDays(TimeTransformEvaluator):
    def __init__(self):
        super().__init__(ADDDAYS, AddDays.func)

    @staticmethod
    def func(time: datetime, interval: int):
        return time + timedelta(days=interval)
