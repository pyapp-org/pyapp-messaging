import pytest

from pyapp.events import bind_to

from pyapp_ext.messaging.asyncio import bases


class QueueTest(bases.MessageSender):
    def __init__(self):
        self.open_called = False
        self.close_called = False
        self.send_raw_calls = []
        self.publish_raw_calls = []

    async def open(self):
        self.open_called = True

    async def close(self):
        self.close_called = True

    async def send_raw(
        self, body: bytes, *, content_type: str = None, content_encoding: str = None
    ) -> str:
        self.send_raw_calls.append(
            (
                (body,),
                {"content_type": content_type, "content_encoding": content_encoding},
            )
        )
        return "Woo!"

    async def publish_raw(
        self, body: bytes, *, content_type: str = None, content_encoding: str = None
    ):
        self.publish_raw_calls.append(
            (
                (body,),
                {"content_type": content_type, "content_encoding": content_encoding},
            )
        )


@pytest.mark.asyncio
async def test_base_context_manager():
    async with QueueTest() as target:
        assert isinstance(target, QueueTest)
        assert target.open_called is True
        assert target.close_called is False

    assert target.close_called is True


@pytest.mark.asyncio
async def test_message_sender():
    target = QueueTest()

    await target.send(foo="bar", eek=123)

    assert len(target.send_raw_calls) == 1
    assert target.send_raw_calls[0] == (
        ('{"foo": "bar", "eek": 123}',),
        {"content_type": "application/json", "content_encoding": None},
    )


class MessageReceiverTest(bases.MessageReceiver):
    async def listen(self):
        pass  # Do nothing


@pytest.mark.asyncio
async def test_message_receiver():
    target = MessageReceiverTest()

    actual = None

    @bind_to(target.new_message)
    async def callback(msg):
        nonlocal actual
        actual = msg

    await target.receive(b'{"foo": "bar"}', content_type="application/json")

    assert isinstance(actual, bases.Message)
    assert actual.body == {"foo": "bar"}
    assert actual.content_type == "application/json"
