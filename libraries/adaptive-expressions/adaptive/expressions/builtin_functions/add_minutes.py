from datetime import datetime, timedelta
from .time_transform_evaluator import TimeTransformEvaluator
from ..expression_type import ADDMINUTES


class AddMinutes(TimeTransformEvaluator):
    def __init__(self):
        super().__init__(ADDMINUTES, AddMinutes.func)

    @staticmethod
    def func(time: datetime, interval: int):
        return time + timedelta(minutes=interval)
