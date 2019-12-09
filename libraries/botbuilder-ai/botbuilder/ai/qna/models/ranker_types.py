# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class RankerTypes:

    """ Default Ranker Behaviour. i.e. Ranking based on Questions and Answer. """

    DEFAULT = "Default"

    """ Ranker based on question Only. """
    QUESTION_ONLY = "QuestionOnly"

    """ Ranker based on Autosuggest for question field only. """
    AUTO_SUGGEST_QUESTION = "AutoSuggestQuestion"
