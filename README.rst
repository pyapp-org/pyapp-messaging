#################
pyApp - Messaging
#################

*Let use handle the boring stuff!*

The messaging extension provides an abstract interface to various messaging
implementations. This lets your application seamlessly migrate from AMQP to SQS
without any changes to your main application code.


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

    from pyapp.injection import inject_into, FactoryArgs
    from pyapp_ext.messaging import MessageQueue

    @inject_into
    def my_function(queue: MessageQueue = FactoryArgs(name="job_queue")):
        queue.send_message("Do job A")

or using `asyncio`::

    from pyapp.injection import inject_into, FactoryArgs
    from pyapp_ext.messaging import AsyncMessageQueue

    @inject_into
    async def my_function(queue: AsyncMessageQueue = FactoryArgs(name="job_queue")):
        await queue.send_message("Do job A")


API
===
