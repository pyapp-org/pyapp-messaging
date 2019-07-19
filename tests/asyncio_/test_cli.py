import asyncmock
import pytest

from pyapp.exceptions import NotFound, CannotImport
from pyapp_ext.messaging.asyncio import cli
from pyapp_ext.messaging.exceptions import QueueNotFound


class TestCLI:
    @pytest.mark.asyncio
    async def test_on_new_message(self):
        await cli.on_new_message(
            cli.Message(
                body="Foo",
                content_type="text/plain",
                content_encoding="gzip",
                queue=asyncmock.Mock(),
            )
        )

    def test_send(self, monkeypatch, event_loop):
        mock_factories = asyncmock.Mock()
        mock_factories.get_sender.return_value = mock_sender = asyncmock.AsyncMock()

        monkeypatch.setattr(cli, "factory", mock_factories)

        cli.send("foo", "bar", loop=event_loop)

        mock_factories.get_sender.assert_called_with("bar")
        mock_sender.send.assert_called_with(data="foo")

    def test_send__config_not_found(self, monkeypatch, event_loop):
        mock_factories = asyncmock.Mock()
        mock_factories.get_sender.side_effect = NotFound

        monkeypatch.setattr(cli, "factory", mock_factories)

        actual = cli.send("foo", "bar", loop=event_loop)

        assert actual == -1
        mock_factories.get_sender.assert_called_with("bar")

    def test_send__queue_not_found(self, monkeypatch, event_loop):
        mock_factories = asyncmock.Mock()
        mock_factories.get_sender.return_value = mock_sender = asyncmock.AsyncMock()
        mock_sender.send.side_effect = QueueNotFound

        monkeypatch.setattr(cli, "factory", mock_factories)

        actual = cli.send("foo", "bar", loop=event_loop)

        assert actual == -2
        mock_factories.get_sender.assert_called_with("bar")
        mock_sender.send.assert_called_with(data="foo")

    def test_receiver(self, monkeypatch, event_loop):
        mock_factories = asyncmock.Mock()
        mock_factories.get_receiver.return_value = mock_receiver = asyncmock.AsyncMock()
        mock_receiver.new_message.bind.not_async = True

        monkeypatch.setattr(cli, "factory", mock_factories)

        cli.receiver("foo", loop=event_loop)

        mock_factories.get_receiver.assert_called_with("foo")
        mock_receiver.listen.assert_called()
        mock_receiver.new_message.bind.assert_called_with(cli.on_new_message)

    def test_receiver__config_not_found(self, monkeypatch, event_loop):
        mock_factories = asyncmock.Mock()
        mock_factories.get_receiver.side_effect = NotFound

        monkeypatch.setattr(cli, "factory", mock_factories)

        actual = cli.receiver("foo", loop=event_loop)

        assert actual == -1
        mock_factories.get_receiver.assert_called_with("foo")

    def test_receiver__queue_not_found(self, monkeypatch, event_loop):
        mock_factories = asyncmock.Mock()
        mock_factories.get_receiver.return_value = mock_receiver = asyncmock.AsyncMock()
        mock_receiver.listen.side_effect = QueueNotFound
        mock_receiver.new_message.bind.not_async = True

        monkeypatch.setattr(cli, "factory", mock_factories)

        actual = cli.receiver("foo", loop=event_loop)

        assert actual == -2
        mock_factories.get_receiver.assert_called_with("foo")
        mock_receiver.listen.assert_called()

    def test_configure(self, monkeypatch, event_loop):
        mock_factories = asyncmock.Mock()
        mock_factories.message_sender_factory.available = ["foo"]
        mock_factories.message_sender_factory.create.return_value = (
            mock_sender
        ) = asyncmock.AsyncMock()
        mock_factories.message_receiver_factory.available = ["bar"]
        mock_factories.message_receiver_factory.create.return_value = (
            mock_receiver
        ) = asyncmock.AsyncMock()

        monkeypatch.setattr(cli, "factory", mock_factories)

        cli.configure(loop=event_loop)

        mock_factories.message_sender_factory.create.assert_called_with("foo")
        mock_sender.configure.assert_called()
        mock_factories.message_receiver_factory.create.assert_called_with("bar")
        mock_receiver.configure.assert_called()

    def test_configure__exception(self, monkeypatch, event_loop):
        mock_factories = asyncmock.Mock()

        mock_factories.message_sender_factory.available = ["foo"]
        mock_factories.message_sender_factory.create.return_value = (
            mock_sender
        ) = asyncmock.AsyncMock()
        mock_sender.configure.side_effect = KeyError

        mock_factories.message_receiver_factory.available = ["bar"]
        mock_factories.message_receiver_factory.create.side_effect = CannotImport

        monkeypatch.setattr(cli, "factory", mock_factories)

        cli.configure(loop=event_loop)

        mock_factories.message_sender_factory.create.assert_called_with("foo")
        mock_factories.message_receiver_factory.create.assert_called_with("bar")
        mock_sender.configure.assert_called()
