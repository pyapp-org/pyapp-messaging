#################
pyApp - Messaging
#################

*Let use handle the boring stuff!*

.. image:: https://github.com/pyapp-org/pyapp-messaging/workflows/Python%20testing/badge.svg
   :target: https://docs.pyapp.info/
   :alt: ReadTheDocs

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
    from pyapp_ext.messaging.aio import MessageReceiver

    @inject
    def my_function(queue: MessageReceiver = Args(name="job_queue")):
        async for msg in queue.listen():
            print(msg)

