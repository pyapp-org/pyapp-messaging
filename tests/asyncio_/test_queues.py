import mock
import pytest

from asyncio import Future

from pyapp_ext.messaging.asyncio import queues


def mock_get_sender(name: str):
    """
    Mocked sender factory that returns mock senders!
    """

    sender = mock.Mock()
    sender.name = name

    for action in ("open", "close", "send_raw"):
        func = Future()
        func.set_result(None)
        getattr(sender, action).return_value = func

    return sender


class TestBroadcastMessagePublisher:
    def test_init(self, monkeypatch):
        monkeypatch.setattr(queues, "get_sender", mock_get_sender)
        target = queues.BroadcastMessagePublisher(target_queues=("foo", "bar"))

        assert len(target._queues) == 2
        assert {q.name for q in target._queues} == {"foo", "bar"}

    @pytest.mark.asyncio
    async def test_open(self, monkeypatch):
        monkeypatch.setattr(queues, "get_sender", mock_get_sender)
        target = queues.BroadcastMessagePublisher(target_queues=("foo", "bar"))

        await target.open()

        for queue in target._queues:
            queue.open.assert_called()

    @pytest.mark.asyncio
    async def test_close(self, monkeypatch):
        monkeypatch.setattr(queues, "get_sender", mock_get_sender)
        target = queues.BroadcastMessagePublisher(target_queues=("foo", "bar"))

        await target.close()

        for queue in target._queues:
            queue.close.assert_called()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "args, kwargs",
        (
            (("foo",), {"content_type": None, "content_encoding": None}),
            (("foo",), {"content_type": "text/plain", "content_encoding": None}),
            (
                ("quibble",),
                {"content_type": "text/plain", "content_encoding": "base64"},
            ),
        ),
    )
    async def test_publish_raw(self, monkeypatch, args, kwargs):
        monkeypatch.setattr(queues, "get_sender", mock_get_sender)
        target = queues.BroadcastMessagePublisher(target_queues=("foo", "bar"))

        await target.publish_raw(*args, **kwargs)

        for queue in target._queues:
            queue.send_raw.assert_called_with(*args, **kwargs)
