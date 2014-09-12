#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import re
import sys

import networkx

from usurper import pos


def sentences_iter(corpus, return_id=False):
    """Iterate over the sentences in a corpus.
    
    Args:
        corpus:

    """
    pattern = re.compile(r"^\d+\t")
    sentence = []
    sid = 0
    for line in corpus:
        if sys.version_info[:1] < (3,):
            line = line.decode("utf-8").rstrip("\n")
        else:
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


def create_nx_digraph_from_conll(conll, tagset, origid=None):
    """Return a networkx.DiGraph object of the CONLL representation,
    containing only the ID, FORM, CPOSTAG or POSTAG fields.
    
    Args:
        conll:
        origid:

    """
    dg = networkx.DiGraph()
    attributes = lambda l: {"form": l[1], "lower": l[1].lower(), "pos": l[pos_field]}    
    if tagset is not None:
        mapping = pos.get_pos_map(tagset)
        attributes = lambda l: {"form": l[1], "lower": l[1].lower(), "pos": l[pos_field], "upos": mapping[l[pos_field]]}
    if origid is not None:
        dg.graph["origid"] = origid
    pos_field = 4
    if conll[0][pos_field] == "_":
        pos_field = 3
    dg.add_nodes_from([(int(l[0]), attributes(l)) for l in conll])
    return dg


def export_to_conll_format(digraph):
    """Do actual formatting work.
    
    Args:
        digraph:

    """
    output = []
    for v in sorted(digraph.nodes()):
        if v == 0:
            continue
        word_id = v
        word = digraph.node[v]["form"]
        lemma = digraph.node[v].get("lemma", "_")
        cpostag = digraph.node[v].get("upos", "_")
        postag = digraph.node[v].get("pos", "_")
        feats = digraph.node[v].get("feats", "_")
        indeps = [(s, l["relation"]) for s, t, l in digraph.in_edges(v, data=True)]
        head, deprel = "_", "_"
        if len(indeps) == 1:
            head = indeps[0][0]
            deprel = indeps[0][1]
        else:
            logging.warning("Graph %s is not a tree: vertex %s has more than one incoming edge" % (digraph.graph["origid"], v))
        phead, pdeprel = "_", "_"
        output.append([str(word_id), word, lemma, cpostag, postag, feats, str(head), deprel, phead, pdeprel])
    return output
