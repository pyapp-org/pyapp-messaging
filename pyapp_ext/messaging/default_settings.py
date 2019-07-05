MESSAGE_QUEUES = {}
"""
Message queue definitions

Example settings::

    MESSAGE_QUEUES = {
        "jobs": ("pyapp_ext.aiomq.aws.MessageQueue", {
            "aws_credentials": "default",
            "url": "http://..."
        })
    }

"""

PUB_SUB_QUEUES = {}
"""
Pub/Sub queue definitions

Example settings::

    PUB_SUB_QUEUES = {
        "jobs": ("pyapp_ext.aiomq.aws.PubSubQueue", {
            "aws_credentials": "default",
            "url": "http://..."
        })
    }

"""
