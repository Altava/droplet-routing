#! /usr/bin/env python
# import glob
import os
import platform

from pathlib import Path
from downward.reports import Report
from downward.suites import build_suite
from lab.environments import BaselSlurmEnvironment, LocalEnvironment
from lab.experiment import Experiment
from lab import tools


# Create custom report class with suitable info and error attributes.
# class BaseReport(AbsoluteReport):
#     INFO_ATTRIBUTES = ["time_limit", "memory_limit", "seed"]
#     ERROR_ATTRIBUTES = [
#         "domain",
#         "problem",
#         "algorithm",
#         "unexplained_errors",
#         "error",
#         "node",
#     ]


NODE = platform.node()
REMOTE = NODE.endswith(".scicore.unibas.ch") or NODE.endswith(".cluster.bc2.ch")
SCRIPT_DIR = os.environ["DOWNWARD_REPO"]
BENCHMARKS_DIR = os.environ["ROUTING_BENCHMARKS"]
# BHOSLIB_GRAPHS = sorted(glob.glob(os.path.join(BENCHMARKS_DIR, "bhoslib", "*.mis")))
# RANDOM_GRAPHS = sorted(glob.glob(os.path.join(BENCHMARKS_DIR, "random", "*.txt")))
# ALGORITHMS = ["2approx", "greedy"]
SEED = 2018
TIME_LIMIT = 1800
MEMORY_LIMIT = 3500
CONFIGURATION = "lama-first"
DIR = Path(__file__).resolve().parent

if REMOTE:
    ENV = BaselSlurmEnvironment(
        email="f.burch@unibas.ch",
        partition="infai_1",
        memory_per_cpu="3790M",
        cpus_per_task=4,
        )
    SUITE = ["classical_grounded_coords", "classical_lifted_coords", "classical_grounded_sequential", "classical_lifted_sequential"]
else:
    ENV = LocalEnvironment(processes=2)
    print("Not on cluster!")
    SUITE = []
ATTRIBUTES = [
    "total_time",
    "search_time",
    "plan_length",
    "plan_cost",
    "evaluations",
    "expanded_states",
    "registered_states",
    "score_total_time",
    "score_search_time"
]

# Create a new experiment.
exp = Experiment(environment=ENV)
# Add solver to experiment and make it available to all runs.
# exp.add_resource("solver", os.path.join(SCRIPT_DIR, "fast-downward.py"))
# Add custom parser.
# exp.add_parser(os.path.join(SCRIPT_DIR, "experiments/cg-vs-ff/parser.py"))
exp.add_parser(DIR / "parser.py")

for task in build_suite(BENCHMARKS_DIR, SUITE):
    run = exp.add_run()
    # Create a symbolic link and an alias. This is optional. We
    # could also use absolute paths in add_command().
    run.add_resource("domain", task.domain_file, symlink=True)
    run.add_resource("problem", task.problem_file, symlink=True)
    run.add_command(
        "solve",
        ["fast-downward.py", "--alias", CONFIGURATION, "{domain}", "{problem}"],
        time_limit=TIME_LIMIT,
        memory_limit=MEMORY_LIMIT,
    )
    # AbsoluteReport needs the following attributes:
    # 'domain', 'problem' and 'algorithm'.
    # domain = os.path.basename(os.path.dirname(task))
    # task_name = os.path.basename(task)
    run.set_property("domain", task.domain)
    run.set_property("problem", task.problem)
    run.set_property("algorithm", CONFIGURATION)
    # BaseReport needs the following properties:
    # 'time_limit', 'memory_limit', 'seed'.
    run.set_property("time_limit", TIME_LIMIT)
    run.set_property("memory_limit", MEMORY_LIMIT)
    # Every run has to have a unique id in the form of a list.
    run.set_property("id", [CONFIGURATION, task.domain, task.problem])

# Add step that writes experiment files to disk.
exp.add_step("build", exp.build)

# Add step that executes all runs.
exp.add_step("start", exp.start_runs)

# Add step that collects properties from run directories and
# writes them to *-eval/properties.
exp.add_fetcher(name="fetch")

def add_score(run):
    success = isinstance(run.get("plan_cost"), float)

    try:
        max_time = run["time_limit"]
    except KeyError:
        print("search time limit missing -> can't compute time scores")
    else:
        run["score_total_time"] = tools.compute_log_score(
            success, run.get("total_time"), lower_bound=1.0, upper_bound=max_time
        )
        run["score_search_time"] = tools.compute_log_score(
            success, run.get("search_time"), lower_bound=1.0, upper_bound=max_time
        )

# Make a report.
report = Report(attributes=ATTRIBUTES, filter=[add_score])
exp.add_report(report)

# Parse the commandline and run the given steps.
exp.run_steps()
