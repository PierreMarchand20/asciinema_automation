
import asciinema_automation.script
import time
import random


class Instruction:

    def run(self, script):
        pass


class ShellInstruction(Instruction):

    def __init__(self, command):
        self.command = command

    def run(self, script):
        for character in self.command:
            if script.standart_deviation is None:
                time.sleep(script.delay)
            else:
                print(script.delay, script.standart_deviation, abs(random.normalvariate(
                    script.delay, script.standart_deviation)))
                time.sleep(abs(random.gauss(
                    script.delay, script.standart_deviation)))

            script.process.send(str(character))
            script.process.expect(str(character))
        script.process.send("\n")
        script.process.expect("\n")


class WaitInstruction(Instruction):
    def __init__(self, wait):
        super().__init__()
        self.wait = wait

    def run(self, script):
        script.wait = self.wait


class DelayInstruction(Instruction):
    def __init__(self, delay):
        super().__init__()
        self.delay = delay

    def run(self, script):
        script.delay = self.delay
