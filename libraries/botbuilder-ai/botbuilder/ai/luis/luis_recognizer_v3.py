import aiohttp
import asyncio
import json

from typing import Dict
from .luis_recognizer_internal import LuisRecognizerInternal
from .luis_recognizer_options_v3 import LuisRecognizerOptionsV3
from .luis_application import LuisApplication

from botbuilder.core import (
    RecognizerResult,
    TurnContext,
)
from .activity_util import ActivityUtil


class LuisRecognizerV3(LuisRecognizerInternal):
    _dateSubtypes = ["date", "daterange", "datetime", "datetimerange", "duration", "set", "time", "timerange"]
    _geographySubtypes = ["poi", "city", "countryRegion", "continent", "state"]
    _metadata_key = "$instance"
    # The value type for a LUIS trace activity.
    luis_trace_type: str = "https://www.luis.ai/schemas/trace"

    # The context label for a LUIS trace activity.
    luis_trace_label: str = "Luis Trace"

    def __init__(self, luis_application: LuisApplication, luis_recognizer_options_v3: LuisRecognizerOptionsV3 = None):
        super().__init__(luis_application)

        self.luis_recognizer_options_v3 = luis_recognizer_options_v3 or LuisRecognizerOptionsV3()
        self._application = luis_application

    async def recognizer_internal(
            self,
            turn_context: TurnContext):
        recognizer_result: RecognizerResult = None

        utterance: str = turn_context.activity.text if turn_context.activity is not None else None

        url = self._build_url()
        body = self._build_request(utterance)
        headers = {
            'Ocp-Apim-Subscription-Key': self.luis_application.endpoint_key,
            'Content-Type': 'application/json'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body, headers=headers) as result:
                luis_result = await result.json()
                recognizer_result["intents"] = self._get_intents(luis_result["prediction"])
                recognizer_result["entities"] = self._extract_entities_and_metadata(luis_result["prediction"])

        return recognizer_result

    def _build_url(self):

        base_uri = self._application.endpoint or 'https://westus.api.cognitive.microsoft.com';
        uri = "%s/luis/prediction/v3.0/apps/%s" % (base_uri, self._application.application_id)

        if (self.luis_recognizer_options_v3.version):
            uri += "versions/%/predict" % (self.luis_recognizer_options_v3.version)
        else:
            uri += "slots/%/predict" % (self.luis_recognizer_options_v3.slot)

        params = "?verbose=%s&show-all-intents=%s&log=%s" % (
            "true" if self.luis_recognizer_options_v3.include_instance_data else "false",
            "true" if self.luis_recognizer_options_v3.include_all_intents else "false",
            "true" if self.luis_recognizer_options_v3.log else "false")

        return uri + params

    def _build_request(self, utterance: str):
        body = {
            'query': utterance,
            'preferExternalEntities' : self.luis_recognizer_options_v3.prefer_external_entities
        }

        if self.luis_recognizer_options_v3.dynamic_lists:
            body["dynamicLists"] = self.luis_recognizer_options_v3.dynamic_lists

        if self.luis_recognizer_options_v3.external_entities:
            body["externalEntities"] = self.luis_recognizer_options_v3.external_entities

        return body

    def _get_intents(self, luisResult):
        intents = {}
        if not luisResult["intents"]:
            return intents

        for intent in luisResult["intents"]:
            intents[self._normalize(intent)] = {'score': luisResult["intents"][intent]["score"]}

        return intents

    def _normalize(self, entity):
        splitEntity = entity.split(":")
        entityName = splitEntity[-1]
        return entityName

    def _extract_entities_and_metadata(self, luisResult):
        entities = luisResult["entities"]
        return self._map_properties(entities, False)

    def _map_properties(self, source, inInstance):

        if isinstance(source, int) or isinstance(source, float):
            return source

        result = source
        if isinstance(source, list):
            narr = []
            for item in source:
                isGeographyV2 = ""
                if isinstance(item, dict) and "type" in item and item["type"] in self._geographySubtypes:
                    isGeographyV2 = item["type"]

                if inInstance and isGeographyV2:
                    geoEntity = {}
                    for itemProps in item:
                        if itemProps == "value":
                            geoEntity["location"] = item[itemProps]

                    geoEntity["type"] = isGeographyV2
                    narr.append(geoEntity)
                else:
                    narr.append(self._map_properties(item, inInstance))

            result = narr

        elif not isinstance(source, str):
            nobj = {}
            if not inInstance and isinstance(source, dict) and "type" in source and isinstance(source["type"], str) and \
                    source["type"] in self._dateSubtypes:
                timexs = source["values"]
                arr = []
                if timexs:
                    unique = []
                    for elt in timexs:
                        if elt["timex"] and elt["timex"] in unique:
                            unique.append(elt["timex"])

                    for timex in unique:
                        arr.append(timex)

                    nobj["timex"] = arr

                nobj["type"] = source["type"]

            else:
                for property in source:
                    name = property
                    isArray = isinstance(source[property], list)
                    isString = isinstance(source[property], str)
                    isInt = isinstance(source[property], int)
                    val = self._map_properties(source[property], inInstance or property == self._metadata_key)
                    if name == "datetime" and isArray:
                        nobj["datetimeV1"] = val

                    elif name == "datetimeV2" and isArray:
                        nobj["datetime"] = val

                    elif inInstance:
                        if name == "length" and isInt:
                            nobj["endIndex"] = source[name] + source["startIndex"]
                        elif not ((isInt and name == "modelTypeId") or
                                  (isString and name == "role")):
                            nobj[name] = val
                    else:
                        if name == "unit" and isString:
                            nobj.units = val
                        else:
                            nobj[name] = val

            result = nobj
        return result
