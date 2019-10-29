import aiounittest
from botbuilder.core import AutoSaveStateMiddleware, BotState, TurnContext
from botbuilder.core.adapters import TestAdapter
from botbuilder.schema import Activity


async def aux_func():
    return


class BotStateMock(BotState):
    def __init__(self, state):  # pylint: disable=super-init-not-called
        self.state = state
        self.assert_force = False
        self.read_called = False
        self.write_called = False

    async def load(self, turn_context: TurnContext, force: bool = False) -> None:
        assert turn_context is not None, "BotStateMock.load() not passed context."
        if self.assert_force:
            assert force, "BotStateMock.load(): force not set."
        self.read_called = True

    async def save_changes(
        self, turn_context: TurnContext, force: bool = False
    ) -> None:
        assert (
            turn_context is not None
        ), "BotStateMock.save_changes() not passed context."
        if self.assert_force:
            assert force, "BotStateMock.save_changes(): force not set."
        self.write_called = True

    def get_storage_key(
        self, turn_context: TurnContext  # pylint: disable=unused-argument
    ) -> str:
        return ""


class TestAutoSaveMiddleware(aiounittest.AsyncTestCase):
    async def test_should_add_and_call_load_all_on_single_plugin(self):
        adapter = TestAdapter()
        context = TurnContext(adapter, Activity())
        foo_state = BotStateMock({"foo": "bar"})
        bot_state_set = AutoSaveStateMiddleware().add(foo_state)
        await bot_state_set.bot_state_set.load_all(context)

    async def test_should_add_and_call_load_all_on_multiple_plugins(self):
        adapter = TestAdapter()
        context = TurnContext(adapter, Activity())
        foo_state = BotStateMock({"foo": "bar"})
        bar_state = BotStateMock({"bar": "foo"})
        bot_state_set = AutoSaveStateMiddleware([foo_state, bar_state])
        await bot_state_set.bot_state_set.load_all(context)

    async def test_should_add_and_call_save_all_changes_on_a_single_plugin(self):
        adapter = TestAdapter()
        context = TurnContext(adapter, Activity())
        foo_state = BotStateMock({"foo": "bar"})
        bot_state_set = AutoSaveStateMiddleware().add(foo_state)
        await bot_state_set.bot_state_set.save_all_changes(context)
        assert foo_state.write_called, "write not called for plugin."

    async def test_should_add_and_call_save_all_changes_on_multiple_plugins(self):
        adapter = TestAdapter()
        context = TurnContext(adapter, Activity())
        foo_state = BotStateMock({"foo": "bar"})
        bar_state = BotStateMock({"bar": "foo"})
        autosave_middleware = AutoSaveStateMiddleware([foo_state, bar_state])
        await autosave_middleware.bot_state_set.save_all_changes(context)
        assert (
            foo_state.write_called or bar_state.write_called
        ), "write not called for either plugin."
        assert foo_state.write_called, "write not called for 'foo_state' plugin."
        assert bar_state.write_called, "write not called for 'bar_state' plugin."

    async def test_should_pass_force_flag_through_in_load_all_call(self):
        adapter = TestAdapter()
        context = TurnContext(adapter, Activity())
        foo_state = BotStateMock({"foo": "bar"})
        foo_state.assert_force = True
        autosave_middleware = AutoSaveStateMiddleware().add(foo_state)
        await autosave_middleware.bot_state_set.load_all(context, True)

    async def test_should_pass_force_flag_through_in_save_all_changes_call(self):
        adapter = TestAdapter()
        context = TurnContext(adapter, Activity())
        foo_state = BotStateMock({"foo": "bar"})
        foo_state.assert_force = True
        autosave_middleware = AutoSaveStateMiddleware().add(foo_state)
        await autosave_middleware.bot_state_set.save_all_changes(context, True)

    async def test_should_work_as_a_middleware_plugin(self):
        adapter = TestAdapter()
        context = TurnContext(adapter, Activity())
        foo_state = BotStateMock({"foo": "bar"})
        autosave_middleware = AutoSaveStateMiddleware().add(foo_state)
        await autosave_middleware.on_turn(context, aux_func)
        assert foo_state.write_called, "save_all_changes() not called."

    async def test_should_support_plugins_passed_to_constructor(self):
        adapter = TestAdapter()
        context = TurnContext(adapter, Activity())
        foo_state = BotStateMock({"foo": "bar"})
        autosave_middleware = AutoSaveStateMiddleware().add(foo_state)
        await autosave_middleware.on_turn(context, aux_func)
        assert foo_state.write_called, "save_all_changes() not called."

    async def test_should_not_add_any_bot_state_on_construction_if_none_are_passed_in(
        self,
    ):
        middleware = AutoSaveStateMiddleware()
        assert (
            not middleware.bot_state_set.bot_states
        ), "should not have added any BotState."
