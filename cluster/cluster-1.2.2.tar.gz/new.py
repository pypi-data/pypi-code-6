from __future__ import print_function


def similarity(a, b, simfunc, linkage=min):
    return linkage([simfunc(x, y) for x in a for y in b])


def reconstruct(data, cluster_indices):
    return [[data[i] for i in _] for _ in cluster_indices]


def run(data):
    indices = [[_] for _ in range(len(data))]
    yield indices, None
    while len(indices) > 1:
        minimum = None
        min_pair = None
        permutations = ((a, b)
                        for i, a in enumerate(indices)
                        for b in indices[:i])
        for x, y in permutations:
            sim = similarity(lambda x, y: abs(x - y),
                             [data[_] for _ in x],
                             [data[_] for _ in y])
            if minimum is None or sim < minimum:
                minimum = sim
                min_pair = (x, y)
            if minimum == 0:
                break
        indices.append(min_pair[0] + min_pair[1])
        indices.remove(min_pair[0])
        indices.remove(min_pair[1])
        yield indices, minimum


def cluster(data, min_distance):
    current_level = None
    current_clusters = None
    for indices, level in run(data):
        if level >= min_distance:
            break
        current_level = level
        current_clusters = indices
    else:
        raise ValueError('whoops')

    return (reconstruct(data, current_clusters), current_level)
