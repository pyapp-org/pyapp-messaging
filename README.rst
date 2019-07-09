#################
pyApp - Messaging
#################

*Let use handle the boring stuff!*

The messaging extension provides an abstract interface to various messaging
implementations. This lets your application seamlessly migrate from AMQP to SQS
without any changes to your main application code.

.. note:: The primary focus of work is on asyncio based queues.

Installation
============

Install using *pip* or *pipenv*::

    # Using pip
    pip install pyapp-Messaging

    # Using pipenv
    pipenv install pyapp-Messaging



Usage
=====

This library is easiest used with the injection framework eg::

    from pyapp.injection import inject, Args
    from pyapp_ext.messaging import MessageQueue

    @inject
    def my_function(queue: MessageQueue = Args(name="job_queue")):
        queue.send_message("Do job A")

or using `asyncio`::

    from pyapp.injection import inject, Args
    from pyapp_ext.messaging.asyncio import MessageSender

    @inject
    async def my_function(sender: MessageSender = Args(name="job_queue")):
        await sender.send("Do job A")


API
===
