import abc
import gzip
import json
import pickle

from typing import Any, Union


class Serialise(abc.ABC):
    __slots__ = ()

    content_type: str
    content_encoding: str = None

    @abc.abstractmethod
    def serialise(self, data: Any) -> Union[bytes, str]:
        """
        Serialise native type into bytes.
        """

    @abc.abstractmethod
    def deserialise(self, data: Union[bytes, str]) -> Any:
        """
        Deserialise bytes into native type.
        """


class ContentType(Serialise, abc.ABC):
    """
    Content type serialisation
    """

    __slots__ = ()


class ContentEncoding(Serialise, abc.ABC):
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

    def deserialise(self, data: Union[bytes, str]) -> Any:
        return pickle.loads(data)


class JSONSerialise(ContentType):
    """
    JSON serialisation
    """

    content_type = "application/json"

    def serialise(self, data: Any) -> str:
        return json.dumps(data)

    def deserialise(self, data: Union[bytes, str]) -> Any:
        if isinstance(data, bytes):
            data = data.decode()
        return json.loads(data)


class GZipEncoding(ContentEncoding):
    """
    GZip encoding
    """

    content_encoding = "GZIP"

    def serialise(self, data: Any) -> bytes:
        data = self.content.serialise(data)
        if isinstance(data, str):
            data = data.encode()
        return gzip.compress(data)

    def deserialise(self, data: bytes) -> Any:
        return self.content.deserialise(gzip.decompress(data))
