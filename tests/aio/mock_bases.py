import json
from typing import Sequence, AsyncGenerator

from pyapp_ext.messaging.aio import MessageSender, MessageReceiver, Message


class MessageSenderTest(MessageSender):

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
    ):
        self.send_raw_calls.append((
            json.loads(body),
            {"content_type": content_type, "content_encoding": content_encoding}
        ))


class MessageReceiverTest(MessageReceiver):
    def __init__(self, messages: Sequence[str] = None):
        self.open_called = False
        self.close_called = False
        self.delete_calls = []
        self.messages = messages

    async def open(self):
        self.open_called = True

    async def close(self):
        self.close_called = True

    async def receive_raw(self) -> AsyncGenerator[Message, None]:
        content_type = self.default_serialisation.content_type

        for idx, message in enumerate(self.messages):
            yield Message(
                message, content_type, None, idx, self
            )

    async def delete(self, message: Message):
        self.delete_calls.append(message.envelope)

