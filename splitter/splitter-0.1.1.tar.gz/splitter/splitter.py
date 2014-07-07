# -*- coding: utf-8 -*-
"""Split a single text into smaller parts.

Counts words by counting spaces. Optionally, the script will attempt to preserve
sentence boundaries.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import logging
import math
import os
import re

logger = logging.getLogger('splitter')

_SENT_RE = re.compile(r'[^\.;。]*[\.;。]\s*')
_TOKEN_RE = re.compile(r'\s*\S+\s*')


def _tokenize(s):
    """Tokenize string without capturing any whitespace."""
    return _TOKEN_RE.findall(s)


def _sent_tokenize(s):
    """Split string into sentences delimited by periods or semicolons.

    Delimiters are not captured. Matches CJK period as well as ASCII periods.
    """
    return _SENT_RE.findall(s)


def _split_preserve_sentences(text, n_words):
    """Split a long text into chunks of approximately `n_words` words.

    Attempt to preserve sentences.
    """
    sentences = _sent_tokenize(text)
    # we want to treat the list of sentences as a stack that we can pop from
    # and push to. The easiest way to do this is just to reverse the list and
    # use the methods pop and append.
    chunks = []
    current_chunk_words = []
    sentences.reverse()
    while sentences:
        current_chunk_words_copy = current_chunk_words.copy()
        sent = sentences.pop()
        words = _tokenize(sent)
        current_chunk_words.extend(words)
        if len(words) > n_words:
            raise RuntimeError("One sentence contains more than `n_words`: {}".format(sent))
        if len(current_chunk_words) > n_words:
            # over limit, push current sentence back onto stack
            sentences.append(sent)
            chunk = ''.join(current_chunk_words_copy)
            chunks.append(chunk)
            # start over for the next chunk
            current_chunk_words = []
    final_chunk = ''.join(current_chunk_words)
    chunks.append(final_chunk)
    return chunks


def _split(text, n_words):
    """Split a long text into chunks of approximately `n_words` words."""
    words = _tokenize(text)
    chunks = []
    current_chunk_words = []
    for word in words:
        current_chunk_words.append(word)
        if len(current_chunk_words) == n_words:
            chunk = ''.join(current_chunk_words)
            chunks.append(chunk)
            # start over for the next chunk
            current_chunk_words = []
    final_chunk = ''.join(current_chunk_words)
    chunks.append(final_chunk)
    return chunks


def splitter(filename, output_dir, n_words, preserve_sentences):
    """Splits text and writes parts to files."""
    text = open(filename, 'r').read()
    filename_base, filename_ext = os.path.splitext(os.path.basename(filename))
    if preserve_sentences:
        chunks = _split_preserve_sentences(text, n_words)
    else:
        chunks = _split(text, n_words)

    # we want a suffix that identifies the chunk, such as "02" for the 2nd
    # chunk. Python has a couple of standard ways of doing this that should
    # be familiar from other programming languages. For example,
    # "{:04d}".format(2) => "0002"
    n_pad_digits = int(math.log10(len(chunks))) + 1
    chunk_filename_template = "{{}}_split{{:0{}d}}{{}}".format(n_pad_digits)
    for i, chunk in enumerate(chunks):
        chunk_filename = chunk_filename_template.format(filename_base, i, filename_ext)
        with open(os.path.join(output_dir, chunk_filename), 'w') as f:
            f.write(chunk)
    logging.info("Split {} into {} files. Saved to {}".format(filename, len(chunks), output_dir))


def main():
    parser = argparse.ArgumentParser(description='Split text into parts.')
    parser.add_argument('input_filename', type=str, help='Input text filename')
    parser.add_argument('output_dir', type=str, help='Output directory')
    parser.add_argument('n_words', type=int, help='Each part has this many words')
    parser.add_argument('--preserve-sentences', action='store_true',
                        help='Try to preserve sentences')
    args = parser.parse_args()
    filename = args.input_filename
    output_dir = args.output_dir
    n_words = args.n_words
    preserve_sentences = args.preserve_sentences

    splitter(filename, output_dir, n_words, preserve_sentences)


if __name__ == "__main__":
    main()
