# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List


class EndorsementsValidator:
    @staticmethod
    def validate(expected_endorsement: str, endorsements: List[str]):
        # If the Activity came in and doesn't have a Channel ID then it's making no
        # assertions as to who endorses it. This means it should pass.
        if not expected_endorsement:
            return True

        if endorsements is None:
            raise ValueError("Argument endorsements is null.")

        # The Call path to get here is:
        # JwtTokenValidation.AuthenticateRequest
        #  ->
        #   JwtTokenValidation.ValidateAuthHeader
        #    ->
        #      ChannelValidation.AuthenticateChannelToken
        #       ->
        #          JWTTokenExtractor

        # Does the set of endorsements match the channelId that was passed in?

        # ToDo: Consider moving this to a HashSet instead of a string
        # array, to make lookups O(1) instead of O(N). To give a sense
        # of scope, tokens from WebChat have about 10 endorsements, and
        # tokens coming from Teams have about 20.

        endorsement_present = expected_endorsement in endorsements
        return endorsement_present
