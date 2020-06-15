from .mock_bases import MessageSenderTest, MessageReceiverTest


class TestQueueBase:
    def test_repr(self):
        target = MessageSenderTest()

        actual = repr(target)

        assert actual == "<MessageSenderTest>"

    def test_base_context_manager(self):
        target = MessageSenderTest()

        with target:
            assert isinstance(target, MessageSenderTest)
            assert target.open_called is True
            assert target.close_called is False

        assert target.close_called is True


class TestMessageSender:
    def test_send(self):
        target = MessageSenderTest()

        target.send({"a": "foo"}, b="bar", c=42)

        assert target.send_raw_calls == [(
            {"a": "foo", "b": "bar", "c": 42},
            {
                "content_type": "application/json",
                "content_encoding": None
            }
        )]

    def test_send__dict_only(self):
        target = MessageSenderTest()

        target.send({"a": "foo", "b": "bar", "c": 42})

        assert target.send_raw_calls == [(
            {"a": "foo", "b": "bar", "c": 42},
            {
                "content_type": "application/json",
                "content_encoding": None
            }
        )]

    def test_send__kwargs_only(self):
        target = MessageSenderTest()

        target.send(a="foo", b="bar", c=42)

        assert target.send_raw_calls == [(
            {"a": "foo", "b": "bar", "c": 42},
            {
                "content_type": "application/json",
                "content_encoding": None
            }
        )]


class TestMessageReceiver:
    def test_receive__auto_delete(self):
        target = MessageReceiverTest(['{"a":"foo"}', '{"b":"bar","c":42}'])

        actual = []
        for message in target.listen(auto_delete=True):
            actual.append(message.content)

        assert actual == [{"a": "foo"}, {"b": "bar", "c": 42}]
        assert target.delete_calls == [0, 1]

    def test_receive(self):
        target = MessageReceiverTest(['{"a":"foo"}', '{"b":"bar","c":42}'])

        actual = []
        for message in target.listen(auto_delete=False):
            actual.append(message.content)

        assert actual == [{"a": "foo"}, {"b": "bar", "c": 42}]
        assert target.delete_calls == []

    def test_receive__manual_delete(self):
        target = MessageReceiverTest(['{"a":"foo"}', '{"b":"bar","c":42}'])

        actual = []
        for message in target.listen(auto_delete=False):
            actual.append(message.content)
            message.delete()

        assert actual == [{"a": "foo"}, {"b": "bar", "c": 42}]
        assert target.delete_calls == [0, 1]
