import matplotlib.pyplot as plt
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
dictionary = open(os.path.join(parentname, 'properties'), 'r')
data = pd.read_json(dictionary)
raw = data.transpose()
print(type(raw.iloc[2][2]))
raw['size_x'] = raw.apply(lambda row: re.search("^p(\d+)x*", row.problem).group(1), axis=1)
raw['size_y'] = raw.apply(lambda row: re.search("^p\d+x(\d+)*", row.problem).group(1), axis=1)
raw['droplets'] = raw.apply(lambda row: re.search("^p\d+x\d+d(\d+)*", row.problem).group(1), axis=1)
raw['problem_type'] = raw.apply(lambda row: re.search("^(p\d+x\d+d\d+)*", row.problem).group(1), axis=1)
raw['score_search_time'] = raw.apply(lambda row: compute_log_score(not math.isnan(row.search_time), row.search_time, 1.0, row.time_limit), axis=1)
raw['score_total_time'] = raw.apply(lambda row: compute_log_score(not math.isnan(row.total_time), row.total_time, 1.0, row.time_limit), axis=1)
print(raw)
aggregations = {'score_search_time': 'mean', 'score_total_time': 'mean', 'plan_cost': 'mean', 'expanded_states': 'mean', 'size_x': 'first', 'droplets': 'first'}
agg = raw.groupby([raw.domain, raw.problem_type]).aggregate(aggregations)
agg.droplets = pd.to_numeric(agg.droplets)
agg.size_x = pd.to_numeric(agg.size_x)

drop = agg.sort_values('droplets')
drop = drop.query('size_x == 16')

size = agg.sort_values('size_x')
size = size.query('droplets == 7')
print(size)

# clc = data.filter(regex='^lama-first-classical_lifted_coords', axis=1)
# # print(clc)

# print(cgc['droplets'])

# xAxis = [cgc['evaluations']]
# yAxis = [cgc['search_time']]
# plt.grid(True)

# Graph for different number of droplets
ax_d = drop.query('domain == "classical_lifted_coords"').plot(x="droplets", y="score_search_time", label="Classical Lifted Coords")
drop.query('domain == "classical_lifted_sequential"').plot(x="droplets", y="score_search_time", label="Classical Lifted Sequential", ax=ax_d)
drop.query('domain == "classical_grounded_coords"').plot(x="droplets", y="score_search_time", label="Classical Grounded Coords", ax=ax_d)
drop.query('domain == "classical_grounded_sequential"').plot(x="droplets", y="score_search_time", label="Classical Grounded Sequential", ax=ax_d)
ax_d.set_xlabel("# of droplets")
ax_d.set_ylabel("mean search time score")

# Graph for different sizes
ax_s = size.query('domain == "classical_lifted_coords"').plot(x="size_x", y="score_search_time", label="Classical Lifted Coords")
size.query('domain == "classical_lifted_sequential"').plot(x="size_x", y="score_search_time", label="Classical Lifted Sequential", ax=ax_s)
size.query('domain == "classical_grounded_coords"').plot(x="size_x", y="score_search_time", label="Classical Grounded Coords", ax=ax_s)
size.query('domain == "classical_grounded_sequential"').plot(x="size_x", y="score_search_time", label="Classical Grounded Sequential", ax=ax_s)
ax_s.set_xlabel("size of the chip")
ax_s.set_ylabel("mean search time score")


ax_scatter = agg.query('domain == "classical_lifted_sequential"').plot.scatter(x="droplets", y="size_x")

# plt.plot(xAxis,yAxis, color='maroon', marker='o')

plt.show()