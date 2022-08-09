
import logging
import asciinema_automation.script
import time
import random


class Instruction:

    def run(self, script):
        pass


class ChangeWaitInstruction(Instruction):
    def __init__(self, wait):
        super().__init__()
        self.wait = wait

    def run(self, script):
        super().run(script)
        script.wait = self.wait


class ChangeDelayInstruction(Instruction):
    def __init__(self, delay):
        super().__init__()
        self.delay = delay

    def run(self, script):
        super().run(script)
        script.delay = self.delay


class ExpectInstruction(Instruction):
    def __init__(self, expect_value: str):
        super().__init__()
        self.expect_value = expect_value

    def run(self, script):
        super().run(script)
        script.process.expect(self.expect_value)


class SendInstruction(Instruction):
    def __init__(self, send_value):
        super().__init__()
        self.send_value = send_value

    def run(self, script):
        super().run(script)

        # Write intruction
        for character in self.send_value:
            if script.standart_deviation is None:
                time.sleep(script.delay)
            else:
                time.sleep(abs(random.gauss(
                    script.delay, script.standart_deviation)))
            script.process.send(str(character))
            script.process.expect(str(character))

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
        script.process.send(self.send_value)


class SendShellInstruction(SendInstruction):

    def __init__(self, command):
        super().__init__(command)

    def run(self, script):
        super().run(script)
        script.process.send("\n")


class SendControlInstruction(Instruction):
    def __init__(self, control):
        super().__init__()
        self.control = control

    def run(self, script):
        super().run(script)
        script.process.sendcontrol(self.control)


class SendArrowInstruction(Instruction):

    KEY_UP = '\x1b[A'
    KEY_DOWN = '\x1b[B'
    KEY_RIGHT = '\x1b[C'
    KEY_LEFT = '\x1b[D'

    def __init__(self, send, num):
        super().__init__()
        self.mapping = dict()
        self.mapping["up"] = '\x1b[A'
        self.mapping["down"] = '\x1b[B'
        self.mapping["right"] = '\x1b[C'
        self.mapping["left"] = '\x1b[D'
        self.send = send
        self.num = num

    def run(self, script):
        super().run(script)
        for _ in range(self.num):
            if script.standart_deviation is None:
                time.sleep(script.delay)
            else:
                time.sleep(abs(random.gauss(
                    script.delay, script.standart_deviation)))
            script.process.sendline(self.mapping[self.send])
