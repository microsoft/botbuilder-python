# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class ContentType:
    O365_CONNECTOR_CARD = "application/vnd.microsoft.teams.card.o365connector"
    FILE_CONSENT_CARD = "application/vnd.microsoft.teams.card.file.consent"
    FILE_DOWNLOAD_INFO = "application/vnd.microsoft.teams.file.download.info"
    FILE_INFO_CARD = "application/vnd.microsoft.teams.card.file.info"


class Type:
    O365_CONNECTOR_CARD_VIEWACTION = "ViewAction"
    O365_CONNECTOR_CARD_OPEN_URI = "OpenUri"
    O365_CONNECTOR_CARD_HTTP_POST = "HttpPOST"
    O365_CONNECTOR_CARD_ACTION_CARD = "ActionCard"
    O365_CONNECTOR_CARD_TEXT_INPUT = "TextInput"
    O365_CONNECTOR_CARD_DATE_INPUT = "DateInput"
    O365_CONNECTOR_CARD_MULTICHOICE_INPUT = "MultichoiceInput"
