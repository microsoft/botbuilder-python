# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import datetime

from datatypes_date_time import Timex


class LanguageGeneration:
    @staticmethod
    def examples():
        LanguageGeneration.__describe(Timex("2019-05-29"))
        LanguageGeneration.__describe(Timex("XXXX-WXX-6"))
        LanguageGeneration.__describe(Timex("XXXX-WXX-6T16"))
        LanguageGeneration.__describe(Timex("T12"))

        # 1.0.2a1 doesn't support this
        # LanguageGeneration.__describe(Timex.from_date(datetime.datetime.now()))
        # LanguageGeneration.__describe(Timex.from_date(datetime.datetime.now() + datetime.timedelta(days=1)))

    @staticmethod
    def __describe(timex: Timex):
        reference_date = datetime.datetime.now()

        # 1.0.2a1: exception using time_value()
        # print(f"{timex.time_value()} {timex.to_natural_language(reference_date)}")
        print("LanguageGeneration: 1.0.2a1 time_value() issue")
