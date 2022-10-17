#! /usr/bin/env python

import logging
import re

from lab.parser import Parser

def parse_times_over_time(content, props):
    matches = re.findall(r"Found plan after (\d+) sec.", content)
    props["times_over_time"] = [float(s) for s in matches]

def parse_plan_length_over_time(content, props):
    matches = re.findall(r"Plan length: (\d+) step\(s\).", content)
    props["plan_length_over_time"] = [int(s) for s in matches]

def parse_plan_cost_over_time(content, props):
    matches = re.findall(r"Makespan   : (.+)", content)
    props["plan_cost_over_time"] = [float(s) for s in matches]

def main():
    parser = Parser()    
    parser.add_function(parse_times_over_time)
    parser.add_function(parse_plan_length_over_time)
    parser.add_function(parse_plan_cost_over_time)
    parser.parse()

if __name__ == "__main__":
    main()
