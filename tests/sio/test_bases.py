from pyapp_ext.messaging.sio import bases


class QueueBaseTest(bases.QueueBase):
    open_called = False
    close_called = False

    def __enter__(self):
        self.open_called = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_called = True


class TestBases:
    def test_context_manager(self):
        with QueueBaseTest() as target:
            assert isinstance(target, QueueBaseTest)
            assert target.open_called is True
            assert target.close_called is False

        assert target.close_called is True
