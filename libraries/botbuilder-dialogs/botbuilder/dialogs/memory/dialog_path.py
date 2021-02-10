# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class DialogPath:
    # Counter of emitted events.
    EVENT_COUNTER = "dialog.eventCounter"

    # Currently expected properties.
    EXPECTED_PROPERTIES = "dialog.expectedProperties"

    # Default operation to use for entities where there is no identified operation entity.
    DEFAULT_OPERATION = "dialog.defaultOperation"

    # Last surfaced entity ambiguity event.
    LAST_EVENT = "dialog.lastEvent"

    # Currently required properties.
    REQUIRED_PROPERTIES = "dialog.requiredProperties"

    # Number of retries for the current Ask.
    RETRIES = "dialog.retries"

    # Last intent.
    LAST_INTENT = "dialog.lastIntent"

    # Last trigger event: defined in FormEvent, ask, clarifyEntity etc..
    LAST_TRIGGER_EVENT = "dialog.lastTriggerEvent"

    @staticmethod
    def get_property_name(prop: str) -> str:
        return prop.replace("dialog.", "")
