# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Type
from flask import jsonify, Request, Response

from msrest.serialization import Model


class HttpHelper:
    @staticmethod
    def read_request(model_cls: Type[Model], request: Request) -> Model:
        try:
            if not request:
                raise TypeError("request can not be None")

            model_cls().deserialize(request.json)
        except:
            model_cls()

    @staticmethod
    def write_response(response: Response, status_code: int, body: Model = None):
        if not response:
            raise TypeError("response can not be None")

        if not body:
            response.status_code = 200
        else:
            response.status_code = status_code
            response.content_type = "application/json"
            response.data = jsonify(body.as_dict())
