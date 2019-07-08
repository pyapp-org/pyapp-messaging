AMQP = {"default": {"url": "amqp://admin:123@localhost/"}}

SEND_MESSAGE_QUEUES = {
    "amqp": (
        "pyapp_ext.aio_pika.queues.MessageSender",
        {"queue_name": "message-queue"},
    ),
    "aws": (
        "pyapp_ext.aiobotocore.queues.MessageSender",
        {
            "queue_name": "message-queue",
            "client_args": {"endpoint_url": "http://localhost:9324"},
        },
    ),
}

RECEIVE_MESSAGE_QUEUES = {
    "amqp": (
        "pyapp_ext.aio_pika.queues.MessageReceiver",
        {"queue_name": "message-queue"},
    ),
    "aws": (
        "pyapp_ext.aiobotocore.queues.MessageReceiver",
        {
            "queue_name": "message-queue",
            "client_args": {"endpoint_url": "http://localhost:9324"},
        },
    ),
}

PUBLISH_MESSAGE_QUEUES = {
    "amqp": (
        "pyapp_ext.aio_pika.queues.MessagePublisher",
        {"queue_name": "pubsub-queue"},
    ),
    "aws": ("pyapp_ext.aiomq.aws.PubSubQueue", {"url": "http://"}),
}

SUBSCRIBE_MESSAGE_QUEUES = {
    "amqp": (
        "pyapp_ext.aio_pika.queues.MessageSubscriber",
        {"queue_name": "pubsub-queue"},
    ),
    "aws": ("pyapp_ext.aiomq.aws.PubSubQueue", {"url": "http://"}),
}
