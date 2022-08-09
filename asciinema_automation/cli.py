import argparse
import pathlib
from asciinema_automation.script import Script


def cli():

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'inputfile', help="file containing list of instructions", type=str)
    parser.add_argument(
        'outputfile', help="file containing recording", type=str)

    parser.add_argument('-aa', '--asciinema-arguments', type=str,
                        default="", help="arguments to be passed to asciinema")
    parser.add_argument('-dt', '--delay', type=int, default=150,
                        help="mean for gaussian used to generate time between key strokes")
    parser.add_argument('-wt', '--wait', type=int, default=80,
                        help="time between each instructions")
    parser.add_argument('-sd', '--standart-deviation', type=int, default=60,
                        help="standart deviation for gaussian used to generate time between key strokes")

    # Command line inputs
    inputfile = pathlib.Path(parser.parse_args().inputfile)
    outputfile = pathlib.Path(parser.parse_args().outputfile)
    delay = parser.parse_args().delay
    wait = parser.parse_args().wait
    asciinema_arguments = parser.parse_args().asciinema_arguments
    standart_deviation = parser.parse_args().standart_deviation

    # Script
    script = Script(inputfile, outputfile, asciinema_arguments,
                    wait, delay, standart_deviation)

    #
    script.execute()
