AMQP = {"default": {"url": "amqp://admin:123@localhost/"}}

AWS_CREDENTIALS = {"default": {"region": "ap-southeast-2"}}


SEND_MESSAGE_QUEUES = {
    "amqp-direct": (
        "pyapp_ext.aio_pika.queues.DirectSender",
        {"queue_name": "message-queue"},
    ),
    "amqp-fanout": (
        "pyapp_ext.aio_pika.queues.FanOutSender",
        {"queue_name": "message-queue"},
    ),
    "aws": (
        "pyapp_ext.aiobotocore.queues.SQSSender",
        {
            "queue_name": "message-queue",
            "client_args": {"endpoint_url": "http://localhost:9324"},
        },
    ),
    "bcast": (
        "pyapp_ext.messaging.asyncio.queues.BroadcastMessagePublisher",
        {"target_queues": ["aws"]},
    ),
}

RECEIVE_MESSAGE_QUEUES = {
    "amqp-direct": (
        "pyapp_ext.aio_pika.queues.Receiver",
        {"queue_name": "message-queue"},
    ),
    "amqp-fanout": (
        "pyapp_ext.aio_pika.queues.FanOutReceiver",
        {"queue_name": "message-queue"},
    ),
    "aws": (
        "pyapp_ext.aiobotocore.queues.SQSReceiver",
        {
            "queue_name": "message-queue",
            "client_args": {"endpoint_url": "http://localhost:9324"},
        },
    ),
}
