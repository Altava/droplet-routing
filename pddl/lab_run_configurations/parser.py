#! /usr/bin/env python

import logging
import re

from lab.parser import Parser


def main():
    parser = Parser()    
    parser.add_pattern(
        "total_time",
        r"\[t=.+s, \d+ KB\] Total time: (.+)s",
        type=float,
    )
    parser.add_pattern(
        "search_time",
        r"\[t=.+s, \d+ KB\] Search time: (.+)s",
        type=float,
    )
    parser.add_pattern(
        "plan_length",
        r"\[t=.+s, \d+ KB\] Plan length: (\d+) step\(s\).",
        type=int,
    )
    parser.add_pattern(
        "plan_cost",
        r"\[t=.+s, \d+ KB\] Plan cost: (.+)",
        type=float,
    )
    parser.add_pattern(
        "evaluations",
        r"\[t=.+s, \d+ KB\] Evaluations: (.+)",
        type=int,
    )
    parser.add_pattern(
        "expanded_states",
        r"\[t=.+s, \d+ KB\] Expanded (\d+) state\(s\).",
        type=float,
    )
    parser.add_pattern(
        "registered_states",
        r"\[t=.+s, \d+ KB\] Number of registered states: (\d+)",
        type=float,
    )
    parser.parse()


if __name__ == "__main__":
    main()
