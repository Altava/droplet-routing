#! /usr/bin/env python
# import glob
import os
import platform

from pathlib import Path
from downward.reports.absolute import AbsoluteReport
from downward.suites import build_suite
from lab.environments import BaselSlurmEnvironment, LocalEnvironment
from lab.experiment import Experiment
from lab.reports import Attribute


# Create custom report class with suitable info and error attributes.
class BaseReport(AbsoluteReport):
    INFO_ATTRIBUTES = ["time_limit", "memory_limit", "seed"]
    ERROR_ATTRIBUTES = [
        "domain",
        "problem",
        "algorithm",
        "unexplained_errors",
        "error",
        "node",
    ]


NODE = platform.node()
REMOTE = NODE.endswith(".scicore.unibas.ch") or NODE.endswith(".cluster.bc2.ch")
SCRIPT_DIR = os.environ["TFD_REPO"]
BENCHMARKS_DIR = os.environ["ROUTING_BENCHMARKS"]
# BHOSLIB_GRAPHS = sorted(glob.glob(os.path.join(BENCHMARKS_DIR, "bhoslib", "*.mis")))
# RANDOM_GRAPHS = sorted(glob.glob(os.path.join(BENCHMARKS_DIR, "random", "*.txt")))
# ALGORITHMS = ["2approx", "greedy"]
SEED = 2018
TIME_LIMIT = 1800
MEMORY_LIMIT = 2048
DIR = Path(__file__).resolve().parent

if REMOTE:
    ENV = BaselSlurmEnvironment(
        email="f.burch@unibas.ch",
        partition="infai_1",
        memory_per_cpu="3790M",
        cpus_per_task=4,
        )
    # SUITE = ["durative_grounded_coords", "durative_lifted_coords", "durative_grounded_sequential", "durative_lifted_sequential"]
    SUITE = ["durative_grounded_coords:p9x9d5n001.pddl"]
else:
    ENV = LocalEnvironment(processes=2)
    # Use smaller suite for local tests.
    # SUITE = BHOSLIB_GRAPHS[:1] + RANDOM_GRAPHS[:1]
ATTRIBUTES = [
    # "cover",
    # "cover_size",
    "error",
    "run_dir",
    "total_time",
    "solver_exit_code",
    "expansions",
    "memory",
    Attribute("solved", absolute=True),
]

# Create a new experiment.
exp = Experiment(environment=ENV)
# Add solver to experiment and make it available to all runs.
# exp.add_resource("solver", os.path.join(SCRIPT_DIR, "fast-downward.py"))
# Add custom parser.
# exp.add_parser(os.path.join(SCRIPT_DIR, "experiments/cg-vs-ff/parser.py"))
exp.add_parser(DIR / "parser.py")

exp.add_resource("run_singularity", DIR / "run-singularity.sh")

for task in build_suite(BENCHMARKS_DIR, SUITE):
    run = exp.add_run()
    # Create a symbolic link and an alias. This is optional. We
    # could also use absolute paths in add_command().
    run.add_resource("domain", task.domain_file, symlink=True)
    run.add_resource("problem", task.problem_file, symlink=True)
    run.add_command(
            "run-planner",
            [
                "runsolver",
                "-C",
                TIME_LIMIT,
                "-V",
                MEMORY_LIMIT,
                "-w",
                "watch.log",
                "-v",
                "values.log",
                "{run_singularity}",
                "/infai/burfab04/bin/tfd.sif",
                "{domain}",
                "{problem}",
                "sas_plan",
            ],
        )
    # AbsoluteReport needs the following attributes:
    # 'domain', 'problem' and 'algorithm'.
    # domain = os.path.basename(os.path.dirname(task))
    # task_name = os.path.basename(task)
    run.set_property("domain", task.domain)
    run.set_property("problem", task.problem)
    run.set_property("algorithm", "lama-first")
    # BaseReport needs the following properties:
    # 'time_limit', 'memory_limit', 'seed'.
    run.set_property("time_limit", TIME_LIMIT)
    run.set_property("memory_limit", MEMORY_LIMIT)
    # Every run has to have a unique id in the form of a list.
    run.set_property("id", ["lama-first", task.domain, task.problem])

# Add step that writes experiment files to disk.
exp.add_step("build", exp.build)

# Add step that executes all runs.
exp.add_step("start", exp.start_runs)

# Add step that collects properties from run directories and
# writes them to *-eval/properties.
exp.add_fetcher(name="fetch")

# Make a report.
exp.add_report(BaseReport(attributes=ATTRIBUTES), outfile="report.html")

# Parse the commandline and run the given steps.
exp.run_steps()
