#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 16:38:55 2021

@author: jbakermans
"""

import random
import copy

class Euler():
    
    def __init__(self, 
                 stimuli=4, 
                 catch_frequency=0,
                 catch_to_all=False,
                 stim_repeat=True, 
                 pair_repeats=1, 
                 seq_repeats=1,
                 triplets=False):
        
        # Process all provided experiment parameter input:
        # Number of stimuli
        self.stimuli = int(stimuli)
        # Catch frequency: number of catch trials / number of trials
        # Catch frequency can't be > 0.5, because we add a stim for each catch
        self.catch_frequency = 0 if triplets else max(min(catch_frequency, 0.5), 0)
        # Whether catch vertex is connected to all stim vertices,
        # to guarantee equal stim number and stim catch precedence
        self.catch_to_all = bool(catch_to_all)
        # Whether to include same-stimulus pairs (e.g. 1,1)
        self.stim_repeat = bool(stim_repeat)
        # Number of times to repeat each pair in the output sequence
        self.pair_repeats = int(pair_repeats)
        # Number of sequences stitched together in the output sequence
        self.seq_repeats = int(seq_repeats)
        
        # Initialise internal variables from processed input:
        # Set function to use for creating base graph of stimuli
        self.graph_function = graph_triplet_create if triplets else graph_create
        # Calculate nr of catch trials
        self.catch_number = int(stimuli if self.catch_to_all else
            ((self.stimuli * (self.stimuli - (int(not self.stim_repeat))) + 1)
            / (1 / self.catch_frequency - 2)
            if self.catch_frequency > 0 else 0)) * self.pair_repeats        
        # Build base graph (without catch trial vertex) for this experiment
        self.graph_base = self.graph_function(self.stimuli,
                                              self.pair_repeats, 
                                              self.stim_repeat)
        # Build full graph (including catch vertex) by augmenting base graph
        self.graph_full = graph_augment(self.graph_base, self.catch_number)
        
    def get_sequence(self, start=None):
        # Set start randomly if not provided
        start = random.randint(0, self.stimuli - 1) if start is None else start
        # Start with empty sequence
        sequence = []
        # Then sample random Euler tour for each sequence repeat
        for i in range(self.seq_repeats):
            # Re-augment graph, so catch trials connect differently for each sequence
            self.graph_full = graph_augment(self.graph_base, self.catch_number)
            # Sample arborescence
            T = get_arborescence(self.graph_full, start)
            # Shuffle graph edges
            graph_shuffle(self.graph_full, T)
            # Get Euler tour
            tour = get_tour(self.graph_full, start)
            # Add tour to sequence, chopping off first stim if sequence isn't empty
            sequence += tour if len(sequence) == 0 else tour[1:]
        # Translate sequence of vertices to sequence of stimuli
        sequence = [self.graph_full['v'][v_i]['name'][0] for v_i in sequence] \
            + self.graph_full['v'][sequence[-1]]['name'][1:]
        return sequence
    
def graph_create(N, R, include_self):
    # Create graph dictionary
    graph = {}
    # Initialise graph vertices: dictionaries of in and out edges
    graph['v'] = [{'id': i, 'name': [str(i)], 'in': [], 'out': []} for i in range(N)]
    # Initialise graph edges: empty list
    graph['e'] = []
    # Now populate lists of edges
    for v_i, v_from in enumerate(graph['v']):
        # Run through all vertices this vertex connects to
        for v_j, v_to in enumerate(graph['v']):
            # Only include self-edges if include_self is True
            if include_self or v_i != v_j:
                # Make edges for as many repeats as requested
                for _ in range(R):
                    # Create new edge
                    e_new = {'id': len(graph['e']), 'source': v_i, 'target': v_j}
                    # Add new edge to graph (in-place)
                    graph_add_edge(graph, e_new)
    return graph    
    
def graph_triplet_create(N, R, include_self):
    # Create graph dictionary
    graph = {}
    # Initialise graph vertices: empty list
    graph['v'] = []
    # Now generate vertices, consisting of pairs of stimuli
    for v_i in range(N):
        # Run through all vertices this vertex connects to
        for v_j in range(N):
            # Only include same-stim pairs if include_self is true
            if include_self or v_i != v_j:
                # Add vertex, with name reflecting stimulus pair
                graph['v'] += [{'id': len(graph['v']), 'name': [str(v_i), str(v_j)],
                                'in': [], 'out': []}]
    # Initialise graph edges: empty list
    graph['e'] = []
    # Now generate edges between vertices whose pairs form triplets
    for v_i, v_from in enumerate(graph['v']):
        # Run through all other vertices to check if they match
        for v_j, v_to in enumerate(graph['v']):
            # Connect vertices if they match
            if v_from['name'][-1] == v_to['name'][0]:
                # Make edges for as many repeats as requested
                for _ in range(R):
                    # Create new edge
                    e_new = {'id': len(graph['e']), 'source': v_i, 'target': v_j}
                    # Add new edge to graph (in-place)
                    graph_add_edge(graph, e_new)
    return graph    

def graph_augment(graph, C):
    # Deep copy the input graph so the input graph won't be affected
    graph = copy.deepcopy(graph)
    # Only add catch vertex if there are catch trials
    if C > 0:
        # Add a vertex for the catch trial
        graph['v'] += [{'id': len(graph['v']), 'name': ['C'], 'in': [], 'out': []}]
        # Shuffle other vertices to connect catch trial vertex to
        connect = [i for i in range(len(graph['v'])-1)]
        # Random.shuffle works in place (doesn't return anything), so do like this
        random.shuffle(connect)
        # Add birectional edge for each catch trial
        for c_i in range(C):
            # Get which vertex this catch trial gets connected to
            v = connect[c_i % (len(graph['v'])-1)]
            # Create new edge towards catch vertex
            e_in = {'id': len(graph['e']), 
                    'source': v, 'target': len(graph['v']) - 1}
            # And a new edge from catch vertex
            e_out = {'id': len(graph['e']) + 1, 
                     'source': len(graph['v']) - 1, 'target': v}
            # Add new edges to graph (in-place)
            for e_new in [e_in, e_out]:
                graph_add_edge(graph, e_new)
    return graph
    
def graph_shuffle(graph, T):
    # Randomly shuffle order of edges for each vertex, making sure any edges
    # in arborescence are at the very bottom of the list (in-place, so no return)
    for v in graph['v']:
        # Get all edges to shuffle: those not in arborescence
        to_shuffle = [e for e in v['out'] if e['id'] not in T]
        # Get edges at end of list (should never be more than 1!)
        at_end = [e for e in v['out'] if e['id'] in T]
        # Shuffle edges in place
        random.shuffle(to_shuffle)
        # And stick shuffled edges back in
        v['out'] = to_shuffle + at_end

def graph_add_edge(graph, e_new):
    # Add edge to egde array
    graph['e'] += [e_new]
    # Add edge to source note outgoing edges
    graph['v'][e_new['source']]['out'] += [e_new]
    # And add edd to target node incoming edges
    graph['v'][e_new['target']]['in'] += [e_new]    

def get_arborescence(graph, v_i):
    # Keep track for each state whether it was visited
    visited = [False for _ in graph['v']]
    # And mark initial vertex as visited
    visited[v_i] = True
    # Start with empty arborescence: list of edges in inbound spanning tree
    T = []
    # Do backwards random walk until all vertices are visited 
    # to randomly sample arborescence (see Kandel et al 1996, page 182)
    while not all(visited):
        # Uniform-randomly select edge leading to current vertex
        e = random.choice(graph['v'][v_i]['in'])
        # Update current vertex as source vertex of selected edge
        v_i = e['source']
        # If vertex wasn't visited before: add selected edge to arborescence
        T += [e['id']] if not visited[v_i] else []
        # And mark current vertex as visited
        visited[v_i] = True
    return T

def get_tour(graph, v_i):
    # Now build tour from start using each edge once. Keep track of used edges
    used = [False for _ in graph['e']]
    # Initialise tour at start
    tour = [v_i]
    # Use edge at top of list until all vertices are used
    for step in range(len(graph['e'])):
        # Select first unused edge
        e = next(e for e in graph['v'][v_i]['out'] if not used[e['id']])
        # Update current vertex as target of selected edge
        v_i = e['target']
        # Add current vertex to tour
        tour += [v_i]
        # Mark edge as used
        used[e['id']] = True
    return tour