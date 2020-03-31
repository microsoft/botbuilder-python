# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .. import QnAMakerOptions, QnADialogResponseOptions


class QnAMakerDialogOptions:
    """
    Defines Dialog Options for QnAMakerDialog.
    """

    def __init__(
        self,
        options: QnAMakerOptions = None,
        response_options: QnADialogResponseOptions = None,
    ):
        self.options = options or QnAMakerOptions()
        self.response_options = response_options or QnADialogResponseOptions()
