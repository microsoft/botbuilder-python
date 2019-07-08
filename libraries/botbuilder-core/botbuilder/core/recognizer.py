from abc import ABC
from botbuilder.core import TurnContext


class Recognizer(ABC):
    @staticmethod
    async def recognize(turn_context: TurnContext) -> Rec:
        raise NotImplementedError()
