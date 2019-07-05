TASK_QUEUES = {}
"""
Task queue definitions

Example settings::

    TASK_QUEUES = {
        "jobs": ("pyapp_ext.aiomq.aws.SQS", {
            "aws_credentials": "default",
            "url": "http://..."
        })
    }

"""

PUBSUB_QUEUES = {}
"""
Task queue definitions

Example settings::

    PUBSUB_QUEUES = {
        "jobs": ("pyapp_ext.aiomq.aws.SNS", {
            "aws_credentials": "default",
            "url": "http://..."
        })
    }

"""
