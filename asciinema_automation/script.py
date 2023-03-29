import codecs
import pathlib
import re
import time
import pexpect
import logging
from asciinema_automation.instruction import ChangeDelayInstruction, ChangeWaitInstruction, ExpectInstruction, SendInstruction, SendShellInstruction, SendControlInstruction, SendArrowInstruction, SendCharacterInstruction

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

    def __init__(self, inputfile: pathlib.Path, outputfile: pathlib.Path, asciinema_arguments: str, wait, delay, standart_deviation, timeout):

        # Set members from arguments
        self.inputfile = inputfile
        self.outputfile = outputfile
        self.asciinema_arguments = asciinema_arguments
        self.delay = delay/1000.
        self.wait = wait/1000.
        self.standart_deviation = standart_deviation/1000.

        # Default values for data members
        self.expected = "\n"
        self.send = "\n"

        # Create data members
        self.instructions = []
        self.process = None

        # Compile regex
        wait_time_regex = re.compile(r'^#\$ wait (\d*)(?!\S)')
        delay_time_regex = re.compile(r'^#\$ delay (\d*)(?!\S)')
        sendcontrol_command_regex = re.compile(
            r'^#\$ sendcontrol ([a-z])(?!\S)')
        sendcharacter_command_regex = re.compile(
            r'^#\$ sendcharacter (.*)(?!\S)')
        expect_regex = re.compile(
            r'^#\$ expect (.*)(?!\S)')
        send_regex = re.compile(
            r'^#\$ send (.*)(?!\S)')
        arrow_command_regex = re.compile(
            r'^#\$ sendarrow (down|up|left|right)(?:\s([\d]+))?(?!\S)')
        arrow_sendline_command_regex = re.compile(
            r'^#\$ sendlinearrow (down|up|left|right)(?:\s([\d]+))?(?!\S)')

        # Read script
        with open(inputfile) as f:
            lines = [line.rstrip() for line in f.readlines() if line.strip()]

        previous_line = ""
        for line in lines:
            if line.startswith("#$ wait"):
                wait_time = wait_time_regex.search(line, 0).group(1)
                self.instructions.append(
                    ChangeWaitInstruction(int(wait_time)/1000))
            elif line.startswith("#$ delay"):
                delay_time = delay_time_regex.search(line, 0).group(1)
                self.instructions.append(
                    ChangeDelayInstruction(int(delay_time)/1000))
            elif line.startswith("#$ sendcontrol"):
                sendcontrol_command = sendcontrol_command_regex.search(
                    line, 0).group(1)
                self.instructions.append(
                    SendControlInstruction(sendcontrol_command))
            elif line.startswith("#$ sendcharacter"):
                sendcharacter_command = sendcharacter_command_regex.search(
                    line, 0).group(1)
                self.instructions.append(
                    SendCharacterInstruction(sendcharacter_command))
            elif line.startswith("#$ sendarrow"):
                arrow_command = arrow_command_regex.search(
                    line, 0).group(1)
                arrow_num = arrow_command_regex.search(
                    line, 0).group(2)
                if arrow_num is None:
                    arrow_num = 1
                self.instructions.append(
                    SendArrowInstruction(arrow_command, int(arrow_num), False))
            elif line.startswith("#$ sendlinearrow"):
                arrow_command = arrow_sendline_command_regex.search(
                    line, 0).group(1)
                arrow_num = arrow_sendline_command_regex.search(
                    line, 0).group(2)
                if arrow_num is None:
                    arrow_num = 1
                self.instructions.append(
                    SendArrowInstruction(arrow_command, int(arrow_num), True))
            elif line.startswith("#$ expect"):
                expect_value = ""
                if expect_regex.search(line, 0) is not None:
                    expect_value = expect_regex.search(line, 0).group(1)
                    expect_value = decode_escapes(expect_value)
                self.instructions.append(
                    ExpectInstruction(expect_value, timeout))
            elif line.startswith("#$ send"):
                send_value = ""
                if send_regex.search(line, 0) is not None:
                    send_value = send_regex.search(line, 0).group(1)
                    send_value = decode_escapes(send_value)
                self.instructions.append(SendInstruction(send_value))
            elif line.startswith("#"):
                pass
            else:
                if line.endswith("\\"):
                    previous_line += line+"\n"
                else:
                    self.instructions.append(
                        SendShellInstruction(previous_line+line))
                    previous_line = ""

    def execute(self):
        spawn_command = "asciinema rec " + \
            str(self.outputfile) + " "+self.asciinema_arguments
        logging.info(spawn_command)
        self.process = pexpect.spawn(spawn_command,
                                     logfile=None)

        self.process.expect("\n")
        logging.debug(self.process.before)
        if not ("recording asciicast to test.cast" in str(self.process.before)):
            self.process.expect(pexpect.EOF)
            self.process.close()
            logging.debug("Exit status:"+str(self.process.exitstatus))
            logging.debug("Signal status:" + str(self.process.signalstatus))
        else:
            self.process.expect("\n")
            logging.debug(self.process.before)
            logging.debug(self.process.after)
            logging.info("Start reading instructions")
            for instruction in self.instructions:
                time.sleep(self.wait)
                instruction.run(self)
            time.sleep(self.wait)
            logging.info("Finished reading instructions")
            self.process.sendcontrol('d')
            self.process.expect(pexpect.EOF)
            self.process.close()
            logging.debug("Exit status:"+str(self.process.exitstatus))
            logging.debug("Signal status:" + str(self.process.signalstatus))
