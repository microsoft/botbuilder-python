import pytest

from botbuilder.schema import Activity
from botbuilder.core import MiddlewareSet, Middleware


class TestMiddlewareSet:

    @pytest.mark.asyncio
    async def test_no_middleware(self):
        middleware_set = MiddlewareSet()

        # This shouldn't explode.
        await middleware_set.receive_activity(None)

    @pytest.mark.asyncio
    async def test_no_middleware_with_callback(self):
        callback_complete = False

        middleware_set = MiddlewareSet()

        async def runs_after_pipeline(context):
            nonlocal callback_complete
            callback_complete = True

        await middleware_set.receive_activity_with_status(None, runs_after_pipeline)
        assert callback_complete

    @pytest.mark.asyncio
    async def test_middleware_set_receive_activity_internal(self):

        class PrintMiddleware(object):
            def __init__(self):
                super(PrintMiddleware, self).__init__()

            async def on_process_request(self, context_or_string, next_middleware):
                print('PrintMiddleware says: %s.' % context_or_string)
                return next_middleware

        class ModifyInputMiddleware(Middleware):
            def __init__(self):
                super(ModifyInputMiddleware, self).__init__()

            async def on_process_request(self, context_or_string, next_middleware):
                context_or_string = 'Hello'
                print(context_or_string)
                print('Here is the current context_or_string: %s' % context_or_string)
                return next_middleware

        async def request_handler(context_or_string):
            assert context_or_string == 'Hello'

        middleware_set = MiddlewareSet().use(PrintMiddleware())
        middleware_set.use(ModifyInputMiddleware())

        await middleware_set.receive_activity_internal('Bye', request_handler)

    @pytest.mark.asyncio
    async def test_middleware_run_in_order(self):
        called_first = False
        called_second = False

        class FirstMiddleware(Middleware):
            async def on_process_request(self, context, logic):
                nonlocal called_first, called_second
                assert called_second is False
                called_first = True
                return await logic()

        class SecondMiddleware(Middleware):
            async def on_process_request(self, context, logic):
                nonlocal called_first, called_second
                assert called_first
                called_second = True
                return await logic()

        middleware_set = MiddlewareSet()\
            .use(FirstMiddleware())\
            .use(SecondMiddleware())

        await middleware_set.receive_activity(None)
        assert called_first
        assert called_second

    @pytest.mark.asyncio
    async def test_run_one_middleware(self):
        called_first = False
        finished_pipeline = False

        class FirstMiddleware(Middleware):
            async def on_process_request(self, context, logic):
                nonlocal called_first
                called_first = True
                return await logic()

        middleware_set = MiddlewareSet().use(FirstMiddleware())

        async def runs_after_pipeline(context):
            nonlocal finished_pipeline
            finished_pipeline = True

        await middleware_set.receive_activity_with_status(None, runs_after_pipeline)

        assert called_first
        assert finished_pipeline

    @pytest.mark.asyncio
    async def test_run_empty_pipeline(self):
        ran_empty_pipeline = False
        middleware_set = MiddlewareSet()

        async def runs_after_pipeline(context):
            nonlocal ran_empty_pipeline
            ran_empty_pipeline = True

        await middleware_set.receive_activity_with_status(None, runs_after_pipeline)
        assert ran_empty_pipeline

    @pytest.mark.asyncio
    async def test_two_middleware_one_does_not_call_next(self):
        called_first = False
        called_second = False
        called_all_middleware = False

        class FirstMiddleware(Middleware):
            """First Middleware, does not call next."""
            async def on_process_request(self, context, logic):
                nonlocal called_first, called_second
                assert called_second is False
                called_first = True
                return

        class SecondMiddleware(Middleware):
            async def on_process_request(self, context, logic):
                nonlocal called_all_middleware
                called_all_middleware = True
                return await logic()

        middleware_set = MiddlewareSet()\
            .use(FirstMiddleware())\
            .use(SecondMiddleware())

        await middleware_set.receive_activity(None)
        assert called_first
        assert not called_second
        assert not called_all_middleware

    @pytest.mark.asyncio
    async def test_one_middleware_does_not_call_next(self):
        called_first = False
        finished_pipeline = False

        class FirstMiddleware(Middleware):
            async def on_process_request(self, context, logic):
                nonlocal called_first
                called_first = True
                return

        middleware_set = MiddlewareSet().use(FirstMiddleware())

        async def runs_after_pipeline(context):
            nonlocal finished_pipeline
            finished_pipeline = True

        await middleware_set.receive_activity_with_status(None, runs_after_pipeline)

        assert called_first
        assert not finished_pipeline
