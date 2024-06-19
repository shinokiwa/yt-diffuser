import pytest
from pytest_mock import MockerFixture

import multiprocessing

from yt_diffuser.domains.message.generate import GenerateMessageType, GenerateMessageEntity
from yt_diffuser.types.error import GeneratorExitSignal
from yt_diffuser.adapters.generator.controller import GeneratorController

class TestGeneratorController:
    def test_listen(self, mocker: MockerFixture):
        """
        listen

        
        リクエストの受付を開始する
        """
        usecase = mocker.MagicMock()

        controller = GeneratorController(usecase=usecase)

        recv_queue = multiprocessing.Queue()
        send_queue = multiprocessing.Queue()

        recv_queue.put(GenerateMessageEntity(type=GenerateMessageType.LOAD).model_dump())
        recv_queue.put(GenerateMessageEntity(type=GenerateMessageType.EXIT).model_dump())

        usecase.handle.side_effect = [None, GeneratorExitSignal]

        controller.listen(recv_queue, send_queue)

        assert usecase.handle.call_count == 2, "handle が 2 回呼ばれていること"
        assert usecase.handle.call_args_list[0].args[0] == recv_queue, "handle に recv_queue が渡されていること"
        assert usecase.handle.call_args_list[0].args[1] == send_queue, "handle に send_queue が渡されていること"

