import codecs
import logging
import pathlib
import re

from .instruction import (
    ChangeDelayInstruction,
    ChangeWaitInstruction,
    ExpectInstruction,
    SendArrowInstruction,
    SendCharacterInstruction,
    SendControlInstruction,
    SendInstruction,
    SendShellInstruction,
)
from .script import Instruction

logger = logging.getLogger(__name__)

# To read escaped character from instructions
# https://stackoverflow.com/a/24519338/5913047
ESCAPE_SEQUENCE_RE = re.compile(
    r"""
    ( \\U........      # 8-digit hex escapes
    | \\u....          # 4-digit hex escapes
    | \\x..            # 2-digit hex escapes
    | \\[0-7]{1,3}     # Octal escapes
    | \\N\{[^}]+\}     # Unicode characters by name
    | \\[\\'"abfnrtv]  # Single-character escapes
    )""",
    re.UNICODE | re.VERBOSE,
)


def decode_escapes(s: str) -> str:
    def decode_match(match: re.Match[str]) -> str:
        return codecs.decode(match.group(0), "unicode-escape")

    return ESCAPE_SEQUENCE_RE.sub(decode_match, s)


def parse_script_file(inputfile: pathlib.Path, timeout: int) -> list["Instruction"]:
    # Compile regex
    wait_time_regex = re.compile(r"^#\$ wait (\d*)(?!\S)")
    delay_time_regex = re.compile(r"^#\$ delay (\d*)(?!\S)")
    sendcontrol_command_regex = re.compile(r"^#\$ sendcontrol ([a-z])(?!\S)")
    sendcharacter_command_regex = re.compile(r"^#\$ sendcharacter (.*)(?!\S)")
    expect_regex = re.compile(r"^#\$ expect (.*)(?!\S)")
    send_regex = re.compile(r"^#\$ send (.*)(?!\S)")
    arrow_command_regex = re.compile(
        r"^#\$ sendarrow (down|up|left|right)(?:\s([\d]+))?(?!\S)"
    )
    arrow_sendline_command_regex = re.compile(
        r"^#\$ sendlinearrow (down|up|left|right)(?:\s([\d]+))?(?!\S)"
    )

    instructions: list[Instruction] = []

    with open(inputfile) as file:
        previous_line = ""
        for line in file:
            if line.strip():
                line = line.rstrip()

                if match := wait_time_regex.search(line, 0):
                    wait_time = match.group(1)
                    instructions.append(ChangeWaitInstruction(int(wait_time) / 1000))
                elif match := delay_time_regex.search(line, 0):
                    delay_time = match.group(1)
                    instructions.append(ChangeDelayInstruction(int(delay_time) / 1000))
                elif match := sendcontrol_command_regex.search(line, 0):
                    sendcontrol_command = match.group(1)
                    instructions.append(SendControlInstruction(sendcontrol_command))
                elif match := sendcharacter_command_regex.search(line, 0):
                    sendcharacter_command = match.group(1)
                    instructions.append(SendCharacterInstruction(sendcharacter_command))
                elif match := arrow_command_regex.search(line, 0):
                    arrow_command = match.group(1)
                    arrow_num = match.group(2)
                    if arrow_num is None:
                        arrow_num = 1
                    instructions.append(
                        SendArrowInstruction(arrow_command, int(arrow_num), False)
                    )
                elif match := arrow_sendline_command_regex.search(line, 0):
                    arrow_command = match.group(1)
                    arrow_num = match.group(2)
                    if arrow_num is None:
                        arrow_num = 1
                    instructions.append(
                        SendArrowInstruction(arrow_command, int(arrow_num), True)
                    )
                elif match := expect_regex.search(line, 0):
                    expect_value = match.group(1)
                    expect_value = decode_escapes(expect_value)
                    instructions.append(ExpectInstruction(expect_value, timeout))
                elif match := send_regex.search(line, 0):
                    send_value = match.group(1)
                    send_value = decode_escapes(send_value)
                    instructions.append(SendInstruction(send_value))
                elif line.startswith("#"):
                    pass
                else:
                    if line.endswith("\\"):
                        previous_line += line + "\n"
                    else:
                        instructions.append(SendShellInstruction(previous_line + line))
                        previous_line = ""

    return instructions
