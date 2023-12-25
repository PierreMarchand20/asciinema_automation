import logging
import random
import re
import time
from typing import List

from .script import Instruction, Script

logger = logging.getLogger(__name__)


class ChangeWaitInstruction(Instruction):
    def __init__(self, wait: float):
        super().__init__()
        self.wait = wait

    def run(self, script: Script) -> None:
        super().run(script)
        logger.debug("%s->%s", script.wait, self.wait)
        script.wait = self.wait


class ChangeDelayInstruction(Instruction):
    def __init__(self, delay: float):
        super().__init__()
        self.delay = delay

    def run(self, script: Script) -> None:
        super().run(script)
        logger.debug("%s->%s", script.delay, self.delay)
        script.delay = self.delay


class ExpectInstruction(Instruction):
    def __init__(self, expect_value: str, timeout: int):
        super().__init__()
        self.expect_value = expect_value
        self.timeout = timeout

    def run(self, script: Script) -> None:
        super().run(script)
        logger.debug("Expect %s", repr(self.expect_value))
        script.process.expect(self.expect_value, timeout=self.timeout)


class SendInstruction(Instruction):
    def __init__(self, send_value: str):
        super().__init__()
        self.send_value = send_value

    def run(self, script: Script) -> None:
        super().run(script)
        logger.debug("Send %s", repr(self.send_value))
        # self.receive_value = self.send_value

        # Check for special character
        self.receive_value: List[str] = [re.escape(c) for c in list(self.send_value)]

        # Write intruction
        for send_character, receive_character in zip(
            self.send_value, self.receive_value
        ):
            if script.standard_deviation is None:
                time.sleep(script.delay)
            else:
                time.sleep(abs(random.gauss(script.delay, script.standard_deviation)))
            script.process.send(str(send_character))
            script.process.expect(str(receive_character))

        # End instruction
        if script.standard_deviation is None:
            time.sleep(script.delay)
        else:
            time.sleep(abs(random.gauss(script.delay, script.standard_deviation)))


class SendCharacterInstruction(Instruction):
    def __init__(self, send_value: str):
        super().__init__()
        self.send_value = send_value

    def run(self, script: Script) -> None:
        super().run(script)
        logger.debug("Send '%s'", self.send_value)
        script.process.send(self.send_value)


class SendShellInstruction(SendInstruction):
    def __init__(self, command: str):
        super().__init__(command)

    def run(self, script: Script) -> None:
        super().run(script)
        logger.debug("Send '\\n'")
        script.process.send("\n")


class SendControlInstruction(Instruction):
    def __init__(self, control: str):
        super().__init__()
        self.control = control

    def run(self, script: Script) -> None:
        super().run(script)
        logger.debug("Send ctrl+%s", self.control)
        script.process.sendcontrol(self.control)


class SendArrowInstruction(Instruction):
    KEY_UP = "\x1b[A"
    KEY_DOWN = "\x1b[B"
    KEY_RIGHT = "\x1b[C"
    KEY_LEFT = "\x1b[D"

    def __init__(self, send: str, num: int, enter: bool = False):
        super().__init__()
        self.mapping = dict()
        self.mapping["up"] = "\x1b[A"
        self.mapping["down"] = "\x1b[B"
        self.mapping["right"] = "\x1b[C"
        self.mapping["left"] = "\x1b[D"
        self.send = send
        self.num = num
        self.enter = enter

    def run(self, script: Script) -> None:
        super().run(script)
        logger.debug("Send %s arrow %i times", self.send, self.num)
        for _ in range(self.num):
            if script.standard_deviation is None:
                time.sleep(script.delay)
            else:
                time.sleep(abs(random.gauss(script.delay, script.standard_deviation)))
            if self.enter:
                script.process.sendline(self.mapping[self.send])
            else:
                script.process.send(self.mapping[self.send])
