import asyncio

from pyapp_ext.messaging.asyncio import cli


class MockCheck:
    __slots__ = ("func", "_calls")

    def __init__(self, func):
        self.func = func
        self._calls = []

    def __call__(self, *args, **kwargs):
        self._calls.append((args, kwargs))
        return self.func(*args, **kwargs)

    def assert_called_with(self, *args, **kwargs):
        assert len(self._calls) > 0, "Not called"
        assert self._calls[-1] == (args, kwargs)


class MockFactories:
    def __init__(self):
        self._actions = {}

    def __getattr__(self, item):
        if item in ["get_sender", "get_receiver", "get_publisher", "get_subscriber"]:
            return self._actions.setdefault(item, MockCheck(self._mock_factory))

        if item in ["send", "listen", "publish", "subscribe"]:
            return self._actions.setdefault(item, MockCheck(self._mock_action))

        raise AttributeError(f"Attribute not found `{item}`")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    def _mock_factory(self, *args, **kwargs):
        return self

    async def _mock_action(self, *args, **kwargs):
        pass


class TestCLI:
    def test_send(self, monkeypatch):
        mock = MockFactories()
        monkeypatch.setattr(cli, "factory", mock)

        cli.send("foo", "bar", loop=asyncio.get_event_loop())

        mock.get_sender.assert_called_with("bar")
        mock.send.assert_called_with({"data": "foo"})

    def test_receiver(self, monkeypatch):
        mock = MockFactories()
        monkeypatch.setattr(cli, "factory", mock)

        cli.receiver("bar", loop=asyncio.get_event_loop())

        mock.get_receiver.assert_called_with("bar")
        mock.listen.assert_called_with()

    def test_publish(self, monkeypatch):
        mock = MockFactories()
        monkeypatch.setattr(cli, "factory", mock)

        cli.publish("foo", "bar", loop=asyncio.get_event_loop())

        mock.get_publisher.assert_called_with("bar")
        mock.publish.assert_called_with({"data": "foo"})

    def test_subscriber(self, monkeypatch):
        mock = MockFactories()
        monkeypatch.setattr(cli, "factory", mock)

        cli.subscriber("bar", loop=asyncio.get_event_loop())

        mock.get_subscriber.assert_called_with("bar")
        mock.subscribe.assert_called_with()
