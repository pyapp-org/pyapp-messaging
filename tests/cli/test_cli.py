import mock
import pytest

from pyapp.exceptions import NotFound, CannotImport
from pyapp_ext.messaging import cli
from pyapp_ext.messaging.exceptions import QueueNotFound


class TestCLI:
    @pytest.mark.asyncio
    async def test_send(self, monkeypatch):
        mock_sender = mock.AsyncMock()
        mock_factory = mock.Mock(
            get_sender=mock.Mock(
                return_value=mock.MagicMock(
                    __aenter__=mock.AsyncMock(return_value=mock_sender)
                )
            )
        )
        monkeypatch.setattr(cli, "factory", mock_factory)

        actual = await cli.Extension.send(mock.Mock(NAME="foo", ARGS={"data": "bar"}))

        assert actual == 0
        mock_factory.get_sender.assert_called_with("foo")
        mock_sender.send.assert_called_with(data="bar")

    @pytest.mark.asyncio
    async def test_send__config_not_found(self, monkeypatch):
        mock_factory = mock.Mock(
            get_sender=mock.Mock(side_effect=NotFound)
        )
        monkeypatch.setattr(cli, "factory", mock_factory)

        actual = await cli.Extension.send(mock.Mock(NAME="foo", ARGS={"data": "bar"}))

        assert actual == 10
        mock_factory.get_sender.assert_called_with("foo")

    @pytest.mark.asyncio
    async def test_send__queue_not_found(self, monkeypatch, event_loop):
        mock_sender = mock.AsyncMock(
            send=mock.AsyncMock(side_effect=QueueNotFound)
        )
        mock_factory = mock.Mock(
            get_sender=mock.Mock(
                return_value=mock.MagicMock(
                    __aenter__=mock.AsyncMock(return_value=mock_sender)
                )
            )
        )
        monkeypatch.setattr(cli, "factory", mock_factory)

        actual = await cli.Extension.send(mock.Mock(NAME="foo", ARGS={"data": "bar"}))

        assert actual == 20
        mock_factory.get_sender.assert_called_with("foo")
        mock_sender.send.assert_called_with(data="bar")

    @pytest.mark.asyncio
    async def test_send_raw(self, monkeypatch):
        mock_sender = mock.AsyncMock()
        mock_factory = mock.Mock(
            get_sender=mock.Mock(
                return_value=mock.MagicMock(
                    __aenter__=mock.AsyncMock(return_value=mock_sender)
                )
            )
        )
        monkeypatch.setattr(cli, "factory", mock_factory)
        mock_file = mock.Mock(
            read=mock.Mock(return_value="eek")
        )
        mock_opts = mock.Mock(
            NAME="foo",
            body=mock_file,
            content_type=None,
            content_encoding=None
        )

        actual = await cli.Extension.send_raw(mock_opts)

        assert actual == 0
        mock_factory.get_sender.assert_called_with("foo")
        mock_sender.send_raw.assert_called_with("eek", content_type=None, content_encoding=None)

    @pytest.mark.asyncio
    async def test_send_raw__config_not_found(self, monkeypatch):
        mock_factory = mock.Mock(
            get_sender=mock.Mock(side_effect=NotFound)
        )
        monkeypatch.setattr(cli, "factory", mock_factory)
        mock_file = mock.Mock(
            read=mock.Mock(return_value="eek")
        )
        mock_opts = mock.Mock(
            NAME="foo",
            body=mock_file,
            content_type=None,
            content_encoding=None
        )

        actual = await cli.Extension.send_raw(mock_opts)

        assert actual == 10
        mock_factory.get_sender.assert_called_with("foo")

    @pytest.mark.asyncio
    async def test_send_raw__queue_not_found(self, monkeypatch, event_loop):
        mock_sender = mock.AsyncMock(
            send_raw=mock.AsyncMock(side_effect=QueueNotFound)
        )
        mock_factory = mock.Mock(
            get_sender=mock.Mock(
                return_value=mock.MagicMock(
                    __aenter__=mock.AsyncMock(return_value=mock_sender)
                )
            )
        )
        monkeypatch.setattr(cli, "factory", mock_factory)
        mock_file = mock.Mock(
            read=mock.Mock(return_value="eek")
        )
        mock_opts = mock.Mock(
            NAME="foo",
            body=mock_file,
            content_type=None,
            content_encoding=None
        )

        actual = await cli.Extension.send_raw(mock_opts)

        assert actual == 20
        mock_factory.get_sender.assert_called_with("foo")
        mock_sender.send_raw.assert_called_with("eek", content_type=None, content_encoding=None)

    def test_receiver__config_not_found(self, monkeypatch, event_loop):
        mock_factory = mock.Mock(
            get_receiver=mock.Mock(side_effect=NotFound)
        )
        monkeypatch.setattr(cli, "factory", mock_factory)
        mock_opts = mock.Mock(
            NAME="foo",
            out=None,
        )

        actual = cli.Extension.receiver(mock_opts, loop=event_loop)

        assert actual == 10
        mock_factory.get_receiver.assert_called_with("foo")

    def test_receiver__queue_not_found(self, monkeypatch, event_loop):
        mock_open = mock.AsyncMock(side_effect=QueueNotFound)
        mock_close = mock.AsyncMock()

        mock_factory = mock.Mock(
            get_receiver=mock.Mock(
                return_value=mock.Mock(
                    open=mock_open, close=mock_close
                )
            )
        )
        monkeypatch.setattr(cli, "factory", mock_factory)
        mock_opts = mock.Mock(
            NAME="foo",
            out=None,
        )

        actual = cli.Extension.receiver(mock_opts, loop=event_loop)

        assert actual == 20
        mock_factory.get_receiver.assert_called_with("foo")
        mock_open.assert_awaited()
        mock_close.assert_awaited()

    def test_receiver__keyboard_exit(self, monkeypatch, event_loop):
        mock_open = mock.AsyncMock(side_effect=KeyboardInterrupt)
        mock_close = mock.AsyncMock()

        mock_factory = mock.Mock(
            get_receiver=mock.Mock(
                return_value=mock.Mock(
                    open=mock_open, close=mock_close
                )
            )
        )
        monkeypatch.setattr(cli, "factory", mock_factory)
        mock_opts = mock.Mock(
            NAME="foo",
            out=None,
        )

        actual = cli.Extension.receiver(mock_opts, loop=event_loop)

        assert actual == 0
        mock_factory.get_receiver.assert_called_with("foo")
        mock_open.assert_awaited()
        mock_close.assert_awaited()

    @pytest.mark.asyncio
    async def test_configure(self, monkeypatch):
        mock_sender = mock.AsyncMock()
        mock_receiver = mock.AsyncMock()
        mock_factory = mock.Mock(
            message_sender_factory=mock.Mock(
                available=["foo"],
                create=mock.Mock(return_value=mock_sender)
            ),
            message_receiver_factory=mock.Mock(
                available=["bar"],
                create=mock.Mock(return_value=mock_receiver)
            )
        )
        monkeypatch.setattr(cli, "factory", mock_factory)

        await cli.Extension.configure(mock.Mock())

        mock_factory.message_sender_factory.create.assert_called_with("foo")
        mock_sender.configure.assert_called()
        mock_factory.message_receiver_factory.create.assert_called_with("bar")
        mock_receiver.configure.assert_called()

    @pytest.mark.asyncio
    async def test_configure__exception(self, monkeypatch):
        mock_sender = mock.AsyncMock(
            configure=mock.AsyncMock(side_effect=KeyError)
        )
        mock_factory = mock.Mock(
            message_sender_factory=mock.Mock(
                available=["foo"],
                create=mock.Mock(return_value=mock_sender)
            ),
            message_receiver_factory=mock.Mock(
                available=["bar"],
                create=mock.Mock(side_effect=CannotImport)
            )
        )
        monkeypatch.setattr(cli, "factory", mock_factory)

        await cli.Extension.configure(mock.Mock())

        mock_factory.message_sender_factory.create.assert_called_with("foo")
        mock_sender.configure.assert_called()
        mock_factory.message_receiver_factory.create.assert_called_with("bar")

    def test_register_commands(self, monkeypatch):
        mock_group = mock.Mock()
        mock_command_group = mock.Mock(
            create_command_group=mock.Mock(return_value=mock_group)
        )

        cli.Extension.register_commands(mock_command_group)

        mock_command_group.create_command_group.assert_called_with("messaging")
        assert mock_group.command.call_count == 4
