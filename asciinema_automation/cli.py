import argparse
import logging
import pathlib

from asciinema_automation.script import Script


def cli(argv=None):
    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "inputfile", help="file containing list of instructions", type=str
    )
    parser.add_argument("outputfile", help="file containing recording", type=str)

    parser.add_argument(
        "-aa",
        "--asciinema-arguments",
        type=str,
        default="",
        help="arguments to be passed to asciinema",
    )
    parser.add_argument(
        "-dt",
        "--delay",
        type=int,
        default=150,
        help="mean for gaussian used to generate time between key strokes",
    )
    parser.add_argument(
        "-wt", "--wait", type=int, default=80, help="time between each instructions"
    )
    parser.add_argument(
        "-sd",
        "--standart-deviation",
        type=int,
        default=60,
        help="standart deviation for gaussian used to generate time between key strokes",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=30,
        help="timeout for a command output to come through",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-d",
        "--debug",
        help="set loglevel to DEBUG and output to 'outputfile.log'. Default loglevel to ERROR.",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.ERROR,
    )
    group.add_argument(
        "-v",
        "--verbose",
        help="set loglevel to INFO and output to 'outputfile.log'. Default loglevel to ERROR.",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )

    # Command line inputs
    args = parser.parse_args(argv)
    inputfile = pathlib.Path(args.inputfile)
    outputfile = pathlib.Path(args.outputfile)
    delay = args.delay
    wait = args.wait
    asciinema_arguments = args.asciinema_arguments
    standart_deviation = args.standart_deviation
    loglevel = args.loglevel
    timeout = args.timeout

    # Setup logger
    logfile = None
    if loglevel < logging.ERROR:
        logfile = outputfile.with_suffix(".log")
    logging.basicConfig(filename=logfile, level=loglevel)

    # Script
    script = Script(
        inputfile,
        outputfile,
        asciinema_arguments,
        wait,
        delay,
        standart_deviation,
        timeout,
    )

    #
    script.execute()
