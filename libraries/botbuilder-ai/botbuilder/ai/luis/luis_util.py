# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict, List, Set, Union

from azure.cognitiveservices.language.luis.runtime.models import (
    CompositeEntityModel,
    EntityModel,
    LuisResult,
)

from . import IntentScore, RecognizerResult


class LuisUtil:
    """
    Utility functions used to extract and transform data from Luis SDK
    """

    _metadataKey: str = "$instance"

    @staticmethod
    def normalized_intent(intent: str) -> str:
        return intent.replace(".", "_").replace(" ", "_")

    @staticmethod
    def get_intents(luisResult: LuisResult) -> Dict[str, IntentScore]:
        if luisResult.intents:
            return {
                LuisUtil.normalized_intent(i.intent): IntentScore(i.score or 0)
                for i in luisResult.intents
            }
        else:
            return {
                LuisUtil.normalized_intent(
                    luisResult.top_scoring_intent.intent
                ): IntentScore(luisResult.top_scoring_intent.score or 0)
            }

    @staticmethod
    def extract_entities_and_metadata(
        entities: List[EntityModel],
        compositeEntities: List[CompositeEntityModel],
        verbose: bool,
    ) -> Dict:
        entitiesAndMetadata = {}
        if verbose:
            entitiesAndMetadata[LuisUtil._metadataKey] = {}

        compositeEntityTypes = set()

        # We start by populating composite entities so that entities covered by them are removed from the entities list
        if compositeEntities:
            compositeEntityTypes = set(ce.parent_type for ce in compositeEntities)
            current = entities
            for compositeEntity in compositeEntities:
                current = LuisUtil.populate_composite_entity_model(
                    compositeEntity, current, entitiesAndMetadata, verbose
                )
            entities = current

        for entity in entities:
            # we'll address composite entities separately
            if entity.type in compositeEntityTypes:
                continue

            LuisUtil.add_property(
                entitiesAndMetadata,
                LuisUtil.extract_normalized_entity_name(entity),
                LuisUtil.extract_entity_value(entity),
            )

            if verbose:
                LuisUtil.add_property(
                    entitiesAndMetadata[LuisUtil._metadataKey],
                    LuisUtil.extract_normalized_entity_name(entity),
                    LuisUtil.extract_entity_metadata(entity),
                )

        return entitiesAndMetadata

    @staticmethod
    def number(value: object) -> Union(int, float):
        if value is None:
            return None

        try:
            s = str(value)
            i = int(s)
            return i
        except ValueError:
            f = float(s)
            return f

    @staticmethod
    def extract_entity_value(entity: EntityModel) -> object:
        if (
            entity.AdditionalProperties is None
            or "resolution" not in entity.AdditionalProperties
        ):
            return entity.entity

        resolution = entity.AdditionalProperty["resolution"]
        if entity.Type.startswith("builtin.datetime."):
            return resolution
        elif entity.Type.startswith("builtin.datetimeV2."):
            if not resolution.values:
                return resolution

            resolutionValues = resolution.values
            val_type = resolution.values[0].type
            timexes = [val.timex for val in resolutionValues]
            distinctTimexes = list(set(timexes))
            return {"type": val_type, "timex": distinctTimexes}
        else:
            if entity.type in {"builtin.number", "builtin.ordinal"}:
                return LuisUtil.number(resolution.value)
            elif entity.type == "builtin.percentage":
                svalue = str(resolution.value)
                if svalue.endswith("%"):
                    svalue = svalue[:-1]

                return LuisUtil.number(svalue)
            elif entity.type in {
                "builtin.age",
                "builtin.dimension",
                "builtin.currency",
                "builtin.temperature",
            }:
                units = str(resolution.unit)
                val = LuisUtil.number(resolution.value)
                obj = {}
                if val is not None:
                    obj["number"] = val

                obj["units"] = units
                return obj

            else:
                return resolution.value or resolution.values

    @staticmethod
    def extract_entity_metadata(entity: EntityModel) -> Dict:
        obj = dict(
            startIndex=int(entity.start_index),
            endIndex=int(entity.end_index + 1),
            text=entity.entity,
            type=entity.type,
        )

        if entity.AdditionalProperties is not None:
            if "score" in entity.AdditionalProperties:
                obj["score"] = float(entity.AdditionalProperties["score"])

            resolution = entity.AdditionalProperties.get("resolution")
            if resolution is not None and resolution.subtype is not None:
                obj["subtype"] = resolution.subtype

        return obj

    @staticmethod
    def extract_normalized_entity_name(entity: EntityModel) -> str:
        # Type::Role -> Role
        type = entity.Type.split(":")[-1]
        if type.startswith("builtin.datetimeV2."):
            type = "datetime"

        if type.startswith("builtin.currency"):
            type = "money"

        if type.startswith("builtin."):
            type = type[8:]

        role = (
            entity.AdditionalProperties["role"]
            if entity.AdditionalProperties is not None
            and "role" in entity.AdditionalProperties
            else ""
        )
        if role and not role.isspace():
            type = role

        return type.replace(".", "_").replace(" ", "_")

    @staticmethod
    def populate_composite_entity_model(
        compositeEntity: CompositeEntityModel,
        entities: List[EntityModel],
        entitiesAndMetadata: Dict,
        verbose: bool,
    ) -> List[EntityModel]:
        childrenEntites = {}
        childrenEntitiesMetadata = {}
        if verbose:
            childrenEntites[LuisUtil._metadataKey] = {}

        # This is now implemented as O(n^2) search and can be reduced to O(2n) using a map as an optimization if n grows
        compositeEntityMetadata = next(
            (
                e
                for e in entities
                if e.type == compositeEntity.parent_type
                and e.entity == compositeEntity.value
            ),
            None,
        )

        # This is an error case and should not happen in theory
        if compositeEntityMetadata is None:
            return entities

        if verbose:
            childrenEntitiesMetadata = LuisUtil.extract_entity_metadata(
                compositeEntityMetadata
            )
            childrenEntites[LuisUtil._metadataKey] = {}

        coveredSet: Set[EntityModel] = set()
        for child in compositeEntity.Children:
            for entity in entities:
                # We already covered this entity
                if entity in coveredSet:
                    continue

                # This entity doesn't belong to this composite entity
                if child.Type != entity.Type or not LuisUtil.composite_contains_entity(
                    compositeEntityMetadata, entity
                ):
                    continue

                # Add to the set to ensure that we don't consider the same child entity more than once per composite
                coveredSet.add(entity)
                LuisUtil.add_property(
                    childrenEntites,
                    LuisUtil.extract_normalized_entity_name(entity),
                    LuisUtil.extract_entity_value(entity),
                )

                if verbose:
                    LuisUtil.add_property(
                        childrenEntites[LuisUtil._metadataKey],
                        LuisUtil.extract_normalized_entity_name(entity),
                        LuisUtil.extract_entity_metadata(entity),
                    )

        LuisUtil.add_property(
            entitiesAndMetadata,
            LuisUtil.extract_normalized_entity_name(compositeEntityMetadata),
            childrenEntites,
        )
        if verbose:
            LuisUtil.add_property(
                entitiesAndMetadata[LuisUtil._metadataKey],
                LuisUtil.extract_normalized_entity_name(compositeEntityMetadata),
                childrenEntitiesMetadata,
            )

        # filter entities that were covered by this composite entity
        return [entity for entity in entities if entity not in coveredSet]

    @staticmethod
    def composite_contains_entity(
        compositeEntityMetadata: EntityModel, entity: EntityModel
    ) -> bool:
        return (
            entity.StartIndex >= compositeEntityMetadata.StartIndex
            and entity.EndIndex <= compositeEntityMetadata.EndIndex
        )

    @staticmethod
    def add_property(obj: Dict[str, object], key: str, value: object) -> None:
        # If a property doesn't exist add it to a new array, otherwise append it to the existing array.

        if key in obj:
            obj[key].append(value)
        else:
            obj[key] = [value]

    @staticmethod
    def add_properties(luis: LuisResult, result: RecognizerResult) -> None:
        if luis.SentimentAnalysis is not None:
            result.Properties.Add(
                "sentiment",
                {
                    "label": luis.SentimentAnalysis.Label,
                    "score": luis.SentimentAnalysis.Score,
                },
            )
