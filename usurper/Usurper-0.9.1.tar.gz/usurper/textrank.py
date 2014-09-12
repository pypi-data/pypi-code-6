#!/usr/bin/python

import networkx
import operator
import re

def _words_iter(sentences, conll_format):
    """Iterator over words in sentences.
    
    Args:
        sentences: An iterator containing a lists of lists
            representing sentences (CWB format)

    Returns:
        An iterator

    """
    index = 0
    if conll_format:
        index = 1
    for sentence, sid in sentences:
        for token in sentence:
            yield token[index]


def get_top_n(sentences, n, k, conll_format):
    """A rudimentary implementation of TextRank (Mihalcea and Tarau, 2004)
    for keyword extraction. We do not use any filters or stop word
    lists, i.e. we expect to get the top n function words.
    
    Args:
        sentences: An iterator containing a lists of lists
            representing sentences (CWB format)
        n: number of keywords to extract
        k: window size
    
    Returns:
        The n highest ranked keywords, expected to be function words.

    """
    words = _words_iter(sentences, conll_format)
    window = ["" for _ in range(2 * k + 1)]
    g = networkx.Graph()
    for i, word in enumerate(words):
        window.pop(0)
        window.append(word.lower())
        if i < k:
            continue
        for j, w in enumerate(window):
            if j == k or w == "":
                continue
            g.add_edge(w, window[k])
    for i in range(k):
        window.pop(0)
        window.append("")
        for j, w in enumerate(window):
            if j == k or w == "":
                continue
            g.add_edge(w, window[k])
    pr = networkx.pagerank(g, alpha=1.0)
    pr = {key: value for key, value in pr.items() if not re.search(r"\W", key, re.U)}
    return [_[0] for _ in sorted(pr.items(), key=operator.itemgetter(1), reverse=True)[0:n]]
