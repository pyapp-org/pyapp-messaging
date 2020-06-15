import pytest

from pyapp.events import bind_to

from pyapp_ext.messaging.aio import bases, Message, MessageSender, MessageReceiver
from pyapp_ext.messaging.aio.bases import QueueBase
from .mock_bases import MessageSenderTest, MessageReceiverTest


class TestQueueBase:
    def test_repr(self):
        target = MessageSenderTest()

        actual = repr(target)

        assert actual == "<MessageSenderTest>"

    @pytest.mark.asyncio
    async def test_base_context_manager(self):
        target = MessageSenderTest()

        async with target:
            assert isinstance(target, MessageSenderTest)
            assert target.open_called is True
            assert target.close_called is False

        assert target.close_called is True


class TestMessageSender:
    @pytest.mark.asyncio
    async def test_send(self):
        target = MessageSenderTest()

        await target.send({"a": "foo"}, b="bar", c=42)

        assert target.send_raw_calls == [(
            {"a": "foo", "b": "bar", "c": 42},
            {
                "content_type": "application/json",
                "content_encoding": None
            }
        )]

    @pytest.mark.asyncio
    async def test_send__dict_only(self):
        target = MessageSenderTest()

        await target.send({"a": "foo", "b": "bar", "c": 42})

        assert target.send_raw_calls == [(
            {"a": "foo", "b": "bar", "c": 42},
            {
                "content_type": "application/json",
                "content_encoding": None
            }
        )]

    @pytest.mark.asyncio
    async def test_send__kwargs_only(self):
        target = MessageSenderTest()

        await target.send(a="foo", b="bar", c=42)

        assert target.send_raw_calls == [(
            {"a": "foo", "b": "bar", "c": 42},
            {
                "content_type": "application/json",
                "content_encoding": None
            }
        )]


class TestMessageReceiver:
    @pytest.mark.asyncio
    async def test_receive__auto_delete(self):
        target = MessageReceiverTest(['{"a":"foo"}', '{"b":"bar","c":42}'])

        actual = []
        async for message in target.listen(auto_delete=True):
            actual.append(message.content)

        assert actual == [{"a": "foo"}, {"b": "bar", "c": 42}]
        assert target.delete_calls == [0, 1]

    @pytest.mark.asyncio
    async def test_receive(self):
        target = MessageReceiverTest(['{"a":"foo"}', '{"b":"bar","c":42}'])

        actual = []
        async for message in target.listen(auto_delete=False):
            actual.append(message.content)

        assert actual == [{"a": "foo"}, {"b": "bar", "c": 42}]
        assert target.delete_calls == []

    @pytest.mark.asyncio
    async def test_receive__manual_delete(self):
        target = MessageReceiverTest(['{"a":"foo"}', '{"b":"bar","c":42}'])

        actual = []
        async for message in target.listen(auto_delete=False):
            actual.append(message.content)
            await message.delete()

        assert actual == [{"a": "foo"}, {"b": "bar", "c": 42}]
        assert target.delete_calls == [0, 1]
