import asyncio
from asyncio import Future, ensure_future
from typing import Dict
from uuid import UUID, uuid4

import aiounittest
from botframework.streaming import ReceiveResponse
from botframework.streaming.payloads import RequestManager


class TestRequestManager(aiounittest.AsyncTestCase):
    def test_ctor_empty_dictionary(self):
        pending_requests: Dict[UUID, Future[ReceiveResponse]] = {}
        _ = RequestManager(pending_requests=pending_requests)

        self.assertEqual(0, len(pending_requests))

    async def test_signal_response_returns_false_when_no_uuid(self):
        pending_requests: Dict[UUID, Future[ReceiveResponse]] = {}
        manager = RequestManager(pending_requests=pending_requests)
        request_id: UUID = uuid4()
        response = ReceiveResponse()
        signal = await manager.signal_response(request_id=request_id, response=response)

        self.assertFalse(signal)

    async def test_signal_response_returns_true_when_uuid(self):
        pending_requests: Dict[UUID, Future[ReceiveResponse]] = {}
        request_id: UUID = uuid4()
        pending_requests[request_id] = Future()

        manager = RequestManager(pending_requests=pending_requests)

        response = ReceiveResponse()
        signal = await manager.signal_response(request_id=request_id, response=response)

        self.assertTrue(signal)

    async def test_signal_response_null_response_is_ok(self):
        pending_requests: Dict[UUID, Future[ReceiveResponse]] = {}
        request_id: UUID = uuid4()
        pending_requests[request_id] = Future()

        manager = RequestManager(pending_requests=pending_requests)

        # noinspection PyTypeChecker
        _ = await manager.signal_response(request_id=request_id, response=None)

        self.assertIsNone(pending_requests[request_id].result())

    async def test_signal_response_response(self):
        pending_requests: Dict[UUID, Future[ReceiveResponse]] = {}
        request_id: UUID = uuid4()
        pending_requests[request_id] = Future()

        manager = RequestManager(pending_requests=pending_requests)
        response = ReceiveResponse()

        _ = await manager.signal_response(request_id=request_id, response=response)

        self.assertEqual(response, pending_requests[request_id].result())

    async def test_get_response_returns_null_on_duplicate_call(self):
        pending_requests: Dict[UUID, Future[ReceiveResponse]] = {}
        request_id: UUID = uuid4()
        pending_requests[request_id] = Future()

        manager = RequestManager(pending_requests=pending_requests)

        response = await manager.get_response(request_id)

        self.assertIsNone(response)

    async def test_get_response_returns_response(self):
        pending_requests: Dict[UUID, Future[ReceiveResponse]] = {}
        request_id: UUID = uuid4()

        manager = RequestManager(pending_requests=pending_requests)
        test_response = ReceiveResponse()

        async def set_response():
            nonlocal manager
            nonlocal request_id
            nonlocal test_response

            while True:
                signal = await manager.signal_response(
                    request_id, response=test_response
                )
                if signal:
                    break
                await asyncio.sleep(2)

        ensure_future(set_response())
        response = await manager.get_response(request_id)

        self.assertEqual(test_response, response)

    async def test_get_response_returns_null_response(self):
        pending_requests: Dict[UUID, Future[ReceiveResponse]] = {}
        request_id: UUID = uuid4()

        manager = RequestManager(pending_requests=pending_requests)

        async def set_response():
            nonlocal manager
            nonlocal request_id

            while True:
                # noinspection PyTypeChecker
                signal = await manager.signal_response(request_id, response=None)
                if signal:
                    break
                await asyncio.sleep(2)

        ensure_future(set_response())
        response = await manager.get_response(request_id)

        self.assertIsNone(response)
