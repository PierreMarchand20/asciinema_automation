import re
import subprocess
import time
import pexpect
import pexpect.replwrap
import os
import sys
from asciinema_automation.instruction import ShellInstruction, DelayInstruction, WaitInstruction, ControlInstruction


class Script:

    def __init__(self, inputfile, outputfile, asciinema_arguments, wait, delay, standart_deviation, verbosity):

        # Set members
        self.inputfile = inputfile
        self.outputfile = outputfile
        self.asciinema_arguments = asciinema_arguments
        self.delay = delay/1000.
        self.wait = wait/1000.
        self.standart_deviation = standart_deviation/1000.
        self.verbosity = verbosity
        self.instructions = []
        self.process = None

        # Compile regex
        wait_time_regex = re.compile(r'^#\$ wait (\d*)(?!\S)')
        delay_time_regex = re.compile(r'^#\$ delay (\d*)(?!\S)')
        control_command_regex = re.compile(r'^#\$ control ([a-z])(?!\S)')

        # Read script
        with open(inputfile) as f:
            lines = [line.rstrip() for line in f.readlines() if line.strip()]

        for line in lines:
            if line.startswith("#$ wait"):
                wait_time = wait_time_regex.search(line, 0).group(1)
                self.instructions.append(WaitInstruction(int(wait_time)/1000))
            elif line.startswith("#$ delay"):
                delay_time = delay_time_regex.search(line, 0).group(1)
                self.instructions.append(
                    DelayInstruction(int(delay_time)/1000))
            elif line.startswith("#$ control"):
                control_command = control_command_regex.search(
                    line, 0).group(1)
                self.instructions.append(ControlInstruction(control_command))
            elif line.startswith("#"):
                pass
            else:
                self.instructions.append(ShellInstruction(line))

    def execute(self):
        if self.verbosity:
            print("asciinema rec "+self.outputfile +
                  " "+self.asciinema_arguments)
        self.process = pexpect.spawn(
            "asciinema rec "+self.outputfile+" "+self.asciinema_arguments)
        self.process.expect("\n")
        self.process.expect("\n")
        for instruction in self.instructions:
            time.sleep(self.wait)
            instruction.run(self)
        time.sleep(self.wait)
        self.process.sendcontrol('d')
