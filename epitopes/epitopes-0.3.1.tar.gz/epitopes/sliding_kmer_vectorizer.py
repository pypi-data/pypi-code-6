# Copyright (c) 2014. Mount Sinai School of Medicine
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize

from reduced_alphabet import make_alphabet_transformer

class SlidingKmerVectorizer(object):
    """
    Splits input strings (of length >= k) into k-mer substrings. 
    
    `transform` and `fit_transform` methods 
    returns a matrix of kmers and a vector of sample weights (1 / # kmers in a string)
    """
    def __init__(
            self,
            kmer_length = 9,
            reduced_alphabet = None):
        self.reduced_alphabet = reduced_alphabet
        self.kmer_length = kmer_length

    def __getstate__(self):
        return {
            'reduced_alphabet': self.reduced_alphabet,
            'kmer_length' : self.kmer_length
        }

    def fit_transform(self, amino_acid_strings):
        self.alphabet_transformer = make_alphabet_transformer(self.reduced_alphabet)
        
        if self.training_already_reduced:
            c = make_count_vectorizer(None, self.max_ngram)
            X = c.fit_transform(amino_acid_strings).todense()
            self.count_vectorizer.vocabulary_ = c.vocabulary_
        else:
            c = self.count_vectorizer
            X = c.fit_transform(amino_acid_strings).todense()

        if self.normalize_row:
            X = normalize(X, norm='l1')
        return X

    def fit(self, amino_acid_strings):
        self.fit_transform(amino_acid_strings)

    def transform(self, amino_acid_strings):
        assert self.count_vectorizer, "Must call 'fit' before 'transform'"
        X = self.count_vectorizer.transform(amino_acid_strings).todense()
        if self.normalize_row:
            X = normalize(X, norm='l1')
        return X
