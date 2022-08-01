import argparse
from asciinema_automation.script import Script


def cli():

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', type=str)
    parser.add_argument('outputfile', type=str)
    parser.add_argument('-aa', '--asciinema-arguments', type=str, default="")
    parser.add_argument('-d', '--delay', type=int, default=150)
    parser.add_argument('-w', '--wait', type=int, default=80)
    parser.add_argument('-sd', '--standart-deviation', type=int, default=60)
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity", action="store_true")

    # Command line inputs
    inputfile = parser.parse_args().inputfile
    outputfile = parser.parse_args().outputfile
    delay = parser.parse_args().delay
    wait = parser.parse_args().wait
    asciinema_arguments = parser.parse_args().asciinema_arguments
    standart_deviation = parser.parse_args().standart_deviation
    verbosity = parser.parse_args().verbose

    # Script
    script = Script(inputfile, outputfile, asciinema_arguments,
                    wait, delay, standart_deviation, verbosity)

    #
    script.execute()
