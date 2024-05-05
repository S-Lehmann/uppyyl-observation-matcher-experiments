"""The loggers."""

import logging
import sys
import pprint

from colorama import Fore

##################
# Pretty Printer #
##################
pp = pprint.PrettyPrinter(indent=4, sort_dicts=False)

##########
# Logger #
##########
experiment_log = logging.getLogger('Experiment')
experiment_log.setLevel(logging.DEBUG)

std_out_msg_formatter = logging.Formatter(f'[%(asctime)s]{Fore.CYAN}[%(name)6s]{Fore.RESET} %(message)s', "%H:%M:%S")
std_out_handler = logging.StreamHandler(sys.stdout)
std_out_handler.setFormatter(std_out_msg_formatter)
experiment_log.addHandler(std_out_handler)
