from __future__ import division


def compare_objects(left, right):
    """
    Compare two objects and return a dict describing the differences.
    Only json-like objects are supported at the moment.
    """

    # The objects are equal: we don't care about the contents
    if left == right:
        return {'distance': 0.0, 'left': left, 'right': right}

    if _are_both(left, right, dict):
        return _compare_dicts(left, right)

    if _are_both(left, right, (list, tuple)):
        return _compare_sequences(left, right)

    # The objects are completely different
    return {'distance': 1.0, 'left': left, 'right': right}


def _are_both(left, right, types):
    return isinstance(left, types) and isinstance(right, types)


def _compare_dicts(left, right):
    left_only = []
    right_only = []
    differences = {}
    equal = []

    all_keys = set(left.keys()).union(set(right.keys()))
    for key in all_keys:
        if key not in left:
            right_only.append(key)
        elif key not in right:
            left_only.append(key)
        else:
            diff = compare_objects(left[key], right[key])
            if diff['distance'] == 0:
                equal.append(key)
            else:
                differences[key] = diff

    total = len(all_keys)
    diff_count = len(differences) + len(left_only) + len(right_only)
    return {
        'distance': (diff_count / total) if total != 0 else 0,
        'removed': left_only,
        'added': right_only,
        'changed': differences.keys(),
        'equal': equal,
        'changes': differences,
        'total': len(all_keys),
    }


def _compare_sequences(left, right):
    """
    To compare two sequences:

    - Create comparison "pairs": (distance, left_id, right_id, diff)
    - Start taking pairs from the top if they both contain items
      for the first time
    """

    all_pairs = []
    for lid, litem in enumerate(left):
        for rid, ritem in enumerate(right):
            diff = compare_objects(litem, ritem)
            all_pairs.append((diff['distance'], lid, rid, diff))
    all_pairs.sort(key=lambda x: x[0])

    unproc_left = set(xrange(len(left)))
    unproc_right = set(xrange(len(right)))

    # Take only pairs containing unused items
    filtered_pairs = []
    for dist, lid, rid, diff in all_pairs:
        if (lid in unproc_left) and (rid in unproc_right):
            unproc_left.remove(lid)
            unproc_right.remove(rid)
            filtered_pairs.append((dist, lid, rid, diff))

    assert len(filtered_pairs) == min(len(left), len(right))

    # Take items left in "unproc" sets as items that have been
    # removed.
    left_only = list(unproc_left)
    right_only = list(unproc_right)

    # Extract differences (items changed or moved)
    differences = {}
    equal = []
    for (dist, lid, rid, diff) in filtered_pairs:
        if dist == 0 and (lid == rid):
            # Same thing in the same place
            equal.append(lid)

        elif dist < 1.0:
            # Something changed, but the item was the same
            differences[lid] = {
                'pos': rid,
                'distance': dist,
                'diff': diff}

        else:
            left_only.append(lid)
            right_only.append(rid)

    diff_count = len(left_only) + len(right_only) + len(differences)
    assert diff_count == len(left_only) + len(right_only) + len(differences)

    total = diff_count + len(equal)
    distance = (diff_count / total) if total != 0 else 0

    return {
        'distance': distance,
        'added': right_only,
        'removed': left_only,
        'changed': differences.keys(),
        'equal': equal,
        'changes': differences,
        'total': total,
    }
