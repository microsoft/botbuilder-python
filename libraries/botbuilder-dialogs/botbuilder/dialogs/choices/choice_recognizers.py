# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

class ChoiceRecognizers:
    """ Contains methods for matching user input against a list of choices. """

    # Note to self: C# implementation has 2 RecognizeChoices overloads, different in their list parameter
    # 1. list of strings - that gets converted into a list of Choice's
    # 2. list of choices
    # Looks like in TS the implement also allows for either string[] or Choice[]

    # C# none of the functions seem to be nested inside another function
    # TS has only 1 recognizer funtion, recognizeChoices()
        # nested within recognizeChoices() is matchChoiceByIndex()
    
