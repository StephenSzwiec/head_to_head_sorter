#!/usr/bin/env python 
# -*- coding: utf-8 -*-

"""
This is a script which:
    - ingests a text file with one item per line 
    - uses 2N - 1 rounds of head-to-head comparisons to sort the items
        - user uses left and right arrow keys to select the item they prefer
    - after sorting, the script displays the sorted list ranking like so:
        1. item1
        2. item2
        ...
    - finally, the sorted list can be saved to a text file if desired

Blessed is a terminal user interface library which behaves more similarly to C++
than typical Python. This script demonstrates Blessed usage, and as such, is
a requirement:
`$ pip --user install blessed` 
or if inside a virtualenv already:
`$ pip install blessed` 
or if already in conda environment:
`$ conda install -c conda-forge blessed`
"""

"""
Region: Metadata
"""
__author__ = "Stephen Szwiec <stephen.szwiec@ndsu.edu>"
__version__ = "0.2.0"
__license__ = "GPL-3.0"
__date__ = "2024-11-11"
__status__ = "Development"
__description__ = "Interactive merge sort demonstrating TUI input handling using Blessed"
__maintainer__ = "Stephen Szwiec <stephen.szwiec@ndsu.edu>"
__email__ = "stephen.szwiec@ndsu.edu"

"""
Region: imports
"""
import sys
import os
import random
from blessed import Terminal

def input_handler(term, i, j):
    """
    Abstraction for the input handling from the user

    Args: 
        - term (blessed.Terminal): a terminal handle
        - i (str): left name to display 
        - j (str): right name to display

    Returns: string 'left', string 'right' or sys.exit()
    """
    print(f"{i} vs {j} (←/→/q): ", end='', flush=True)
    while True:
        key = term.inkey()
        if key.name == 'KEY_LEFT':
            print("←")
            return 'left'
        elif key.name == 'KEY_RIGHT':
            print("→")
            return 'right'
        elif key.lower() == 'q':
            print("q")
            sys.exit()

def head_to_head_sorter(term, items):
    """
    Recursive merge sort 

    Args: 
        - term (blessed.Terminal): a terminal handle
        - items (list): list of items, presumably str

    Returns:
        - list: The list merge-sorted by the user
    """
    if len(items) == 1:
        return items
    random.shuffle(items)
    mid = len(items) // 2
    left = head_to_head_sorter(term, items[:mid])
    right = head_to_head_sorter(term, items[mid:])
    return merge_with_preference(term, left, right)

def merge_with_preference(term, left, right):
    """
    Interior loop of the merge sort which interfaces with user feedback

    Args:
        - term (blessed.Terminal): a terminal handle
        - left (list): list of items, presumably str
        - right (list): list of items, presumably str

    Returns:
        - list: The list merge-sorted by the user
    """
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        choice = input_handler(term, left[i], right[j])
        if choice == 'left':
            result.append(left[i])
            i += 1
        elif choice == 'right':
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def main(term):
    """
    main method

    Args: 
        - term (blessed.Terminal): a terminal handle

    Returns: None
    """
    # open the first terminal argument as a text file 
    filename = sys.argv[1]
    with open(filename) as f:
        items = f.read().splitlines()
    # call sort algorithms
    sorted_items = head_to_head_sorter(term, items)
    print("\nSorted list:")
    for i, item in enumerate(sorted_items):
        print(f'{i+1}. {item}')
    # user can save if they would like to
    print("\nSave sorted list to file? (y/n): ", end='', flush=True)
    while True:
        save = term.inkey()
        if save.lower() == 'y':
            print("y")
            save_filename = input('Enter filename: ')
            with open(save_filename, 'w') as f:
                for item in sorted_items:
                    f.write(f'{item}\n')
            print(f"Sorted list saved to {save_filename}")
            break
        elif save.lower() == 'n':
            print("n")
            break
          
if __name__ == '__main__':
    # Terminal handle exists in the context of using this as the main method
    term = Terminal()
    with term.fullscreen(), term.cbreak():
        main(term)
