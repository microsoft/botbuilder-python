# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class BookingDetails:
    def __init__(self, destination: str = None, origin: str = None, travel_date: str = None,
                 supported_destination: bool = False, supported_origin: bool = False):
        self.destination = destination
        self.origin = origin
        self.travel_date = travel_date
        self.supported_destination = supported_destination
        self.supported_origin = supported_origin
