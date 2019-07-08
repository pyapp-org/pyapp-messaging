import pytest

from pyapp_ext.messaging.asyncio import bases


class QueueBaseTest(bases.QueueBase):
    open_called = False
    close_called = False

    async def open(self):
        self.open_called = True

    async def close(self):
        self.close_called = True


class TestBases:
    @pytest.mark.asyncio
    async def test_context_manager(self):
        async with QueueBaseTest() as target:
            assert isinstance(target, QueueBaseTest)
            assert target.open_called is True
            assert target.close_called is False

        assert target.close_called is True
