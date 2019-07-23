# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from aiohttp import ClientSession

from ..qnamaker_endpoint import QnAMakerEndpoint
from ..models import FeedbackRecords

from .http_request_utils import HttpRequestUtils


class TrainUtils:
    """ Class for Train API, used in active learning to add suggestions to the knowledge base  """

    def __init__(self, endpoint: QnAMakerEndpoint, http_client: ClientSession):
        """
        Initializes a new instance for active learning train utils.

        Parameters:
        -----------

        endpoint: QnA Maker Endpoint of the knowledge base to query.

        http_client: Http client.
        """
        self._endpoint = endpoint
        self._http_client = http_client

    async def call_train(self, feedback_records: FeedbackRecords):
        """
        Train API to provide feedback.

        Parameter:
        -------------

        feedback_records: Feedback record list.
        """
        if not feedback_records:
            raise TypeError("TrainUtils.call_train(): feedback_records cannot be None.")

        if not feedback_records.records or len(feedback_records.records) == 0:
            return

        self.query_train(feedback_records)

    async def query_train(self, feedback_records: FeedbackRecords):
        url: str = f"{ self._endpoint.host }/knowledgebases/{ self._endpoint.knowledge_base_id }/train"
        payload_body = {"feedbackRecords": feedback_records}
        http_request_helper = HttpRequestUtils(self._http_client)

        await http_request_helper.execute_http_request(
            url, payload_body, self._endpoint
        )
