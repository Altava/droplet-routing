import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd
import os
import re
import math

def compute_log_score(success, value, lower_bound, upper_bound):
    """Compute score between 0 and 1.
    Best possible performance (value <= lower_bound) counts as 1, while failed
    runs (!success) and worst performance (value >= upper_bound) counts as 0.
    """
    if value is None or not success:
        return 0.0
    value = max(value, lower_bound)
    value = min(value, upper_bound)
    raw_score = math.log(value) - math.log(upper_bound)
    best_raw_score = math.log(lower_bound) - math.log(upper_bound)
    return raw_score / best_raw_score

parentname = os.path.dirname(__file__)
dictionary_classical = open(os.path.join(parentname, 'properties_classical'), 'r')
dictionary_durative = open(os.path.join(parentname, 'properties_durative'), 'r')
data_classical = pd.read_json(dictionary_classical)
data_durative = pd.read_json(dictionary_durative)
raw_classical = data_classical.transpose()
raw_durative = data_durative.transpose()

raw_classical['size_x'] = raw_classical.apply(lambda row: re.search("^p(\d+)x*", row.problem).group(1), axis=1)
raw_classical['size_y'] = raw_classical.apply(lambda row: re.search("^p\d+x(\d+)*", row.problem).group(1), axis=1)
raw_classical['droplets'] = raw_classical.apply(lambda row: re.search("^p\d+x\d+d(\d+)*", row.problem).group(1), axis=1)
raw_classical['blockages'] = raw_classical.apply(lambda row: re.search("^p\d+x\d+d\d+b(\d+)*", row.problem).group(1), axis=1)
raw_classical['problem_type'] = raw_classical.apply(lambda row: re.search("^(p\d+x\d+d\d+b\d+)*", row.problem).group(1), axis=1)
raw_classical['score_search_time'] = raw_classical.apply(lambda row: compute_log_score(not math.isnan(row.search_time), row.search_time, 1.0, row.time_limit), axis=1)
raw_classical['score_total_time'] = raw_classical.apply(lambda row: compute_log_score(not math.isnan(row.total_time), row.total_time, 1.0, row.time_limit), axis=1)
raw_classical['search_score_per_plan_length'] = raw_classical.apply(lambda row: row.score_search_time / row.plan_length, axis=1)
# print(raw_classical.blockages)

raw_durative['size_x'] = raw_durative.apply(lambda row: re.search("^p(\d+)x*", row.problem).group(1), axis=1)
raw_durative['size_y'] = raw_durative.apply(lambda row: re.search("^p\d+x(\d+)*", row.problem).group(1), axis=1)
raw_durative['droplets'] = raw_durative.apply(lambda row: re.search("^p\d+x\d+d(\d+)*", row.problem).group(1), axis=1)
raw_durative['blockages'] = raw_durative.apply(lambda row: re.search("^p\d+x\d+d\d+b(\d+)*", row.problem).group(1), axis=1)
raw_durative['problem_type'] = raw_durative.apply(lambda row: re.search("^(p\d+x\d+d\d+b\d+)*", row.problem).group(1), axis=1)
raw_durative['score_search_time'] = raw_durative.apply(lambda row: compute_log_score(not math.isnan(row.search_time), row.search_time, 1.0, row.time_limit), axis=1)
raw_durative['score_total_time'] = raw_durative.apply(lambda row: compute_log_score(not math.isnan(row.total_time), row.total_time, 1.0, row.time_limit), axis=1)
raw_durative['search_score_per_plan_length'] = raw_durative.apply(lambda row: row.score_search_time / row.plan_length, axis=1)
# print(raw_durative.size_x)

aggregations = {'score_search_time': 'mean', 'score_total_time': 'mean', 'plan_cost': 'mean', 'plan_length': 'mean', 'search_score_per_plan_length': 'mean', 'expanded_states': 'mean', 'size_x': 'first', 'droplets': 'first', 'blockages': 'first'}

raw_classical.droplets = pd.to_numeric(raw_classical.droplets)
raw_classical.size_x = pd.to_numeric(raw_classical.size_x)
raw_classical.blockages = pd.to_numeric(raw_classical.blockages)
agg_classical = raw_classical.groupby([raw_classical.domain, raw_classical.problem_type]).aggregate(aggregations)
# print(agg_classical)

agg_durative = raw_durative.groupby([raw_durative.domain, raw_durative.problem_type]).aggregate(aggregations)
agg_durative['droplets'] = agg_durative['droplets'].astype('int')
agg_durative['size_x'] = agg_durative['size_x'].astype('int')
agg_durative['blockages'] = agg_durative['blockages'].astype('int')

drop_classical = agg_classical.sort_values('droplets')
drop_classical = drop_classical.query('size_x == 9 and blockages == 3')
drop_durative = agg_durative.sort_values('droplets')
drop_durative = drop_durative.query('size_x == 9 and blockages == 3')
# print(drop_classical)

size_classical = agg_classical.sort_values('size_x')
size_classical = size_classical.query('droplets == 7 and blockages == 3')
size_durative = agg_durative.sort_values('size_x')
size_durative = size_durative.query('droplets == 7 and blockages == 3')
# print(size_classical)

bloc_classical = agg_classical.sort_values('blockages')
bloc_classical = bloc_classical.query('droplets == 7 and size_x == 15 and blockages >= 3')
bloc_durative = agg_durative.sort_values('blockages')
bloc_durative = bloc_durative.query('droplets == 7 and size_x == 15 and blockages >= 3')

drop = [drop_classical, drop_durative]
size = [size_classical, size_durative]
bloc = [bloc_classical, bloc_durative]

# clc = data.filter(regex='^lama-first-classical_lifted_coords', axis=1)
# # print(clc)

# print(cgc['droplets'])

# xAxis = [cgc['evaluations']]
# yAxis = [cgc['search_time']]
# plt.grid(True)

plot_classical = True
plot_durative = False
plots = [["droplets", "score_search_time", drop], ["size_x", "score_search_time", size], ["blockages", "score_search_time", bloc], 
        ["droplets", "plan_length", drop], ["size_x", "plan_length", size], ["blockages", "plan_length", bloc], 
        ["droplets", "search_score_per_plan_length", drop], ["size_x", "search_score_per_plan_length", size], ["blockages", "search_score_per_plan_length", bloc]]
fig, axes = plt.subplots(int(len(plots) / 3), 3)
i_p = 0

for p in plots:
    ax = axes[int(i_p / 3), i_p % 3]
    if plot_classical:
        p[2][0].query('domain == "classical_lifted_coords"').plot(x=p[0], y=p[1], label="Classical Lifted Coords", ax=ax, legend=0)
        p[2][0].query('domain == "classical_lifted_sequential"').plot(x=p[0], y=p[1], label="Classical Lifted Sequential", ax=ax, legend=0)
        p[2][0].query('domain == "classical_grounded_coords"').plot(x=p[0], y=p[1], label="Classical Grounded Coords", ax=ax, legend=0)
        p[2][0].query('domain == "classical_grounded_sequential"').plot(x=p[0], y=p[1], label="Classical Grounded Sequential", ax=ax, legend=0)
    if plot_durative:
        p[2][1].query('domain == "durative_lifted_coords"').plot(x=p[0], y=p[1], label="Durative Lifted Coords", ax=ax, legend=0)
        p[2][1].query('domain == "durative_lifted_sequential"').plot(x=p[0], y=p[1], label="Durative Lifted Sequential", ax=ax, legend=0)
        p[2][1].query('domain == "durative_grounded_coords"').plot(x=p[0], y=p[1], label="Durative Grounded Coords", ax=ax, legend=0)
        p[2][1].query('domain == "durative_grounded_sequential"').plot(x=p[0], y=p[1], label="Durative Grounded Sequential", ax=ax, legend=0)
    ax.set_xlabel(p[0])
    ax.set_ylabel(p[1])
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    handles, labels = ax.get_legend_handles_labels()
    fig.subplots_adjust(bottom=0.17)
    fig.legend(handles, labels, loc='lower right')
    i_p += 1

# Graph for different sizes
# ax_s = size_classical.query('domain == "classical_lifted_coords"').plot(x="size_x", y="score_search_time", label="Classical Lifted Coords")
# size_classical.query('domain == "classical_lifted_sequential"').plot(x="size_x", y="score_search_time", label="Classical Lifted Sequential", ax=ax_s)
# size_classical.query('domain == "classical_grounded_coords"').plot(x="size_x", y="score_search_time", label="Classical Grounded Coords", ax=ax_s)
# size_classical.query('domain == "classical_grounded_sequential"').plot(x="size_x", y="score_search_time", label="Classical Grounded Sequential", ax=ax_s)
# size_durative.query('domain == "durative_lifted_coords"').plot(x="size_x", y="score_search_time", label="Durative Lifted Coords", ax=ax_s)
# size_durative.query('domain == "durative_lifted_sequential"').plot(x="size_x", y="score_search_time", label="Durative Lifted Sequential", ax=ax_s)
# size_durative.query('domain == "durative_grounded_coords"').plot(x="size_x", y="score_search_time", label="Durative Grounded Coords", ax=ax_s)
# size_durative.query('domain == "durative_grounded_sequential"').plot(x="size_x", y="score_search_time", label="Durative Grounded Sequential", ax=ax_s)
# ax_s.set_xlabel("size of the chip")
# ax_s.set_ylabel("mean search time score")


# ax_scatter = agg_classical.query('domain == "classical_lifted_sequential"').plot.scatter(x="droplets", y="size_x")

# plt.plot(xAxis,yAxis, color='maroon', marker='o')

plt.show()