# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import re
from typing import Dict

import aiohttp
from botbuilder.ai.luis.activity_util import ActivityUtil
from botbuilder.ai.luis.luis_util import LuisUtil
from botbuilder.core import (
    IntentScore,
    RecognizerResult,
    TurnContext,
)
from .luis_recognizer_internal import LuisRecognizerInternal
from .luis_recognizer_options_v3 import LuisRecognizerOptionsV3
from .luis_application import LuisApplication


# from .activity_util import ActivityUtil


class LuisRecognizerV3(LuisRecognizerInternal):
    _dateSubtypes = [
        "date",
        "daterange",
        "datetime",
        "datetimerange",
        "duration",
        "set",
        "time",
        "timerange",
    ]
    _geographySubtypes = ["poi", "city", "countryRegion", "continent", "state"]
    _metadata_key = "$instance"

    # The value type for a LUIS trace activity.
    luis_trace_type: str = "https://www.luis.ai/schemas/trace"

    # The context label for a LUIS trace activity.
    luis_trace_label: str = "Luis Trace"

    def __init__(
        self,
        luis_application: LuisApplication,
        luis_recognizer_options_v3: LuisRecognizerOptionsV3 = None,
    ):
        super().__init__(luis_application)

        self.luis_recognizer_options_v3 = (
            luis_recognizer_options_v3 or LuisRecognizerOptionsV3()
        )
        self._application = luis_application

    async def recognizer_internal(self, turn_context: TurnContext):
        recognizer_result: RecognizerResult = None

        utterance: str = (
            turn_context.activity.text if turn_context.activity is not None else None
        )

        url = self._build_url()
        body = self._build_request(utterance)
        headers = {
            "Ocp-Apim-Subscription-Key": self.luis_application.endpoint_key,
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, json=body, headers=headers, ssl=False
            ) as result:
                luis_result = await result.json()

                recognizer_result = RecognizerResult(
                    text=utterance,
                    intents=self._get_intents(luis_result["prediction"]),
                    entities=self._extract_entities_and_metadata(
                        luis_result["prediction"]
                    ),
                )

                if self.luis_recognizer_options_v3.include_instance_data:
                    recognizer_result.entities[self._metadata_key] = (
                        recognizer_result.entities[self._metadata_key]
                        if self._metadata_key in recognizer_result.entities
                        else {}
                    )

                if "sentiment" in luis_result["prediction"]:
                    recognizer_result.properties["sentiment"] = self._get_sentiment(
                        luis_result["prediction"]
                    )

                await self._emit_trace_info(
                    turn_context,
                    luis_result,
                    recognizer_result,
                    self.luis_recognizer_options_v3,
                )

        return recognizer_result

    def _build_url(self):
        base_uri = (
            self._application.endpoint or "https://westus.api.cognitive.microsoft.com"
        )
        uri = "%s/luis/prediction/v3.0/apps/%s" % (
            base_uri,
            self._application.application_id,
        )

        if self.luis_recognizer_options_v3.version:
            uri += "/versions/%s/predict" % (self.luis_recognizer_options_v3.version)
        else:
            uri += "/slots/%s/predict" % (self.luis_recognizer_options_v3.slot)

        params = "?verbose=%s&show-all-intents=%s&log=%s" % (
            (
                "true"
                if self.luis_recognizer_options_v3.include_instance_data
                else "false"
            ),
            "true" if self.luis_recognizer_options_v3.include_all_intents else "false",
            "true" if self.luis_recognizer_options_v3.log else "false",
        )

        return uri + params

    def _build_request(self, utterance: str):
        body = {
            "query": utterance,
            "options": {
                "preferExternalEntities": self.luis_recognizer_options_v3.prefer_external_entities,
            },
        }

        if self.luis_recognizer_options_v3.datetime_reference:
            body["options"][
                "datetimeReference"
            ] = self.luis_recognizer_options_v3.datetime_reference

        if self.luis_recognizer_options_v3.dynamic_lists:
            body["dynamicLists"] = self.luis_recognizer_options_v3.dynamic_lists

        if self.luis_recognizer_options_v3.external_entities:
            body["externalEntities"] = self.luis_recognizer_options_v3.external_entities

        return body

    def _get_intents(self, luis_result):
        intents = {}
        if not luis_result["intents"]:
            return intents

        for intent in luis_result["intents"]:
            intents[self._normalize_name(intent)] = IntentScore(
                luis_result["intents"][intent]["score"]
            )

        return intents

    def _normalize_name(self, name):
        return re.sub(r"\.", "_", name)

    def _normalize(self, entity):
        split_entity = entity.split(":")
        entity_name = split_entity[-1]
        return self._normalize_name(entity_name)

    def _extract_entities_and_metadata(self, luis_result):
        entities = luis_result["entities"]
        return self._map_properties(entities, False)

    def _map_properties(self, source, in_instance):
        if isinstance(source, (int, float, bool, str)):
            return source

        result = source
        if isinstance(source, list):
            narr = []
            for item in source:
                is_geography_v2 = ""
                if (
                    isinstance(item, dict)
                    and "type" in item
                    and item["type"] in self._geographySubtypes
                ):
                    is_geography_v2 = item["type"]

                if not in_instance and is_geography_v2:
                    geo_entity = {}
                    for item_props in item:
                        if item_props == "value":
                            geo_entity["location"] = item[item_props]

                    geo_entity["type"] = is_geography_v2
                    narr.append(geo_entity)
                else:
                    narr.append(self._map_properties(item, in_instance))

            result = narr

        elif not isinstance(source, str):
            nobj = {}
            if (
                not in_instance
                and isinstance(source, dict)
                and "type" in source
                and isinstance(source["type"], str)
                and source["type"] in self._dateSubtypes
            ):
                timexs = source["values"]
                arr = []
                if timexs:
                    unique = []
                    for elt in timexs:
                        if elt["timex"] and elt["timex"] not in unique:
                            unique.append(elt["timex"])

                    for timex in unique:
                        arr.append(timex)

                    nobj["timex"] = arr

                nobj["type"] = source["type"]

            else:
                for property in source:
                    name = self._normalize(property)
                    is_array = isinstance(source[property], list)
                    is_string = isinstance(source[property], str)
                    is_int = isinstance(source[property], (int, float))
                    val = self._map_properties(
                        source[property], in_instance or property == self._metadata_key
                    )
                    if name == "datetime" and is_array:
                        nobj["datetimeV1"] = val

                    elif name == "datetimeV2" and is_array:
                        nobj["datetime"] = val

                    elif in_instance:
                        if name == "length" and is_int:
                            nobj["endIndex"] = source[name] + source["startIndex"]
                        elif not (
                            (is_int and name == "modelTypeId")
                            or (is_string and name == "role")
                        ):
                            nobj[name] = val
                    else:
                        if name == "unit" and is_string:
                            nobj["units"] = val
                        else:
                            nobj[name] = val

            result = nobj
        return result

    def _get_sentiment(self, luis_result):
        return {
            "label": luis_result["sentiment"]["label"],
            "score": luis_result["sentiment"]["score"],
        }

    async def _emit_trace_info(
        self,
        turn_context: TurnContext,
        luis_result,
        recognizer_result: RecognizerResult,
        options: LuisRecognizerOptionsV3,
    ) -> None:
        trace_info: Dict[str, object] = {
            "recognizerResult": LuisUtil.recognizer_result_as_dict(recognizer_result),
            "luisModel": {"ModelID": self._application.application_id},
            "luisOptions": {"Slot": options.slot},
            "luisResult": luis_result,
        }

        trace_activity = ActivityUtil.create_trace(
            turn_context.activity,
            "LuisRecognizer",
            trace_info,
            LuisRecognizerV3.luis_trace_type,
            LuisRecognizerV3.luis_trace_label,
        )

        await turn_context.send_activity(trace_activity)
