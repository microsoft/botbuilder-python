# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List, Union


class BookingDetails:
    def __init__(
        self,
        destination: Union[str, None] = None,
        origin: Union[str, None] = None,
        travel_date: Union[str, None] = None,
        unsupported_airports: List[str] = None,
    ):
        self.destination = destination
        self.origin = origin
        self.travel_date = travel_date
        self.unsupported_airports = unsupported_airports or []
