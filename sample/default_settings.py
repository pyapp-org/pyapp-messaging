SEND_MESSAGE_QUEUES = {
    "amqp": ("pyapp_ext.aio_pika.queues.MessageSend", {"routing_key": "message-queue"}),
    "sqs": ("pyapp_ext.aiomq.aws.MessageQueue", {"url": "http://"}),
}

RECEIVE_MESSAGE_QUEUES = {
    "amqp": ("pyapp_ext.aio_pika.queues.MessageReceiver", {"queue_name": "test_receive"}),
    "sqs": ("pyapp_ext.aiomq.aws.MessageQueue", {"url": "http://"}),
}

PUB_SUB_QUEUES = {
    "amqp": ("pyapp_ext.aio_pika.queues.PubSubQueue", {"url": "http://"}),
    "sqs": ("pyapp_ext.aiomq.aws.PubSubQueue", {"url": "http://"}),
}
