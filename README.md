# Sampling Euler tours for uniform stimulus history

## Table of Contents

* [About](#about)
* [Examples](#examples)
	* [Experiment 1](#experiment-1)
	* [Experiment 2](#experiment-2)
	* [Experiment 3](#experiment-3)
	* [Experiment 4](#experiment-4)
	* [Experiment 5](#experiment-5)	
* [Contact](#contact)


## About

This is a Python library that implements the methods described in the article _Controlling precedence in sequential stimulus presentation with Euler tours_, available on [PsyArXiv](https://psyarxiv.com/y8r6k/). It contains two files:

1. ```euler.py```: contains all functionality for generating sequences of stimuli. Add this file to your working directory and import it using ```import euler``` to use the library.
2. ```sequence.py```: contains examples of generating sequences of stimuli for various experimental parameters. Run it by calling ```python sequence.py``` on the command line.


## Examples

The file ```sequence.py``` contains a number of examples on how to use the library to generate sequences for various experimental parameters. These example experiment setups and corresponding generated sequences are included below.

### Experiment 1

Generate sequence for four stimuli with each pair occurring once, including repeated stimuli. These are the default settings, so no need to specify any parameters for this experiment.

Input:

```python
experiment = euler.Euler()
print(experiment.get_sequence())
```

Output:

```
['3', '0', '0', '1', '2', '1', '3', '1', '1', '0', '2', '3', '3', '2', '2', '0', '3']
```

### Experiment 2

Generate sequence for 3 stimuli without same-stimulus pairs, and with catch trials occurring on average every 1/4 stims. Force the sequence to start at stimulus 0.

Input:

```python
experiment = euler.Euler(stimuli=3, catch_frequency=0.25, stim_repeat=False)
print(experiment.get_sequence(0))
```

Output:

```
['0', '2', '1', '0', 'C', '0', '1', 'C', '1', '2', 'C', '2', '0']
```

### Experiment 3

Generate sequence with equal catch trial precedence, and each pair of stimuli twice.

Input:

```python
experiment = euler.Euler(catch_to_all=True, pair_repeats=2)
print(experiment.get_sequence())
```

Output:

```
['1', '2', '0', '0', '1', '3', '3', 'C', '0', '1', '1', '2', '3', '3', 'C', '2', 'C', '1', '0', '2', '0', 'C', '0', 'C', '3', '1', 'C', '1', '0', '0', '3', '0', '2', '2', '3', '2', '2', '1', '1', 'C', '2', '1', '3', '2', 'C', '3', '0', '3', '1']
```

### Experiment 4

Generate sequence by stitching two sequences for five stimuli together. Repeating sequences (exp. 4) is different from repeating pairs (exp. 3): it guarantees that all pairs have occurred exactly once in the first half.

Input:

```python
experiment = euler.Euler(stimuli=5, seq_repeats=2)
print(experiment.get_sequence())
```

Output:

```
['2', '1', '0', '3', '3', '0', '2', '2', '0', '1', '2', '4', '3', '4', '4', '2', '3', '1', '4', '0', '0', '4', '1', '1', '3', '2', '2', '4', '4', '1', '3', '3', '1', '1', '4', '0', '3', '4', '3', '2', '3', '0', '0', '4', '2', '1', '0', '1', '2', '0', '2']
```

### Experiment 5

Generate sequence for four stimuli with each triplet occurring once.

Input:

```python
experiment = euler.Euler(triplets=True, stim_repeat=False)
print(experiment.get_sequence())
```

Output:

```
['0', '1', '2', '3', '0', '2', '3', '2', '0', '2', '0', '1', '3', '2', '1', '3', '0', '3', '2', '3', '1', '3', '1', '0', '3', '1', '2', '1', '2', '0', '3', '0', '1', '0', '2', '1', '0', '1']
```

## Contact

[Jacob Bakermans](http://users.ox.ac.uk/~phys1358/) - jacob.bakermans [at] gmail.com

Project Link: [https://github.com/jbakermans/stimulus-history-euler-tours](https://github.com/jbakermans/stimulus-history-euler-tours)
