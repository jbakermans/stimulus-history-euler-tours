#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 17:26:27 2021

@author: jbakermans
"""

import euler

# Example 1: generate sequence for four stimuli with each pair occurring once
# Create object to sample euler routes on experiment graph with default params
experiment = euler.Euler()
# Sample sequence from random initial stimulus and print result
print(experiment.get_sequence())

# Example 2: sequence without same-stimulus pairs, catch trials every 1/4 stims
experiment = euler.Euler(stimuli=3, catch_frequency=0.25, stim_repeat=False)
# Sample sequence from initial stimulus 0 and print result
print(experiment.get_sequence(0))

# Example 3: sequence with equal catch trial precedence, and each pair twice
experiment = euler.Euler(catch_to_all=True, pair_repeats=2)
# Sample sequence from random initial stimulus and print result
print(experiment.get_sequence())

# Example 4: sequence by stitching two sequences for five stimuli together
# Repeating sequences (exp. 4) is different from repeating pairs (exp. 3):
# It guarantees that all pairs have occurred exactly once in the first half
experiment = euler.Euler(stimuli=5, seq_repeats=2)
# Sample sequence from random initial stimulus and print result
print(experiment.get_sequence())

# Example 5: sequence for four stimuli with each triplet occurring once
experiment = euler.Euler(triplets=True, stim_repeat=False)
# Sample sequence from random initial stimulus and print result
print(experiment.get_sequence())