from cluster import HierarchicalClustering
import sys
from new import run, cluster


def load(n):
    data = []
    with open('data.txt') as fp:
        for i, line in enumerate(fp):
            if i == n:
                break
            data.append(int(line))
    return data


if __name__ == "__main__":
    data = load(int(sys.argv[1]))
    data = [791, 956, 676, 124, 564, 84, 24, 365, 594, 940, 398,
            971, 131, 365, 542, 336, 518, 835, 134, 391]
    cl, level = cluster(data, min_distance=40)
    for row in cl:
        print(row)
    sys.exit(0)
    if sys.argv[2] == 'old':
        cl = HierarchicalClustering(data, lambda x, y: abs(x-y))
        result = cl.getlevel(20)
        for row in result:
            print(row)
        print(len(result))
    else:
        result = run(data)
        last_cluster, last_level = [], None
        for clusters, level in result:
            print(level, len(clusters))
            if level > 20:
                break
            last_cluster = clusters
            last_level = level
        for row in last_cluster:
            print(row)
        print(len(last_cluster), last_level)




