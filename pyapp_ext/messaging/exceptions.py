class MessagingError(Exception):
    pass


class QueueNotFound(MessagingError):
    """
    Specified queue was not found.
    """
