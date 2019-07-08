SEND_MESSAGE_QUEUES = {}
"""
Message sending queue definitions

Example settings::

    SEND_MESSAGE_QUEUES = {
        "amqp": (
            "pyapp_ext.aio_pika.queues.MessageSender",
            {"routing_key": "message-queue"},
        ),
    }
    
"""

RECEIVE_MESSAGE_QUEUES = {}
"""
Message receive queue definitions.

Example settings::

    RECEIVE_MESSAGE_QUEUES = {
        "amqp": (
            "pyapp_ext.aio_pika.queues.MessageReceiver",
            {"queue_name": "message-queue"},
        ),
    }
    
"""


PUBLISH_MESSAGE_QUEUES = {}
"""
Message receive queue definitions.

Example settings::

    PUBLISH_MESSAGE_QUEUES = {
        "amqp": (
            "pyapp_ext.aio_pika.queues.MessagePublisher",
            {"exchange_name": "pubsub-queue"},
        ),
    }

"""

SUBSCRIBE_MESSAGE_QUEUES = {}
"""
Message receive queue definitions.

Example settings::

    SUBSCRIBE_MESSAGE_QUEUES = {
        "amqp": (
            "pyapp_ext.aio_pika.queues.MessageSubscriber",
            {"exchange_name": "pubsub-queue"},
        ),
    }

"""
