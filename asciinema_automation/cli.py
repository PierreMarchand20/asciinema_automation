import argparse
from asciinema_automation.script import Script


def cli():

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', type=str)
    parser.add_argument('--asciinema-arguments', type=str, default="")
    parser.add_argument('--delay', type=int, default=150)
    parser.add_argument('--wait', type=int, default=80)
    parser.add_argument('--standart-deviation', type=int, default=60)

    # Command line inputs
    inputfile = parser.parse_args().inputfile
    delay = parser.parse_args().delay
    wait = parser.parse_args().wait
    asciinema_arguments = parser.parse_args().asciinema_arguments
    standart_deviation = parser.parse_args().standart_deviation

    # Script
    script = Script(inputfile, asciinema_arguments,
                    wait, delay, standart_deviation)

    #
    script.execute()
