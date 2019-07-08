import abc
import gzip
import json
import pickle

from typing import Any


class Serialise(abc.ABC):
    __slots__ = ()

    content_type: str
    content_encoding: str = None

    @abc.abstractmethod
    def serialise(self, data: Any) -> bytes:
        """
        Serialise native type into bytes.
        """

    @abc.abstractmethod
    def deserialise(self, data: bytes) -> Any:
        """
        Deserialise bytes into native type.
        """


class ContentType(Serialise, metaclass=abc.ABCMeta):
    """
    Content type serialisation
    """

    __slots__ = ()


class ContentEncoding(Serialise, metaclass=abc.ABCMeta):
    """
    Content encoding serialisation
    """

    __slots__ = ("content", "content_type")

    def __init__(self, content: ContentType):
        self.content = content
        self.content_type = self.content.content_type


class PickleSerialise(ContentType):
    """
    Pickle serialisation
    """

    content_type = "application/python-pickle"

    def serialise(self, data: Any) -> bytes:
        return pickle.dumps(data)

    def deserialise(self, data: bytes) -> Any:
        return pickle.loads(data)


class JSONSerialise(ContentType):
    """
    JSON serialisation
    """

    content_type = "application/json"

    def serialise(self, data: Any) -> bytes:
        return json.dumps(data).encode()

    def deserialise(self, data: bytes) -> Any:
        return json.loads(data.decode())


class GZipEncoding(ContentEncoding):
    """
    GZip encoding
    """

    content_encoding = "GZIP"

    def serialise(self, data: Any) -> bytes:
        return gzip.compress(self.content.serialise(data))

    def deserialise(self, data: bytes) -> Any:
        return self.content.deserialise(gzip.decompress(data))
