class MessagingError(Exception):
    pass


class QueueNotFound(MessagingError):
    """
    Specified Queue was not found.
    """
