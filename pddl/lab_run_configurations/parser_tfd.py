#! /usr/bin/env python

import logging
import re

from lab.parser import Parser


def main():
    parser = Parser()    
    parser.add_pattern(
        "search_time",
        r"Search time: (.+) seconds - Walltime: .+ seconds",
        type=float,
    )
    parser.add_pattern(
        "total_time",
        r"Total time: (.+) seconds - Walltime: .+ seconds",
        type=float,
    )
    parser.add_pattern(
        "plan_length",
        r"Plan length: (\d+) step\(s\).",
        type=int,
    )
    parser.add_pattern(
        "plan_cost",
        r"Makespan   : (.+)",
        type=float,
    )
    parser.add_pattern(
        "branching_factor",
        r"Overall branching factor by list sizes: (.+)",
        type=float,
    )
    parser.add_pattern(
        "expanded_states",
        r"Expanded Nodes: (\d+) state\(s\).",
        type=int,
    )
    parser.add_pattern(
        "generated_nodes",
        r"Generated Nodes: (\d+) state\(s\).",
        type=int,
    )
    parser.parse()


if __name__ == "__main__":
    main()
