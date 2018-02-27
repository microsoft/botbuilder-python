# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from typing import List
from botbuilder.schema import Activity


class ActivityAdapter(ABC):
    @abstractmethod
    def send(self, activities: List[Activity]): pass

    @abstractmethod
    def receive(self, auth_header: str, activity: Activity): pass
