"""
pyApp - Messaging
~~~~~~~~~~~~~~~~~

A simple messaging interface covering Message Queue and Pub/Sub style queues
for distributed applications.

Provides three extensions Messaging-SIO, Messaging-AIO and Messaging-CLI.

Messaging itself does not provide connectivity to messaging services, instead
implementation specific extensions provide client libraries that implement the
queue interfaces.


Message Queues
--------------

This pattern is used for task/job queues where a message is sent to the queue
and then delivered to one of the multiple listeners. This pattern commonly
utilises a timeout and retry mechanism to handle failures in the processing
of a message.

Visually the queue looks like::

                  |--> [Receiver 1]
        [Sender] -|    [Receiver 2]
                  |    [Receiver 2]


While this diagram greatly simplifies the role of the server between the sender
and receiver from your applications point of view that is outside the scope of
what pyApp Messaging provides.


Pub/Sub Queues
--------------

This pattern is used for notifications, event-bus queues where is sent to the
queue and then delivered to all listeners. This allows for events to be broadcast
to all subsystems without a larger application or for notification of events to
systems outside of your application.

Visually the queue looks like::

                     |--> [Subscriber 1]
        [Publisher] -|--> [Subscriber 2]
                     |--> [Subscriber 3]


Again this diagram greatly simplifies the role of the server. Typically messages
in a pub/sub queue are only available while your endpoint is connected. However,
if your applications requires that all events are processed a hybrid approach can
be utilised, see the next section.


Hybrid Queues
-------------

Another common pattern is for pub/sub messages be placed into a task queue for
certain subsystems that require all messages to be processed. A good example is
a system that reacts to certain events and can't miss events.

The configuration of this kind of queues is beyond the scope of pyApp-Messaging
and will depend entirely on the particular queuing server you are using.

Without supporting any particular messaging server, Rabbit MQ makes does allow
for fairly complex hybrid queuing models, while combination of AWS SQS and SNS
can be used to provide a basic hybrid setup.

"""
