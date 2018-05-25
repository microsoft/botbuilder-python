# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import pytest

from botbuilder.core import AnonymousReceiveMiddleware, MiddlewareSet, Middleware


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

    @pytest.mark.asyncio
    async def test_anonymous_middleware(self):
        did_run = False

        middleware_set = MiddlewareSet()

        async def processor(context, logic):
            nonlocal did_run
            did_run = True
            return await logic()

        middleware_set.use(AnonymousReceiveMiddleware(processor))

        assert not did_run
        await middleware_set.receive_activity(None)
        assert did_run

    @pytest.mark.asyncio
    async def test_anonymous_two_middleware_and_in_order(self):
        called_first = False
        called_second = False

        middleware_set = MiddlewareSet()

        async def processor_one(context, logic):
            nonlocal called_first, called_second
            called_first = True
            assert not called_second
            return await logic()

        async def processor_two(context, logic):
            nonlocal called_first, called_second
            called_second = True
            return await logic()

        middleware_set.use(AnonymousReceiveMiddleware(processor_one))
        middleware_set.use(AnonymousReceiveMiddleware(processor_two))

        await middleware_set.receive_activity(None)
        assert called_first
        assert called_second

    @pytest.mark.asyncio
    async def test_mixed_middleware_anonymous_first(self):
        called_regular_middleware = False
        called_anonymous_middleware = False

        middleware_set = MiddlewareSet()

        class MyFirstMiddleware(Middleware):
            async def on_process_request(self, context, logic):
                nonlocal called_regular_middleware, called_anonymous_middleware
                assert called_anonymous_middleware
                called_regular_middleware = True
                return await logic()

        async def anonymous_method(context, logic):
            nonlocal called_regular_middleware, called_anonymous_middleware
            assert not called_regular_middleware
            called_anonymous_middleware = True
            return await logic()

        middleware_set.use(AnonymousReceiveMiddleware(anonymous_method))
        middleware_set.use(MyFirstMiddleware())

        await middleware_set.receive_activity(None)
        assert called_regular_middleware
        assert called_anonymous_middleware

    @pytest.mark.asyncio
    async def test_mixed_middleware_anonymous_last(self):
        called_regular_middleware = False
        called_anonymous_middleware = False

        middleware_set = MiddlewareSet()

        class MyFirstMiddleware(Middleware):
            async def on_process_request(self, context, logic):
                nonlocal called_regular_middleware, called_anonymous_middleware
                assert not called_anonymous_middleware
                called_regular_middleware = True
                return await logic()

        async def anonymous_method(context, logic):
            nonlocal called_regular_middleware, called_anonymous_middleware
            assert called_regular_middleware
            called_anonymous_middleware = True
            return await logic()

        middleware_set.use(MyFirstMiddleware())
        middleware_set.use(AnonymousReceiveMiddleware(anonymous_method))

        await middleware_set.receive_activity(None)
        assert called_regular_middleware
        assert called_anonymous_middleware

    def test_invalid_middleware_should_not_be_added_to_middleware_set(self):
        middleware_set = MiddlewareSet()

        try:
            middleware_set.use(2)
        except TypeError:
            pass
        except Exception as e:
            raise e
        else:
            raise AssertionError('MiddlewareSet.use(): should not have added an invalid middleware.')
