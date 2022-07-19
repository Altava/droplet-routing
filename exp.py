from lab.environments import BaselSlurmEnvironment
import os

exp = FastDownwardExperiment()
exp.add_step("build", exp.build)
exp.add_step("start", exp.start_runs)
exp.add_fetcher(name="fetch")

from lab.environments import BaselSlurmEnvironment
env = BaselSlurmEnvironment(email="f.burch@unibas.ch")
exp = FastDownwardExperiment(environment=env)

exp.add_parser(exp.EXITCODE_PARSER)
exp.add_parser(exp.TRANSLATOR_PARSER)
exp.add_parser(exp.SINGLE_SEARCH_PARSER)
exp.add_parser(exp.PLANNER_PARSER)

exp = FastDownwardExperiment()
repo = os.environ["DOWNWARD_REPO"]
rev = "main"

exp.add_algorithm("lmcut", repo, rev, ["--search", "astar(lmcut())"])

dir = "~/droplet-routing/pddl/"
exp.add_suite(benchmarks_dir, ["depot", "gripper"])
exp.add_suite(benchmarks_dir, ["gripper:prob01.pddl"])
exp.add_suite(benchmarks_dir, ["rubiks-cube:p01.sas"])