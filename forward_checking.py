from heuristics import *
from queue import LifoQueue
import numpy as np

import argparse
import sys
import random
import time
import copy

node_count = 0


def forward_checking(puzzle, empty_cells, wall_cells, deleted_empty_cell, heuristic):

    """
    :param puzzle: List[List[str]]
    :param domain: List[str] - The domain of posible values each cell in empty cell could take
    :param empty_cells: List[List[int]] - List of position [x,y] of each empty cell.
    :param wall_cells: List[List[int]] - List of position [x,y] of each wall cell.
    :param deleted_empty_cell: stack(List[int]) - Stack of positions of empty cells that got deleted in the process
    :param heuristic: String - "H1", "H2", or "H3". To decide the heuristic
    :return: The complete solution, or no solution if puzzle is not solvable
    """

    global node_count
    node_count += 1

    # printing solving status

    if node_count % 10000 == 0:
        print('\rAlready processed {} nodes.'.format(node_count))

    if node_count == 500000:
        return 'Too many nodes. Timeout!'

    if is_solved(puzzle):
        return puzzle

    next_potential_cells = []

    # Check input for the heuristic to use
    if heuristic == 'H1':
        next_potential_cells = most_constrained_variable_heuristic(puzzle, empty_cells)  # Find most constrained
    elif heuristic == 'H2':
        next_potential_cells = most_constraining_variable_heuristic(puzzle, empty_cells)  # Find most constraining
    elif heuristic == 'H3':
        next_potential_cells = hybrid_heuristic(puzzle, empty_cells)  # Hybrid
    else:
        print('\n*** ERROR *** Heuristic must be either "H1", "H2", or "H3".')
        return 'Abort!!'

    # If we have more than 1 chosen cells, randomly pick 1
    # else, pick the only one we have
    # next_cell holds the position of the next cell chosen
    if len(next_potential_cells) >= 1:
        next_cell = next_potential_cells[random.randint(0, len(next_potential_cells) - 1)]
    else:    # We have no empty cell to consider, and the puzzle is still not solved, so backtrack here!
        return 'backtrack'

    # # remove the cell chosen above from the list of temporary empty cells
    # temp_empty_cells = copy.deepcopy(empty_cells)
    # temp_empty_cells.remove(next_cell)

    deleted_empty_cell.put(next_cell)
    empty_cells.remove(next_cell)

    row, col = next_cell[0], next_cell[1]

    # Get the domain of the cell we chose
    next_cell_domain = puzzle[row][col].get_cell_domain()

    # Try each value in the domain of the chosen variable
    for i in range(len(next_cell_domain)):
        value = next_cell_domain[i]

        # Create a copy of the current puzzle state for variable assignment
        temp_puzzle = copy.deepcopy(puzzle)

        temp_puzzle[row][col].set_cell_value(value)

        domain_change(temp_puzzle, row, col, value)

        check_no_empty_domain = no_empty_domain(temp_puzzle, empty_cells)
        feasible_for_all_wall = check_wall_feasibility(temp_puzzle, wall_cells)

        if is_state_valid(temp_puzzle) and check_no_empty_domain and feasible_for_all_wall:
            result = forward_checking(temp_puzzle, empty_cells, wall_cells, deleted_empty_cell, heuristic)
            if result != 'backtrack' and result != 'failure':
                return result

    return 'failure'


def domain_change(puzzle, row, col, value):
    """
    # With the row-col position of a chosen cell and the new value of that cell, if the new value is 'b'
    # then modifying all the '_' cell that the chosen cell could "see" by excluding "b" out of their domain
    # If the new value is '_', nothing to do
    :param puzzle: List[List[Cell]] - The puzzle
    :param row: int - row index of the cell that got assigned variable
    :param col: int - col index of the cell that got assigned variable
    :param value: the value of the variable (either'_' or 'b'
    :return: NA
    """

    #TODO: remove this after finish
    '''
    print('in domain change function, the domain passed in is:')
    print_domain(domain)
    '''

    if value == CellState.BULB:

        travel_dist = 1

        # Keep travel if we still in domain map, and the cell domain we are looking at is not wall

        # Up
        while row - travel_dist >= 0 and not puzzle[row - travel_dist][col].is_wall():
            cell = puzzle[row - travel_dist][col]
            cell.remove_bulb_from_domain()
            travel_dist += 1

        travel_dist = 1

        # Down
        while row + travel_dist < len(puzzle) and not puzzle[row + travel_dist][col].is_wall():
            cell = puzzle[row + travel_dist][col]
            cell.remove_bulb_from_domain()
            travel_dist += 1

        travel_dist = 1

        # To the left
        while col - travel_dist >= 0 and not puzzle[row][col - travel_dist].is_wall():
            cell = puzzle[row][col - travel_dist]
            cell.remove_bulb_from_domain()
            travel_dist += 1

        travel_dist = 1

        # To the right
        while col + travel_dist < len(puzzle[0]) and not puzzle[row][col + travel_dist].is_wall():
            cell = puzzle[row][col + travel_dist]
            cell.remove_bulb_from_domain()
            travel_dist += 1


def no_empty_domain(puzzle, empty_cells):
    """
    Check all empty cells' domain. Domains must have size > 0
    Return True is all cells has domain of size at least 1, False otherwise
    :param puzzle: The current state of the puzzle
    :param empty_cells: List of positions of empty cells
    :return: bool
    """

    for position in empty_cells:
        row, col = position[0], position[1]
        if puzzle[row][col].has_domain_of_size_zero():
            return False
    return True


def check_wall_feasibility(puzzle, wall_cells):
    """
    # Check the surrounding of each wall
    # Return true if for each wall, the number of cells around it that could accept a bulb is >= wall value
    :param puzzle: List[List[Cell]]
    :param wall_cells: List[List[int]] - the positions of the walls
    :return: bool
    """

    valid = True
    i = 0

    while valid and i < len(wall_cells):

        row, col = wall_cells[i][0], wall_cells[i][1]

        # The number of bulbs that must be placed around this wall
        wall_value = int(puzzle[row][col].get_cell_value())
        count = 0

        # Count for the number of available spots to place bulbs around this wall
        if row - 1 >= 0 and puzzle[row-1][col].domain_contain(CellState.BULB):
            count += 1
        if row + 1 < len(puzzle) and puzzle[row+1][col].domain_contain(CellState.BULB):
            count += 1
        if col - 1 >= 0 and puzzle[row][col-1].domain_contain(CellState.BULB):
            count += 1
        if col + 1 < len(puzzle[0]) and puzzle[row][col+1].domain_contain(CellState.BULB):
            count += 1

        # We have less available spots than the # of bulbs that must be placed
        if count < wall_value:
            valid = False

        i += 1

    return valid
