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
    parser.parse()


if __name__ == "__main__":
    main()
