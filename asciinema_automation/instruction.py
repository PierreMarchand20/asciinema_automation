
import logging
import time
import random


class Instruction:

    def run(self, script):
        logging.info(self.__class__.__name__)


class ChangeWaitInstruction(Instruction):
    def __init__(self, wait):
        super().__init__()
        self.wait = wait

    def run(self, script):
        super().run(script)
        logging.debug("%s->%s", script.wait, self.wait)
        script.wait = self.wait


class ChangeDelayInstruction(Instruction):
    def __init__(self, delay):
        super().__init__()
        self.delay = delay

    def run(self, script):
        super().run(script)
        logging.debug("%s->%s", script.delay, self.delay)
        script.delay = self.delay


class ExpectInstruction(Instruction):
    def __init__(self, expect_value: str, timeout: int):
        super().__init__()
        self.expect_value = expect_value
        self.timeout = timeout

    def run(self, script):
        super().run(script)
        logging.debug("Expect %s", repr(self.expect_value))
        script.process.expect(self.expect_value, timeout=self.timeout)


class SendInstruction(Instruction):
    def __init__(self, send_value):
        super().__init__()
        self.send_value = send_value

    def run(self, script):
        super().run(script)
        logging.debug("Send %s", repr(self.send_value))
        self.receive_value = self.send_value

        # Check for special character
        if "\\" in self.send_value:
            self.receive_value = [character if character !=
                                  '\\' else character+'\\' for character in list(self.send_value)]

        # Write intruction
        for send_character, receive_character in zip(self.send_value, self.receive_value):
            if script.standart_deviation is None:
                time.sleep(script.delay)
            else:
                time.sleep(abs(random.gauss(
                    script.delay, script.standart_deviation)))
            script.process.send(str(send_character))
            script.process.expect(str(receive_character))

        # End instruction
        if script.standart_deviation is None:
            time.sleep(script.delay)
        else:
            time.sleep(abs(random.gauss(
                script.delay, script.standart_deviation)))


class SendCharacterInstruction(Instruction):
    def __init__(self, send_value):
        super().__init__()
        self.send_value = send_value

    def run(self, script):
        super().run(script)
        logging.debug("Send '%s'", self.send_value)
        script.process.send(self.send_value)


class SendShellInstruction(SendInstruction):

    def __init__(self, command):
        super().__init__(command)

    def run(self, script):
        super().run(script)
        logging.debug("Send '\\n'")
        script.process.send("\n")


class SendControlInstruction(Instruction):
    def __init__(self, control):
        super().__init__()
        self.control = control

    def run(self, script):
        super().run(script)
        logging.debug("Send ctrl+%s", self.control)
        script.process.sendcontrol(self.control)


class SendArrowInstruction(Instruction):

    KEY_UP = '\x1b[A'
    KEY_DOWN = '\x1b[B'
    KEY_RIGHT = '\x1b[C'
    KEY_LEFT = '\x1b[D'

    def __init__(self, send, num, enter=False):
        super().__init__()
        self.mapping = dict()
        self.mapping["up"] = '\x1b[A'
        self.mapping["down"] = '\x1b[B'
        self.mapping["right"] = '\x1b[C'
        self.mapping["left"] = '\x1b[D'
        self.send = send
        self.num = num
        self.enter = enter

    def run(self, script):
        super().run(script)
        logging.debug("Send %s arrow %i times", self.send, self.num)
        for _ in range(self.num):
            if script.standart_deviation is None:
                time.sleep(script.delay)
            else:
                time.sleep(abs(random.gauss(
                    script.delay, script.standart_deviation)))
            if self.enter:
                script.process.sendline(self.mapping[self.send])
            else:
                script.process.send(self.mapping[self.send])
