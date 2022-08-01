
import asciinema_automation.script
import time
import random


class Instruction:

    def run(self, script):
        if script.verbosity:
            print(self.__class__.__name__)
        pass


class ShellInstruction(Instruction):

    def __init__(self, command):
        self.command = command

    def run(self, script):
        super().run(script)
        # Write intruction
        for character in self.command:
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
        script.process.send("\n")
        script.process.expect(script.expected)


class WaitInstruction(Instruction):
    def __init__(self, wait):
        super().__init__()
        self.wait = wait

    def run(self, script):
        super().run(script)
        script.wait = self.wait


class DelayInstruction(Instruction):
    def __init__(self, delay):
        super().__init__()
        self.delay = delay

    def run(self, script):
        super().run(script)
        script.delay = self.delay


class ControlInstruction(Instruction):
    def __init__(self, control):
        super().__init__()
        self.control = control

    def run(self, script):
        super().run(script)
        script.process.sendcontrol(self.control)


class ExpectInstruction(Instruction):
    def __init__(self, expect):
        super().__init__()
        self.expect = expect

    def run(self, script):
        super().run(script)
        script.expected = self.expect
