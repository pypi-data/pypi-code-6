# for pybedtools issue #99

import pybedtools

# make a demo list of chrom:start-stop strings from example data shipped with
# pybedtools
n_intervals = 20000
loc_list = []
for i, feature in enumerate(pybedtools.example_bedtool('x.bed')):
    if i >= n_intervals:
        break
    loc_list.append('{0.chrom}:{0.start}-{0.stop}'.format(feature))


def make_intervals(loc_list):
    for data in loc_list:
        seqid = data.split(':')[0]
        loc_str = data.split(':')[1]
        start = str(int(loc_str.split('-')[0]) - 1)
        stop = loc_str.split('-')[1]
        yield pybedtools.create_interval_from_list([seqid, start, stop])


def mergeBed(bed):
    sorted_bed = bed.sort()
    bed_merge = sorted_bed.merge()
    tot_len = 0
    for feature in bed_merge:
        feat_len = feature.stop - feature.start
        tot_len += feat_len
    pybedtools.helpers.close_or_delete(sorted_bed)
    pybedtools.helpers.close_or_delete(bed_merge)
    return tot_len

# split the n_intervals into this many separate groups to simulate many
# separate transcripts
n_groups = 500
n_per_group = n_intervals / n_groups
group_num = 0
for start_ind in range(0, n_intervals, n_per_group):
    end_ind = start_ind + n_per_group
    locs_subset = loc_list[start_ind:end_ind]
    x = pybedtools.BedTool(make_intervals(locs_subset))
    print 'group %s: %s' % (group_num, mergeBed(x))
    pybedtools.helpers.close_or_delete(x)
    group_num += 1

