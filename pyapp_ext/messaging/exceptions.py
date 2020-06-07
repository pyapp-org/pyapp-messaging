"""
Messaging Exceptions
~~~~~~~~~~~~~~~~~~~~
"""


class MessagingError(RuntimeError):
    """
    Base messaging exception
    """


class QueueNotFound(MessagingError):
    """
    Specified Queue was not found.
    """
