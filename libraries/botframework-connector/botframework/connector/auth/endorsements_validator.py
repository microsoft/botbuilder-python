from typing import List

class EndorsementsValidator():
    @staticmethod
    def validate(channel_id: str, endorsements: List[str]):
        # If the Activity came in and doesn't have a Channel ID then it's making no 
        # assertions as to who endorses it. This means it should pass. 
        if not channel_id:
            return True

        if endorsements == None:
            raise ValueError('Argument endorsements is null.')

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

        endorsementPresent = channel_id in endorsements
        return endorsementPresent
