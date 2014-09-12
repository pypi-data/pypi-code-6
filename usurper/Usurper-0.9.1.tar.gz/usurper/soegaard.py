#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import operator
import re

import networkx

from usurper.utils import tsv


def _add_edge(g, u, v):
    """Add edge to graph or increase edge weight."""
    if g.has_edge(u, v):
        g.edge[u][v]["weight"] += 1
    else:
        g.add_edge(u, v, {"weight": 1})
    return g


def _add_edges(s, function_words):
    """Create vertices and edges."""
    s_len = s.__len__()
    fw_set = set(["ADP", "CONJ", "DET", "PRON", "PRT"])
    for i in range(s_len):
        i += 1
        for j in range(s_len):
            j += 1
            if i == j:
                continue
            # short edges – edges between neighboring words
            if j == i - 1 or j == i + 1:
                s = _add_edge(s, i, j)
                # function words – edges from neighboring words to
                # function words
                # if "upos" in s.node[i]:
                #     if s.node[i]["upos"] in fw_set:
                #         s = _add_edge(s, j, i)
                # else:
                if s.node[i]["lower"] in function_words:
                    s = _add_edge(s, j, i)
            # morphological inequality – edges between words with
            # different pre- or suffixes
            if "upos" in s.node[i]:
                if s.node[i]["upos"] != s.node[j]["upos"] or s.node[i]["lower"][:2] != s.node[j]["lower"][:2] or s.node[i]["lower"][-3:] != s.node[j]["lower"][-3:]:
                    s = _add_edge(s, i, j)
            else:
                if s.node[i]["lower"][:2] != s.node[j]["lower"][:2] or s.node[i]["lower"][-3:] != s.node[j]["lower"][-3:]:
                    s = _add_edge(s, i, j)
            # verb edges
            if "upos" in s.node[i]:
                if s.node[i]["upos"] == "VERB":
                    s = _add_edge(s, j, i)
                    if s.node[j]["upos"] == "NOUN":
                        s = _add_edge(s, i, j)
    return s


def _rank_vertices(sid, digraph):
    """Rank vertices using PageRank."""
    pr = None
    try:
        pr = networkx.pagerank(digraph, alpha=1.0, tol=1e-05, weight="weight")
    except networkx.exception.NetworkXError:
        if sid is not None:
            logging.warning("PageRank did not converge on sentence %s" % sid)
        else:
            logging.warning("PageRank did not converge")
        pr = {v: -1.0 * v for v in digraph.nodes()}
    return pr


def _construct_parse_tree(s, pageranks, no_rules):
    """Construct dependency parse tree from PageRanks."""
    # potential governors
    # Paper:
    dep_rules = {"VERB": set(["VERB"]), "NOUN": set(["VERB", "NOUN", "ADP"]), "ADJ": set(["NOUN", "VERB"]), "ADV": set(["VERB", "ADP"]), "ADP": set(["VERB"]), "CONJ": set(["VERB"]), "DET": set(["NOUN", "VERB"]), "NUM": set(["NOUN", "VERB"])}
    # Paper + VERB -> PRON
    # dep_rules = {"VERB": set(["VERB"]), "NOUN": set(["VERB", "NOUN", "ADP"]), "ADJ": set(["NOUN", "VERB"]), "ADV": set(["VERB", "ADP"]), "ADP": set(["VERB"]), "CONJ": set(["VERB"]), "DET": set(["NOUN", "VERB"]), "NUM": set(["NOUN", "VERB"]), "PRON": set(["VERB"])}
    g = networkx.DiGraph()
    g.add_nodes_from(s.nodes(data=True))
    pr = sorted(pageranks.items(), key=operator.itemgetter(1), reverse=True)
    pr_dict = {v: r for v, r in pr}
    heads = set()
    # Most central verb as root, if possible
    if "upos" in g.node[pr[0][0]] and not no_rules:
        root_candidates = [v for v, r in pr if g.node[v]["upos"] == "VERB"]
        if len(root_candidates) > 0:
            root = root_candidates[0]
            g.add_edge(0, root, {"relation": "ROOT"})
            heads = set([root])
    for v, r in pr:
        if len(heads) == 0:
            g.add_edge(0, v, {"relation": "ROOT"})
            heads.add(v)
            continue
        if g.has_edge(0, v):
            continue
        # TODO: penalize punctuation as head
        parent = None
        parent_candidates = []
        if "upos" in g.node[v] and not no_rules:
            parent_upos = dep_rules.get(g.node[v]["upos"], set())
            parent_candidates = [u for u in heads if g.node[u]["upos"] in parent_upos]
        if len(parent_candidates) > 0:
            # if g.node[v]["upos"] == "DET":
            #     right = [pc for pc in parent_candidates if pc > v]
            #     if len(right) > 0:
            #         parent = min(right, key=lambda u: (abs(u - v), pr_dict[u] * -1.0))
            #     else:
            #         parent = min(parent_candidates, key=lambda u: (abs(u - v), pr_dict[u] * -1.0))
            # else:
            parent = min(parent_candidates, key=lambda u: (abs(u - v), pr_dict[u] * -1.0))
        else:
            parent = min(heads, key=lambda u: (abs(u - v), pr_dict[u] * -1.0))
        heads.add(v)
        g.add_edge(parent, v, {"relation": "DEP"})
    return g


def parse_sentence_graph(args):
    """Parse sentence graph using the algorithm by Søgaard (2012)."""
    (s, sid), function_words, no_rules = args
    s = _add_edges(s, function_words)
    pr = _rank_vertices(sid, s)
    p = _construct_parse_tree(s, pr, no_rules)
    return p


def parse_sentence(tokens, function_words, no_rules, tags=[], tagset=None):
    """Parse sentence using the algorithm by Søgaard (2012).
    
    Args:
        tokens: list of tokens
        function_words: set of function words
        no_rules: boolean; true if universal dependency rules should
            not be used
        tags: list of tags, if available; the nth element of tags
            should be the part-of-speech tag associated with the nth
            element of tokens
        tagset: string identifying one of the supported tagsets
    
    Returns:
        A networkx DiGraph representing the dependency structure.

    """
    sentence = None
    if len(tokens) == len(tags):
        sentence = list(zip(tokens, tags))
    else:
        if len(tags) > 0:
            logging.warning("len(tokens) != len(tags) -- will not use part-of-speech tags")
        sentence = list(zip(tokens))
    s = tsv.create_nx_digraph_from_tsv(sentence, tagset)
    return parse_sentence_graph(((s, None), function_words, no_rules))
