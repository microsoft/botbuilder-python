import json
import asyncio
import requests

class QnAMaker:

    __qnaMakerServiceEndpoint = 'https://westus.api.cognitive.microsoft.com/qnamaker/v3.0/knowledgebases/'
    __json_mime_type = 'application/json'
    __api_management_header = 'Ocp-Apim-Subscription-Key'

    def __init__(self, options, http_client):
        
        self.__http_client = _http_client or False
        if not self.__http_client:
            raise TypeError('HTTP Client failed')
        self.__options = options or False
        if not self.__options:
            raise TypeError('Options config error')

        self.__answerUrl = "%s%s/generateanswer" % (__qnaMakerServiceEndpoint,options.knowledge_base_id)

        if self.__options.ScoreThreshold == 0:
            self.__options.ScoreThreshold = 0.3 #Note - SHOULD BE 0.3F 'FLOAT'
        
        if self.__options.Top == 0:
            self.__options.Top = 1
        
        if self.__options.StrictFilters == None:
            self.__options.StrictFilters = MetaData()

        if self.__options.MetadataBoost == None:
            self.__options.MetadataBoost = MetaData()

    async def get_answers(question):        # HTTP call
        headers = {
            __api_management_header : self.__options.subscription_key,
            "Content-Type" : __json_mime_type
        }
        
        payload = json.dumps({
            "question" : question
        })
        # POST request to QnA Service
        content = requests.post(self.__answerUrl, headers=headers, data=payload)
        return content.json()
     
class QnAMakerOptions:
    def __init__(self, subscription_key, knowledge_base_id, score_threshhold, top, strict_filters, metadata_boost):
        self.subscription_key = subscription_key
        self.knowledge_base_id = knowledge_base_id
        self.score_threshhold = score_threshhold
        self.top = top
        self.strict_filters = strict_filters
        self.metadata_boost = metadata_boost

class MetaData:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class QueryResult:
    def __init__(self, questions, answer, score, metadata, source, qna_id):
        self.questions = questions
        self.answer = answer
        self.score = score
        self.metadata = metadata
        self.source = source
        self.qna_id = qna_id

class QueryResults:
    def __init__(self, answers):
        self.__answers = answers