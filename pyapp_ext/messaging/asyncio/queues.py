import asyncio

from typing import Sequence

from .bases import MessageSender, MessageReceiver, Message
from .factory import get_sender, get_receiver


class BroadcastMessagePublisher(MessageSender):
    """
    Message publisher that simulates publishing to a pub/sub style broker by publishing
    to a list of incoming queues.

    This is useful during testing or in the case where messages only need to be
    delivered to a few listening queues.

    :param target_queues: Names of send message queues to publish messages to.

    """

    __slots__ = ("_queues",)

    def __init__(self, *, target_queues: Sequence[str]):
        self._queues = [get_sender(name) for name in target_queues]

    async def open(self):
        aw = [queue.open() for queue in self._queues]
        await asyncio.wait(aw)

    async def close(self):
        aw = [queue.close() for queue in self._queues]
        await asyncio.wait(aw)

    async def send_raw(
        self, body: bytes, *, content_type: str = None, content_encoding: str = None
    ):
        aw = [
            queue.send_raw(
                body, content_type=content_type, content_encoding=content_encoding
            )
            for queue in self._queues
        ]
        await asyncio.wait(aw)


class CombinedQueue(MessageSender, MessageReceiver):
    """
    Queue that combines the Sender and Receiver interfaces into a single proxy
    for underlying queues. This provides a simpler interface for applications
    utilising bi-directional queues/buses.
    """

    @classmethod
    def from_names(cls, *, sender: str, receiver: str):
        return cls(sender=get_sender(sender), receiver=get_receiver(receiver))

    def __init__(self, sender: MessageSender, receiver: MessageReceiver):
        self.sender = sender
        self.receiver = receiver

        self.receiver.new_message.bind(self.on_new_message)

    async def open(self):
        await self.sender.open()
        await self.receiver.open()

    async def close(self):
        await self.receiver.close()
        await self.sender.close()

    async def on_new_message(self, message: Message):
        """
        New message received

        This is more to allow child implementations to override this behaviour.
        """
        await self.new_message(message)

    async def send_raw(
        self, body: bytes, *, content_type: str = None, content_encoding: str = None
    ) -> str:
        return await self.sender.send_raw(
            body, content_type=content_type, content_encoding=content_encoding
        )
