"""
Messaging Exceptions
~~~~~~~~~~~~~~~~~~~~
"""


class MessagingError(Exception):
    """
    Base messaging exception
    """


class QueueNotFound(MessagingError):
    """
    Specified Queue was not found.
    """


class ClientError(MessagingError):
    """
    An error occurred with the client.

    This is to provide a generic response exception type.
    """
