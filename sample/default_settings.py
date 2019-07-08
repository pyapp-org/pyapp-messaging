AMQP = {"default": {"url": "amqp://admin:123@localhost/"}}

SEND_MESSAGE_QUEUES = {
    "amqp": (
        "pyapp_ext.aio_pika.queues.MessageSender",
        {"routing_key": "message-queue"},
    ),
    "sqs": ("pyapp_ext.aiomq.aws.MessageQueue", {"url": "http://"}),
}

RECEIVE_MESSAGE_QUEUES = {
    "amqp": (
        "pyapp_ext.aio_pika.queues.MessageReceiver",
        {"queue_name": "message-queue"},
    ),
    "sqs": ("pyapp_ext.aiomq.aws.MessageQueue", {"url": "http://"}),
}

PUBLISH_MESSAGE_QUEUES = {
    "amqp": (
        "pyapp_ext.aio_pika.queues.MessagePublisher",
        {"routing_key": "pubsub-queue"},
    ),
    "sqs": ("pyapp_ext.aiomq.aws.PubSubQueue", {"url": "http://"}),
}

SUBSCRIBE_MESSAGE_QUEUES = {
    "amqp": (
        "pyapp_ext.aio_pika.queues.MessageSubscriber",
        {"exchange_name": "pubsub-queue"},
    ),
    "sqs": ("pyapp_ext.aiomq.aws.PubSubQueue", {"url": "http://"}),
}
