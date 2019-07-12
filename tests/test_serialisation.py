import pytest

from pyapp_ext.messaging import serialisation


@pytest.mark.parametrize(
    "target, value",
    (
        (serialisation.PickleSerialise(), "Foo"),
        (serialisation.PickleSerialise(), {"Foo": "Bar"}),
        (serialisation.PickleSerialise(), 123),
        (serialisation.PickleSerialise(), True),
        (serialisation.JSONSerialise(), "Foo"),
        (serialisation.JSONSerialise(), {"Foo": "Bar"}),
        (serialisation.JSONSerialise(), 123),
        (serialisation.JSONSerialise(), True),
    ),
)
def test_content_type__round_trip(target, value):
    data = target.serialise(value)
    actual = target.deserialise(data)

    assert actual == value


@pytest.mark.parametrize(
    "target, value",
    (
        (serialisation.GZipEncoding(serialisation.PickleSerialise()), "Foo"),
        (serialisation.GZipEncoding(serialisation.PickleSerialise()), {"Foo": "Bar"}),
        (serialisation.GZipEncoding(serialisation.PickleSerialise()), 123),
        (serialisation.GZipEncoding(serialisation.PickleSerialise()), True),
        (serialisation.GZipEncoding(serialisation.JSONSerialise()), "Foo"),
        (serialisation.GZipEncoding(serialisation.JSONSerialise()), {"Foo": "Bar"}),
        (serialisation.GZipEncoding(serialisation.JSONSerialise()), 123),
        (serialisation.GZipEncoding(serialisation.JSONSerialise()), True),
    ),
)
def test_content_encoder__round_trip(target, value):
    data = target.serialise(value)
    actual = target.deserialise(data)

    assert actual == value
