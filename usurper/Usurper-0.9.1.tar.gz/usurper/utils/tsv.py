#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import re

import networkx

from usurper import pos


def sentences_iter(corpus, return_id=False):
    """Iterate over the sentences in a corpus.
    
    Args:
        corpus:

    """
    pattern = re.compile(r"^\S+")
    sentence = []
    sid = 0
    for line in corpus:
        line = line.rstrip("\n")
        if line == "":
            if len(sentence) > 0:
                sid += 1
                if return_id:
                    yield sentence, sid
                else:
                    yield sentence
            sentence = []
        else:
            m = re.search(pattern, line)
            if m:
                sentence.append(line.split("\t"))
            else:
                raise Exception("Line does not match: %s" % line)
    # in case the file does not end in an empty line
    if len(sentence) > 0:
        sid += 1
        if return_id:
            yield sentence, sid
        else:
            yield sentence


def create_nx_digraph_from_tsv(tsv, tagset, origid=None):
    """Return a networkx.DiGraph object of the TSV representation.
    
    Args:
        tsv:
        origid:

    """
    dg = networkx.DiGraph()
    attributes = lambda l: {"form": l[0], "lower": l[0].lower()}
    if len(tsv[0]) > 1:
        attributes = lambda l: {"form": l[0], "lower": l[0].lower(), "pos": l[1]}
        if tagset is not None:
            mapping = pos.get_pos_map(tagset)
            attributes = lambda l: {"form": l[0], "lower": l[0].lower(), "pos": l[1], "upos": mapping[l[1]]}
    if origid is not None:
        dg.graph["origid"] = origid
    dg.add_nodes_from([(i + 1, attributes(l)) for i, l in enumerate(tsv)])
    return dg
