import codecs
import re
import subprocess
import time
import pexpect
import pexpect.replwrap
import os
import sys
from asciinema_automation.instruction import ShellInstruction, DelayInstruction, WaitInstruction, ControlInstruction, ExpectInstruction, SendInstruction, SendControlInstruction

# To read escaped character from instructions
# https://stackoverflow.com/a/24519338/5913047
ESCAPE_SEQUENCE_RE = re.compile(r'''
    ( \\U........      # 8-digit hex escapes
    | \\u....          # 4-digit hex escapes
    | \\x..            # 2-digit hex escapes
    | \\[0-7]{1,3}     # Octal escapes
    | \\N\{[^}]+\}     # Unicode characters by name
    | \\[\\'"abfnrtv]  # Single-character escapes
    )''', re.UNICODE | re.VERBOSE)


def decode_escapes(s):
    def decode_match(match):
        return codecs.decode(match.group(0), 'unicode-escape')

    return ESCAPE_SEQUENCE_RE.sub(decode_match, s)


class Script:

    def __init__(self, inputfile, outputfile, asciinema_arguments, wait, delay, standart_deviation, verbosity):

        # Set members from arguments
        self.inputfile = inputfile
        self.outputfile = outputfile
        self.asciinema_arguments = asciinema_arguments
        self.delay = delay/1000.
        self.wait = wait/1000.
        self.standart_deviation = standart_deviation/1000.
        self.verbosity = verbosity

        # Default values for data members
        self.expected = "\n"
        self.send = "\n"

        # Create data members
        self.instructions = []
        self.process = None

        # Compile regex
        wait_time_regex = re.compile(r'^#\$ wait (\d*)(?!\S)')
        delay_time_regex = re.compile(r'^#\$ delay (\d*)(?!\S)')
        control_command_regex = re.compile(r'^#\$ control ([a-z])(?!\S)')
        sendcontrol_command_regex = re.compile(
            r'^#\$ sendcontrol ([a-z])(?!\S)')
        expect_regex = re.compile(
            r'^#\$ expect ([\w\!\@\#\$\%\^\&\*\(\)\_\+\-\=\[\]\{\}\;\'\:\"\\\|\,\.\<\>\/\?]*)(?!\S)')
        send_regex = re.compile(
            r'^#\$ send ([\w\!\@\#\$\%\^\&\*\(\)\_\+\-\=\[\]\{\}\;\'\:\"\\\|\,\.\<\>\/\?]*)(?!\S)')
        check_special_character_regex = re.compile(
            r'\\\\[\w]*')

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
            elif line.startswith("#$ sendcontrol"):
                sendcontrol_command = sendcontrol_command_regex.search(
                    line, 0).group(1)
                self.instructions.append(
                    SendControlInstruction(sendcontrol_command))
            elif line.startswith("#$ expect"):
                expect = ""
                if expect_regex.search(line, 0) is not None:
                    expect = expect_regex.search(line, 0).group(1)
                    if check_special_character_regex.search(repr(expect), 0) is not None:
                        expect = decode_escapes(expect)
                self.instructions.append(ExpectInstruction(expect))
            elif line.startswith("#$ send"):
                send = ""
                if send_regex.search(line, 0) is not None:
                    send = send_regex.search(line, 0).group(1)
                    if check_special_character_regex.search(repr(send), 0) is not None:
                        send = decode_escapes(send)
                self.instructions.append(SendInstruction(expect))
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
        # self.process.logfile = sys.stdout.buffer
        self.process.expect("\n")
        self.process.expect("\n")
        for instruction in self.instructions:
            time.sleep(self.wait)
            instruction.run(self)
        time.sleep(self.wait)
        self.process.sendcontrol('d')
