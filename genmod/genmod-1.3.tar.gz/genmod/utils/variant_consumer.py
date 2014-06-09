#!/usr/bin/env python
# encoding: utf-8
"""
variant_consumer.py

Class that takes a list of objects and return all unordered pairs as a generator.

If only one object? Raise Exception
 
Created by Måns Magnusson on 2013-03-01.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

from __future__ import division
import sys
import os
import multiprocessing
import sqlite3
import operator
from functools import reduce
from math import log10
from pysam import Tabixfile, asTuple

from pprint import pprint as pp

from genmod.models import genetic_models

class VariantConsumer(multiprocessing.Process):
    """Yeilds all unordered pairs from a list of objects as tuples, like (obj_1, obj_2)"""
    
    def __init__(self, task_queue, results_queue, family, phased=False, vep=False, 
                    cadd_file=None, cadd_1000g=None, thousand_g=None, chr_prefix=False, verbosity=False):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.family = family
        self.results_queue = results_queue
        self.verbosity = verbosity
        self.phased = phased
        self.vep = vep
        self.cadd_file = cadd_file
        self.cadd_1000g = cadd_1000g
        self.thousand_g = thousand_g
        self.chr_prefix = chr_prefix
        if self.cadd_1000g:
            self.cadd_1000g = Tabixfile(self.cadd_1000g, parser = asTuple())
        if self.cadd_file:
            self.cadd_file = Tabixfile(self.cadd_file, parser = asTuple())
        if self.thousand_g:
            self.thousand_g = Tabixfile(self.thousand_g, parser = asTuple())
        
        
    def fix_variants(self, variant_batch):
        """Merge the variants into one dictionary, make shure that the compounds are treated right."""
        fixed_variants = {}
        for feature in variant_batch:
            for variant_id in variant_batch[feature]:
                if variant_id in fixed_variants:
                    # We need to add compound information from different features
                    if len(variant_batch[feature][variant_id]['Compounds']) > 0:
                        fixed_variants[variant_id]['Compounds'] = (
                         dict(list(variant_batch[feature][variant_id]['Compounds'].items()) +
                                    list(fixed_variants[variant_id]['Compounds'].items())))
                else:
                    fixed_variants[variant_id] = variant_batch[feature][variant_id]
        
        return fixed_variants
    
    def get_cadd_score(self, variant):
        """Get the cadd score and add it to the variant."""
        cadd_score = '-'
        alternatives = variant['ALT'].split(',')
        longest_alt = max([len(alt) for alt in alternatives]+[len(variant['REF'])])
        # CADD values are only for snps:
        cadd_key = int(variant['POS'])
        if self.cadd_file:
            try:
                for tpl in self.cadd_file.fetch(str(variant['CHROM']), cadd_key-1, cadd_key):
                    if alternatives[0] == str(tpl[3]):
                        try:
                            return str(tpl[-1], encoding='utf-8')
                        except TypeError:
                            return str(unicode(tpl[-1], encoding='utf-8'))
            except (IndexError, KeyError) as e:
                pass
        #If cadd file was provided and the variant was found the score has been returned, otherwise check 1000g file:
        if self.cadd_1000g:
            try:
                for tpl in self.cadd_1000g.fetch(str(variant['CHROM']), cadd_key-1, cadd_key):
                    #This is for compability between python versions:
                    try:
                        return str(tpl[-1], encoding='utf-8')
                    except TypeError:
                        return str(unicode(tpl[-1], encoding='utf-8'))
            except (IndexError, KeyError) as e:
                pass
        return cadd_score
    
    def get_1000g_freq(self, variant):
        """Get the frequency from 1000g."""
        freq = '-'
        alternatives = variant['ALT'].split(',')
        longest_alt = max([len(alt) for alt in alternatives]+[len(variant['REF'])])
        # CADD values are only for snps:
        cadd_key = int(variant['POS'])
        if self.thousand_g:
            try:
                for tpl in self.thousand_g.fetch(str(variant['CHROM']), cadd_key-1, cadd_key):
                    #This is for compability between python versions:
                    try:
                        if str(tpl[3], encoding='utf-8') == variant['REF']:
                            for info in str(tpl[7], encoding='utf-8').split(';'):
                                if info.split('=')[0] == 'AF':
                                    return info.split('=')[-1]
                    except TypeError:
                        if str(unicode(tpl[3], encoding='utf-8')) == variant['REF']:
                            for info in str(unicode(tpl[7], encoding='utf-8')).split(';'):
                                if info.split('=')[0] == 'AF':
                                    return info.split('=')[-1]
            except (IndexError, KeyError) as e:
                pass
        
        return freq
        
    
    def get_model_score(self, individuals, variant):
        """Return the model score for this variant."""
        model_score = '-'
        genotype_scores = []
        
        
        for individual in individuals:
            gt_call = variant[individual].split(':')
            gt_info = variant['FORMAT'].split(':')
            if len(gt_call) == 1:
                gt_call = {'GT':gt_call[0]}
            else:
                gt_call = dict(zip(gt_info, gt_call))
            if 'GQ' in gt_call:
                # Add the error probabilities to genotype scores
                genotype_scores.append(10**-(float(gt_call['GQ'])/10))
        if len(genotype_scores) > 0:
            model_score = (str(round(-10*log10(1-reduce(operator.mul, [1-score for score in genotype_scores])))))
        
        return model_score
        
    
    def make_print_version(self, variant_dict):
        """Get the variants ready for printing"""
        for variant_id in variant_dict:
            if self.cadd_file or self.cadd_1000g:
                variant_dict[variant_id]['CADD'] = self.get_cadd_score(variant_dict[variant_id])
            if self.thousand_g:
                variant_dict[variant_id]['1000G'] = self.get_1000g_freq(variant_dict[variant_id])
            model_list = []
            compounds_list = []
            #Remove the 'Genotypes' post since we will not need them for now
            variant_dict[variant_id].pop('Genotypes', 0)
            
            feature_list = variant_dict[variant_id]['Annotation']
            
            if len(variant_dict[variant_id]['Compounds']) > 0:
                #We do not want reference to itself as a compound:
                variant_dict[variant_id]['Compounds'].pop(variant_id, 0)
                compounds_list = list(variant_dict[variant_id]['Compounds'].keys())
            else:
                compounds_list = ['-']
            
            for model in variant_dict[variant_id]['Inheritance_model']:
                if variant_dict[variant_id]['Inheritance_model'][model]:
                    model_list.append(model)
            if len(model_list) == 0:
                model_list = ['NA']            
            
            variant_dict[variant_id].pop('Compounds',0)
            variant_dict[variant_id].pop('Inheritance_model',0)
            variant_dict[variant_id].pop('Annotation',0)
            vcf_info = variant_dict[variant_id]['INFO'].split(';')
            
            if self.chr_prefix:
                variant_dict[variant_id]['CHROM'] = 'chr'+variant_dict[variant_id]['CHROM']
            
            # We only want to include annotations where we have a value
            
            if not self.vep:
                if len(feature_list) != 0 and feature_list != ['-']:
                    vcf_info.append('ANN=' + ':'.join(feature_list))
            if compounds_list != ['-']:
                vcf_info.append('Comp=' + ':'.join(compounds_list))
            # if we should include genetic models:
            if model_list != ['NA']:
                vcf_info.append('GM=' + ':'.join(model_list))
                vcf_info.append('MS=' +  self.get_model_score(self.family.individuals, variant_dict[variant_id]))
            cadd_score = str(variant_dict[variant_id].pop('CADD', '-'))
            if cadd_score != '-':
                vcf_info.append('CADD=%s' % cadd_score)
            thousand_g_freq = str(variant_dict[variant_id].pop('1000G', '-'))
            if thousand_g_freq != '-':
                vcf_info.append('1000G_freq=%s' % thousand_g_freq)
            
            variant_dict[variant_id]['INFO'] = ';'.join(vcf_info)
        return
    
    def run(self):
        """Run the consuming"""
        proc_name = self.name
        if self.verbosity:
            print('%s: Starting!' % proc_name)
        while True:
            # A batch is a dictionary on the form {gene:{variant_id:variant_dict}}
            next_batch = self.task_queue.get()
            # if self.verbosity:
                # if self.results_queue.full():
                #     print('Batch results queue Full! %s' % proc_name)
                # if self.task_queue.full():
                #     print('Variant queue full! %s' % proc_name)
            if next_batch is None:
                self.task_queue.task_done()
                if self.verbosity:
                    print('%s: Exiting' % proc_name)
                break
            genetic_models.check_genetic_models(next_batch, self.family, self.verbosity, self.phased, proc_name)
            # Make shure we only have one copy of each variant:
            fixed_variants = self.fix_variants(next_batch)
            
            # Now we want to make versions of the variants that are ready for printing.
            self.make_print_version(fixed_variants)
            self.results_queue.put(fixed_variants)
            self.task_queue.task_done()
        return
        
    

def main():
    pass

if __name__ == '__main__':
    main()