import pytest

from pyapp_ext.messaging.aio import Extension
from pyapp_ext.messaging.aio import factory
from pyapp_ext.messaging.aio import bases


class TestExtension:
    @pytest.fixture
    def registry(self):
        from pyapp.injection import default_registry

        default_registry.clear()
        yield default_registry
        default_registry.clear()

    def test_ready(self, registry):
        target = Extension()

        target.ready()

        assert len(registry) == 2
        assert registry[bases.MessageSender] == factory.get_sender
        assert registry[bases.MessageReceiver] == factory.get_receiver
