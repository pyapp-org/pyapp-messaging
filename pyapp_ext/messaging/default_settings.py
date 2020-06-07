SEND_MESSAGE_QUEUES = {}
"""
Message sending queue definitions

Example settings::

    SEND_MESSAGE_QUEUES = {
        "amqp": (
            "pyapp_ext.aio_pika.queues.MessageSender",
            {"routing_key": "message-queue"},
        ),
        "sqs": (
            "pyapp_ext.aiobotocore.queues.SQSSender",
            {"queue_url": "https://..."}
        )
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
        "sqs": (
            "pyapp_ext.aiobotocore.queues.SQSReceiver",
            {"queue_url": "https://..."}
        )
    }
    
"""
