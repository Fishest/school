#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
TODO:

* finish c++ implementation
* https://class.coursera.org/optimization-002/forum/thread?thread_id=171
* branch and bound
* numpy sparse
'''

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def dynamic_solution(capacity, items):
    ''' Given a capacity and a collection of items, solve
    the knapsack problem using a dynamic programming approach.

    :param capacity: The total capacity of the knapsack
    :param items: The possible items to choose from
    :returns: The optimal solution
    '''
    lookup = [[0] * (len(items) + 1) for _ in range(capacity + 1)]
    for index, item in enumerate(items, start=1):
        for weight in range(1, capacity + 1):
            lookup[weight][index] = lookup[weight][index - 1]
            if item.weight <= weight:
                possible = item.value + lookup[weight - item.weight][index - 1]
                lookup[weight][index] = max(lookup[weight][index], possible)

    weight   = capacity
    value    = lookup[weight][len(items)]
    selected = [0] * len(items)

    for index in range(len(items), -1, -1):
        if lookup[weight][index] != lookup[weight][index - 1]:
            selected[index - 1] = 1
            weight -= items[index - 1].weight # item.index = index - 1
    return value, selected

def dynamic_terse_solution(capacity, items):
    ''' Given a capacity and a collection of items, solve
    the knapsack problem using a dynamic programming approach.

    This works by only using a single column to store the previous
    values and thus saving (len(items) - 1) * capacity * sizeof(int)
    amount of memory.

    :param capacity: The total capacity of the knapsack
    :param items: The possible items to choose from
    :returns: The optimal solution
    '''
    lookup = [0] * (capacity + 1)
    for item in items:
        for weight in range(capacity, -1, -1):
            if item.weight <= weight:
                possible = item.value + lookup[weight - item.weight]
                lookup[weight] = max(lookup[weight], possible)

    weight   = capacity
    value    = lookup[weight]
    selected = [0]

    return value, selected

def greedy_solution(capacity, items):
    ''' A trivial greedy algorithm for filling the knapsack
    it takes items in-order until the knapsack is full
    '''
    value    = 0
    weight   = 0
    selected = [0] * len(items)
    by_value = sorted(items, key=lambda i: float(i.value) / i.weight, reverse=True)

    for item in by_value:
        if (weight + item.weight) <= capacity:
            selected[item.index] = 1
            value  += item.value
            weight += item.weight
    return value, selected

def initialize_items(stream):
    ''' Given a stream of data, generate the items
    to choose from and the capacity to meet.

    :param stream: The stream to consume from
    :returns: A tuple of (capacity, items) to work with
    '''
    lines     = stream.split('\n')
    header    = lines[0].split()
    item_size = int(header[0])
    capacity  = int(header[1])

    items = []
    for i in range(1, item_size + 1):
        line  = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))
    return capacity, items

def solve_it(stream):
    ''' Given a stream of data that meets the supplied format,
    choose the optimal solution for packing the knapsack.

    :param stream: A stream of the input data
    :returns: The optimal solution to the problem
    '''
    capacity, items = initialize_items(stream)
    if len(items) <= 200:
        value, taken = dynamic_terse2_solution(capacity, items)
        print "terse: ", value
        value, taken = dynamic_solution(capacity, items)
    else:
        value, taken = greedy_solution(capacity, items)
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

