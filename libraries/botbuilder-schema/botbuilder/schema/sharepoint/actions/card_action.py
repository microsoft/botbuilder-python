# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum
from typing import Dict, List
from msrest.serialization import Model


class ConfirmationDialog(Model):
    """
    SharePoint Confirmation Dialog option that is passed through `Submit` Action is executed.

    :param title: Title of the type.
    :type title: str
    :param message: Message of the type.
    :type message: str
    """

    _attribute_map = {
        "title": {"key": "title", "type": "str"},
        "message": {"key": "message", "type": "str"},
    }

    def __init__(self, *, title: str = None, message: str = None, **kwargs) -> None:
        super(ConfirmationDialog, self).__init__(**kwargs)
        self.title = title
        self.message = message


class Location(Model):
    """
    Sharepoint Location object.

    :param latitude: Latitude of the location of type.
    :type latitude: int
    :param longitude: Longitude of the location of type.
    :type longitude: int
    :param timestamp: Timestamp of the location of type.
    :type timestamp: int
    :param accuracy: Accuracy of the location of type.
    :type accuracy: int
    """

    _attribute_map = {
        "latitude": {"key": "latitude", "type": "int"},
        "longitude": {"key": "longitude", "type": "int"},
        "timestamp": {"key": "timestamp", "type": "int"},
        "accuracy": {"key": "accuracy", "type": "int"},
    }

    def __init__(
        self,
        *,
        latitude: int = None,
        longitude: int = None,
        timestamp: int = None,
        accuracy: int = None,
        **kwargs
    ) -> None:
        super(Location, self).__init__(**kwargs)
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp
        self.accuracy = accuracy


class MediaTypeOption(Enum):
    """
    This enum contains the different types of media that can be selected.
    """

    Image = 1
    Audio = 4
    Document = 8


class SelectMediaActionParameters(Model):
    """
    SharePoint parameters for a select media action.

    :param media_type: The type of media to select.
    :type media_type: MediaTypeOption
    :param allow_multiple_capture: Whether to allow multiple files to be captured.
    :type allow_multiple_capture: bool
    :param max_size_per_file: The maximum size per file.
    :type max_size_per_file: int
    :param supported_file_formats: The supported file formats of select media action of type.
    :type supported_file_formats: List[str]
    """

    _attribute_map = {
        "media_type": {"key": "mediaType", "type": "MediaTypeOption"},
        "allow_multiple_capture": {"key": "allowMultipleCapture", "type": "bool"},
        "max_size_per_file": {"key": "maxSizePerFile", "type": "int"},
        "supported_file_formats": {"key": "supportedFileFormats", "type": "[str]"},
    }

    def __init__(
        self,
        *,
        media_type: MediaTypeOption = None,
        allow_multiple_capture: bool = None,
        max_size_per_file: int = None,
        supported_file_formats: List[str] = None,
        **kwargs
    ) -> None:
        super(SelectMediaActionParameters, self).__init__(**kwargs)
        self.media_type = media_type
        self.allow_multiple_capture = allow_multiple_capture
        self.max_size_per_file = max_size_per_file
        self.supported_file_formats = supported_file_formats


class QuickViewActionParameters(Model):
    """
    SharePoint parameters for an quick view action.

    :param view: The view of the Quick view to open.
    :type title: str
    """

    _attribute_map = {
        "view": {"key": "view", "type": "str"},
    }

    def __init__(self, *, view: str = None, **kwargs) -> None:
        super(QuickViewActionParameters, self).__init__(**kwargs)
        self.view = view


class BaseAction(Model):
    """
    Base class for all actions.
    """

    _attribute_map = {
        "type": {"key": "type", "type": "str"},
    }

    def __init__(self, *, type: str = None, **kwargs) -> None:
        super(BaseAction, self).__init__(**kwargs)
        self.type = type


class CardAction(BaseAction):
    """
    Type of handler for when a card button is pressed.
    """


class OnCardSelectionAction(BaseAction):
    """
    Type of handler for when a card is selected.
    """


class QuickViewAction(CardAction, OnCardSelectionAction):
    """
    SharePoint Quick view action.

    :param type: Type of the action.
    :type type: str
    :param parameters: Parameters for the quick view action.
    :type parameters: QuickViewActionParameters
    """

    _attribute_map = {
        "parameters": {"key": "parameters", "type": "QuickViewActionParameters"},
    }

    def __init__(
        self, *, parameters: QuickViewActionParameters = None, **kwargs
    ) -> None:
        super(QuickViewAction, self).__init__(type="QuickView", **kwargs)
        self.parameters = parameters


class ExternalLinkActionParameters(Model):
    """
    SharePoint parameters for an external link action.

    :param is_teams_deep_link: Whether the link is a Teams deep link.
    :type is_teams_deep_link: bool
    :param target: The target of the external link.
    :type target: str
    """

    _attribute_map = {
        "is_teams_deep_link": {"key": "isTeamsDeepLink", "type": "bool"},
        "target": {"key": "target", "type": "str"},
    }

    def __init__(
        self, *, is_teams_deep_link: bool = None, target: str = None, **kwargs
    ) -> None:
        super(ExternalLinkActionParameters, self).__init__(**kwargs)
        self.is_teams_deep_link = is_teams_deep_link
        self.target = target


class ExternalLinkAction(CardAction, OnCardSelectionAction):
    """
    SharePoint External link action.

    :param type: Type of the action.
    :type type: str
    :param parameters: Parameters for the external link action.
    :type parameters: ExternalLinkActionParameters
    """

    _attribute_map = {
        "parameters": {"key": "parameters", "type": "ExternalLinkActionParameters"},
    }

    def __init__(
        self, *, parameters: ExternalLinkActionParameters = None, **kwargs
    ) -> None:
        super(ExternalLinkAction, self).__init__(type="ExternalLink", **kwargs)
        self.parameters = parameters


class SubmitAction(CardAction):
    """
    SharePoint Submit action.

    :param type: Type of the action.
    :type type: str
    :param parameters: The action parameters of type
    :type parameters: {object}
    :param dialog: Dialog of the action.
    :type dialog: ConfirmationDialog
    """

    _attribute_map = {
        "parameters": {"key": "parameters", "type": "{object}"},
        "confirmation_dialog": {
            "key": "confirmationDialog",
            "type": "ConfirmationDialog",
        },
    }

    def __init__(
        self,
        *,
        parameters: Dict[str, object] = None,
        dialog: ConfirmationDialog = None,
        **kwargs
    ) -> None:
        super(SubmitAction, self).__init__(type="Submit", **kwargs)
        self.parameters = parameters
        self.dialog = dialog


class ExecuteAction(CardAction):
    """
    SharePoint Execute action.

    :param type: Type of the action.
    :type type: str
    :param parameters: The action parameters of type
    :type parameters: {object}
    :param verb: The verb associated with this action of type.
    :type verb: str
    """

    _attribute_map = {
        "parameters": {"key": "parameters", "type": "{object}"},
        "verb": {"key": "verb", "type": "str"},
    }

    def __init__(
        self, *, parameters: Dict[str, object] = None, verb: str = None, **kwargs
    ) -> None:
        super(ExecuteAction, self).__init__(type="Execute", **kwargs)
        self.parameters = parameters
        self.verb = verb


class SelectMediaAction(CardAction, OnCardSelectionAction):
    """
    SharePoint Select media action.

    :param type: Type of the action.
    :type type: str
    :param parameters: Parameters for the select media action.
    :type parameters: SelectMediaActionParameters
    """

    _attribute_map = {
        "parameters": {"key": "parameters", "type": "SelectMediaActionParameters"},
    }

    def __init__(
        self, *, parameters: SelectMediaActionParameters = None, **kwargs
    ) -> None:
        super(SelectMediaAction, self).__init__(type="VivaAction.SelectMedia", **kwargs)
        self.parameters = parameters


class ShowLocationActionParameters(Model):
    """
    SharePoint parameters for a show location action.

    :param location: The location coordinates of type.
    :type location: Location
    """

    _attribute_map = {
        "location_coordinates": {"key": "locationCoordinates", "type": "Location"},
    }

    def __init__(self, *, location: Location = None, **kwargs) -> None:
        super(ShowLocationActionParameters, self).__init__(**kwargs)
        self.location = location


class ShowLocationAction(CardAction, OnCardSelectionAction):
    """
    SharePoint Show location action.

    :param type: Type of the action.
    :type type: str
    :param parameters: Parameters for the show location action.
    :type parameters: ShowLocationActionParameters
    """

    _attribute_map = {
        "parameters": {"key": "parameters", "type": "ShowLocationActionParameters"},
    }

    def __init__(
        self, *, parameters: ShowLocationActionParameters = None, **kwargs
    ) -> None:
        super(ShowLocationAction, self).__init__(
            type="VivaAction.ShowLocation", **kwargs
        )
        self.parameters = parameters


class GetLocationActionParameters(Model):
    """
    SharePoint parameters for a get location action.

    :param choose_location_on_map: Whether the location on the map can be chosen of type.
    :type choose_location_on_map: bool
    """

    _attribute_map = {
        "choose_location_on_map": {"key": "chooseLocationOnMap", "type": "bool"},
    }

    def __init__(self, *, choose_location_on_map: bool = None, **kwargs) -> None:
        super(GetLocationActionParameters, self).__init__(**kwargs)
        self.choose_location_on_map = choose_location_on_map


class GetLocationAction(CardAction, OnCardSelectionAction):
    """
    SharePoint Get location action.

    :param type: Type of the action.
    :type type: str
    :param parameters: Parameters for the get location action.
    :type parameters: GetLocationActionParameters
    """

    _attribute_map = {
        "parameters": {"key": "parameters", "type": "GetLocationActionParameters"},
    }

    def __init__(
        self, *, parameters: GetLocationActionParameters = None, **kwargs
    ) -> None:
        super(GetLocationAction, self).__init__(type="VivaAction.GetLocation", **kwargs)
        self.parameters = parameters
