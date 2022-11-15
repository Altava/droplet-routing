from math import nan
import matplotlib.pyplot as plt
import pandas as pd
import os
import re
import math
import seaborn as sb

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

def compute_log_scores(success, values, lower_bound, upper_bound):
    """Compute score between 0 and 1.
    Best possible performance (value <= lower_bound) counts as 1, while failed
    runs (!success) and worst performance (value >= upper_bound) counts as 0.
    """    
    scores = []
    for value in values:
        if value is None or not success:
            scores.append(0.0)
        value = max(value, lower_bound)
        value = min(value, upper_bound)
        raw_score = math.log(value) - math.log(upper_bound)
        best_raw_score = math.log(lower_bound) - math.log(upper_bound)
        scores.append(raw_score / best_raw_score)
    return scores

def name(ext, mixture):
    return ext + " M%i" % mixture
    

# function to parse files using the BioGram grammar
def parseFile(file):
    f = open(file, "r")
    content = f.read()
    
    # search for "nets", parse into list of coordinates
    min_plan_length = 0
    netsearch = re.search("(?s)nets(.*)end", content)
    nets = list(filter(None, netsearch.group(1).split("end")[0].split("\n")))
    for net in nets:
        pos = re.search("\d+ \((\d+),(\d+)\) -> \((\d+),(\d+)\)", net).group(1, 2, 3, 4)
        min_plan_length += abs(int(pos[0]) - int(pos[2]))
        min_plan_length += abs(int(pos[1]) - int(pos[3]))

    # print("current min_plan_length:", min_plan_length)
    
    return min_plan_length

def getFirst(list):
    return [item[0] for item in list]

parentname = os.path.dirname(__file__)
dictionary_classical = open(os.path.join(parentname, 'properties_classical'), 'r')
dictionary_durative = open(os.path.join(parentname, 'properties_durative'), 'r')
dictionary_classical_anytime = open(os.path.join(parentname, 'properties_classical_anytime'), 'r')
dictionary_durative_anytime = open(os.path.join(parentname, 'properties_durative_anytime'), 'r')
data_classical = pd.read_json(dictionary_classical)
data_durative = pd.read_json(dictionary_durative)
data_classical_anytime = pd.read_json(dictionary_classical_anytime)
data_durative_anytime = pd.read_json(dictionary_durative_anytime)
raw_classical = data_classical.transpose()
raw_durative = data_durative.transpose()
raw_classical_anytime = data_classical_anytime.transpose()
raw_durative_anytime = data_durative_anytime.transpose()
# print(raw_classical_anytime)
# print(raw_durative_anytime)
# raw_classical_anytime['plans'] = raw_classical_anytime.apply(lambda row: len(row.plan_length_over_time), axis=1)
# raw_classical_anytime = raw_classical_anytime.drop(raw_classical_anytime[raw_classical_anytime.plans > 0].index)
# print(raw_classical_anytime)
# print(raw_durative_anytime)
# raw_durative_anytime['plans'] = raw_durative_anytime.apply(lambda row: len(row.plan_length_over_time), axis=1)
# raw_durative_anytime = raw_durative_anytime.drop(raw_durative_anytime[raw_durative_anytime.plans > 0].index)
# print(raw_durative_anytime)

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

# -----V----V-----V-- Plots for Extensions --V----V----V---- #

dictionary_extensions = open(os.path.join(parentname, 'properties_extensions'), 'r')
data_extensions = pd.read_json(dictionary_extensions)
raw_extensions = data_extensions.transpose()
raw_extensions['mixture'] = raw_extensions.apply(lambda row: re.search("^p(\d)*", row.problem).group(1), axis=1)
raw_extensions['extension'] = raw_extensions.apply(lambda row: re.search("^p\d(\D+).pddl", row.problem).group(1), axis=1)
bestPlan = [18, 0, 17, 13, 40, 12, 13, 40, 12, 14, 43, 7, 34, 128, 23, 32, 0, 18, 0, 0, 39]
raw_extensions['best_plan'] = bestPlan
# print(raw_extensions)
raw_extensions['scores_plan_length'] = raw_extensions.apply(lambda row: compute_log_scores(row.plan_length_over_time, row.plan_length_over_time, row.best_plan, 10 * row.best_plan), axis=1)
raw_extensions.mixture = pd.to_numeric(raw_extensions.mixture)
# print(raw_extensions)
raw_extensions = raw_extensions.sort_values('extension', kind="stable")
tier1 = raw_extensions.query('mixture < 5')
tier2 = raw_extensions.query('mixture < 7 & mixture > 4')
tier3 = raw_extensions.query('mixture == 7')
print(raw_extensions.scores_plan_length)
print(tier1)
print(tier2)
print(tier3)
merge_only_colors = sb.color_palette("BuGn", 10)
merge_mixer_colors = sb.color_palette("OrRd", 10)
merge_no_module_colors = sb.color_palette("BuPu", 10)
for index, row in raw_extensions.iterrows():
    if "only" in row.problem:
        color = merge_only_colors[row.mixture + 2]
    if "mixer" in row.problem:
        color = merge_mixer_colors[row.mixture + 2]
    if "module" in row.problem:
        color = merge_no_module_colors[row.mixture + 2]
    times = getFirst(row['times_over_time'])
    plan_length = row['scores_plan_length']
    if len(times) > len(plan_length):
        times = times[0:len(plan_length)]
    if times:
        plt.plot(times, plan_length, marker="o", label=name(row['extension'], row['mixture']), color=color)
    if len(row.scores_plan_length) > 0:
        print(row.scores_plan_length[-1])

plt.legend(loc='lower left')
plt.title("Plan length scores over time")
plt.xscale('log')
plt.xlabel('time in seconds')
plt.ylabel('plan length score')
plt.show()

# -----V----V-----V-- Survival Plots for Anytime Search --V----V----V---- #

# raw_classical_anytime['min_plan_length'] = raw_classical_anytime.apply(lambda row: 0, axis=1)
# raw_durative_anytime['min_plan_length'] = raw_durative_anytime.apply(lambda row: 0, axis=1)
# min_solutions = []

# dir = "/home/altava/droplet-routing/benchmarks"
# for dirpath, dirs, files in os.walk(dir):
#     print(dirpath)
#     for fl in files:
#         if re.search("^\d+.bio", fl):
#             min_plan_length = parseFile(os.path.join(dirpath, fl))
#             problemname = dirpath.split("/")[-1] + "n" + fl
#             problemname = problemname.replace("bm", "p")
#             problemname = problemname.replace("bio", "pddl")
#             raw_classical_anytime.loc[raw_classical_anytime['problem'] == problemname, ['min_plan_length']] = min_plan_length
#             raw_durative_anytime.loc[raw_durative_anytime['problem'] == problemname, ['min_plan_length']] = min_plan_length

# cgca = raw_classical_anytime.query('domain == "classical_grounded_coords"')
# cgsa = raw_classical_anytime.query('domain == "classical_grounded_sequential"')
# clca = raw_classical_anytime.query('domain == "classical_lifted_coords"')
# clsa = raw_classical_anytime.query('domain == "classical_lifted_sequential"')
# dgca = raw_durative_anytime.query('domain == "durative_grounded_coords"')
# dgsa = raw_durative_anytime.query('domain == "durative_grounded_sequential"')
# dlca = raw_durative_anytime.query('domain == "durative_lifted_coords"')
# dlsa = raw_durative_anytime.query('domain == "durative_lifted_sequential"')
# configurations = [cgca, cgsa, clca, clsa, dgca, dgsa, dlca, dlsa]
# for cfg in configurations:
#     scores = []
#     for index, row in cfg.iterrows():
#         i = 0
#         for t in row['times_over_time']:
#             if len(row['plan_length_over_time']) <= i:
#                 i = len(row['plan_length_over_time']) - 1
#             plan_length = row['plan_length_over_time'][i]
#             if isinstance(t, list):
#                 t = t[0]
#             score = compute_log_score(not math.isnan(t), plan_length, row['min_plan_length'], row['min_plan_length'] * 4)
#             scores.append((t, score))
#             i += 1

#     scores.sort(key=lambda x: x[0])
#     timesteps = []
#     average_score = []
#     to_average = []
#     for j in range(-25, 50):
#         timesteps.append(math.exp(j/10.0))
#         if scores:
#             while(scores[0][0] <= math.exp(j/10.0)):
#                 to_average.append(scores.pop(0)[1])
#                 if not scores:
#                     break
#         if len(to_average) == 0:
#             average_score.append(nan)
#         else:
#             average_score.append(sum(to_average) / len(to_average))

#     plt.plot(timesteps, average_score, label=cfg.iloc[0]['domain'])
# plt.legend(loc='lower left')
# plt.title("Accumulated Average Plan Length Score")
# plt.xscale('log')
# plt.xlabel('time in seconds')
# plt.ylabel('plan length score')
# plt.show()
            
# -----V----V-----V-- Survival Plots --V----V----V---- #

# problem_types = ["p15x15d7b3", "p15x15d7b6", "p9x9d5b3", "p9x9d9b3"]
# fig, ax = plt.subplots(2, 2)
# for i in range(0,4):
#     p15_c = raw_classical.query('problem_type == "%s"' % problem_types[i])
#     p15_d = raw_durative.query('problem_type == "%s"' % problem_types[i])
#     p15_cgc = p15_c.query('domain == "classical_grounded_coords"')
#     p15_cgs = p15_c.query('domain == "classical_grounded_sequential"')
#     p15_clc = p15_c.query('domain == "classical_lifted_coords"')
#     p15_cls = p15_c.query('domain == "classical_lifted_sequential"')
#     p15_dgc = p15_d.query('domain == "durative_grounded_coords"')
#     p15_dgs = p15_d.query('domain == "durative_grounded_sequential"')
#     p15_dlc = p15_d.query('domain == "durative_lifted_coords"')
#     p15_dls = p15_d.query('domain == "durative_lifted_sequential"')
#     timesteps = []
#     cgc = []
#     cgs = []
#     clc = []
#     cls = []
#     dgc = []
#     dgs = []
#     dlc = []
#     dls = []
#     for j in range(-25, 50):
#         timesteps.append(math.exp(j/10.0))
#         cgc.append((len(p15_cgc[p15_cgc['search_time'] < math.exp(j/10.0)]))/len(p15_cgc))
#         cgs.append((len(p15_cgs[p15_cgs['search_time'] < math.exp(j/10.0)]))/len(p15_cgs))
#         clc.append((len(p15_clc[p15_clc['search_time'] < math.exp(j/10.0)]))/len(p15_clc))
#         cls.append((len(p15_cls[p15_cls['search_time'] < math.exp(j/10.0)]))/len(p15_cls))
#         dgc.append((len(p15_dgc[p15_dgc['search_time'] < math.exp(j/10.0)]))/len(p15_dgc))
#         dgs.append((len(p15_dgs[p15_dgs['search_time'] < math.exp(j/10.0)]))/len(p15_dgs))
#         dlc.append((len(p15_dlc[p15_dlc['search_time'] < math.exp(j/10.0)]))/len(p15_dlc))
#         dls.append((len(p15_dls[p15_dls['search_time'] < math.exp(j/10.0)]))/len(p15_dls))


#     ax[int(i/2), i%2].plot(timesteps, cgc, label='classical grounded coordinates')
#     ax[int(i/2), i%2].plot(timesteps, cgs, label='classical grounded sequential')
#     ax[int(i/2), i%2].plot(timesteps, clc, label='classical lifted coordinates')
#     ax[int(i/2), i%2].plot(timesteps, cls, label='classical lifted sequential')
#     ax[int(i/2), i%2].plot(timesteps, dgc, label='durative grounded coordinates')
#     ax[int(i/2), i%2].plot(timesteps, dgs, label='durative grounded sequential')
#     ax[int(i/2), i%2].plot(timesteps, dlc, label='durative lifted coordinates')
#     ax[int(i/2), i%2].plot(timesteps, dls, label='durative lifted sequential')
#     ax[int(i/2), i%2].set_title(problem_types[i])
#     # ax[int(i/2), i%2].xscale('log')
# for a in ax.flat:
#     a.set_xscale('log')
#     a.set(xlabel='time in seconds')
#     a.set(ylabel='percentage of instances that found a solution')
#     a.label_outer()
# ax[1, 0].legend(loc='lower right')
# plt.show()

# ----V----V----V-- Basic Blots --V----V----V---- #

# clc = data.filter(regex='^lama-first-classical_lifted_coords', axis=1)
# # print(clc)

# print(cgc['droplets'])

# xAxis = [cgc['evaluations']]
# yAxis = [cgc['search_time']]
# plt.grid(True)

# plot_classical = True
# plot_durative = False
# plots = [["droplets", "score_search_time", drop], ["size_x", "score_search_time", size], ["blockages", "score_search_time", bloc], 
#         ["droplets", "plan_length", drop], ["size_x", "plan_length", size], ["blockages", "plan_length", bloc], 
#         ["droplets", "search_score_per_plan_length", drop], ["size_x", "search_score_per_plan_length", size], ["blockages", "search_score_per_plan_length", bloc]]
# fig, axes = plt.subplots(int(len(plots) / 3), 3)
# i_p = 0

# for p in plots:
#     ax = axes[int(i_p / 3), i_p % 3]
#     if plot_classical:
#         p[2][0].query('domain == "classical_lifted_coords"').plot(x=p[0], y=p[1], label="Classical Lifted Coords", ax=ax, legend=0)
#         p[2][0].query('domain == "classical_lifted_sequential"').plot(x=p[0], y=p[1], label="Classical Lifted Sequential", ax=ax, legend=0)
#         p[2][0].query('domain == "classical_grounded_coords"').plot(x=p[0], y=p[1], label="Classical Grounded Coords", ax=ax, legend=0)
#         p[2][0].query('domain == "classical_grounded_sequential"').plot(x=p[0], y=p[1], label="Classical Grounded Sequential", ax=ax, legend=0)
#     if plot_durative:
#         p[2][1].query('domain == "durative_lifted_coords"').plot(x=p[0], y=p[1], label="Durative Lifted Coords", ax=ax, legend=0)
#         p[2][1].query('domain == "durative_lifted_sequential"').plot(x=p[0], y=p[1], label="Durative Lifted Sequential", ax=ax, legend=0)
#         p[2][1].query('domain == "durative_grounded_coords"').plot(x=p[0], y=p[1], label="Durative Grounded Coords", ax=ax, legend=0)
#         p[2][1].query('domain == "durative_grounded_sequential"').plot(x=p[0], y=p[1], label="Durative Grounded Sequential", ax=ax, legend=0)
#     ax.set_xlabel(p[0])
#     ax.set_ylabel(p[1])
#     ax.xaxis.set_major_locator(MaxNLocator(integer=True))
#     handles, labels = ax.get_legend_handles_labels()
#     fig.subplots_adjust(bottom=0.17)
#     fig.legend(handles, labels, loc='lower right')
#     i_p += 1

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

# plt.show()