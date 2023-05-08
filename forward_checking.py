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

    #print("Next cell is: " + str(next_cell))

    deleted_empty_cell.put(next_cell)
    empty_cells.remove(next_cell)

    row, col = next_cell[0], next_cell[1]

    # Get the domain of the cell we chose
    next_cell_domain = puzzle[row][col].get_cell_domain()
    #print("Next cell domain is: " + str(next_cell_domain))

    # Try each value in the domain of the chosen variable
    for i in range(len(next_cell_domain)):
        value = next_cell_domain[i]
        #print("attemp solving at node" + str(node_count))

        # Create a copy of the current puzzle state for variable assignment
        temp_puzzle = copy.deepcopy(puzzle)

        temp_puzzle[row][col].set_cell_value(value)

        domain_change(temp_puzzle, row, col, value)

        check_no_empty_domain = no_empty_domain(temp_puzzle, empty_cells)
        feasible_for_all_wall = check_wall_feasibility(temp_puzzle, wall_cells)

        # print("In front of if")
        # print(is_state_valid(temp_puzzle))
        # print(check_no_empty_domain)
        # print(feasible_for_all_wall)
        # print_puzzle(temp_puzzle)

        if is_state_valid(temp_puzzle) and check_no_empty_domain and feasible_for_all_wall:
            result = forward_checking(temp_puzzle, empty_cells, wall_cells, deleted_empty_cell, heuristic)
            if result != 'backtrack' and result != 'failure':
                return result

    empty_cells.append(next_cell)
    deleted_empty_cell.get()
    return 'failure'


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


def preprocess_puzzle(puzzle, empty_cells, wall_cells, first_pre_process):
    """
    # Pre-processing the given puzzle by placing bulb at sure-place
    # For each bulb that we place, correspondingly reduce the domain of related empty cells
    # Return the total number of changes made in the pre-processing
    :param puzzle: List[List[Cell]] - The puzzle
    :param empty_cells: List[List[int]] - positions of empty cells
    :param wall_cells: List[List[int]] - positions of wall cells
    :param first_pre_process: bool - True if call method for the 1st time, False otherwise
    :return: int
    """

    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    change_count = 0

    for position in wall_cells:
        row = position[0]
        col = position[1]
        wall_value = int(puzzle[row][col].get_cell_value())

        # If seeing a wall of number 0, reduce domain size of all empty walls around it
        # (i.e. take bulb out of domain values)
        if wall_value == 0 and first_pre_process:

            for x_direct, y_direct in directions:
                x_temp, y_temp = row + x_direct, col + y_direct
                if is_in_bounds(puzzle, x_temp, y_temp):
                    puzzle[x_temp][y_temp].remove_bulb_from_domain()

                    # Cells that we cannot place bulb on are no longer considered "empty" for puzzle solving purpose
                    if [x_temp, y_temp] in empty_cells:
                        empty_cells.remove([x_temp, y_temp])

        # If the number of spots in which bulb can be placed matches wall value
        # we place bulbs around this wall
        # and increase number of changes made by 1
        elif available_spots_match_wall_value(puzzle, row, col, wall_value) and wall_value_not_satisfy(puzzle, row, col):
            place_bulbs_around_special_wall(puzzle, row, col, empty_cells, wall_value)
            change_count += 1

    return change_count


# call necessary methods/algorithms to solve the puzzle as required.
def solve_puzzle(puzzle, heuristic):
    """
    Given the puzzle and the chosen heuristic, return the solved puzzle if the puzzle is solvable
    Else, return failure message
    :param puzzle: List[List[Cell]] - The puzzle
    :param heuristic: Str - The chosen heuristic, either "H1", "H2", or "H3"
    :return: The solved puzzle, or the error message
    """

    empty_cells = get_empty_cells(puzzle)

    wall_cells = get_wall_cells(puzzle)
    stack_of_empty_cells = LifoQueue(maxsize=len(puzzle)*len(puzzle))
    changes_count = preprocess_puzzle(puzzle, empty_cells, wall_cells, True)

    while changes_count > 0:
        changes_count = preprocess_puzzle(puzzle, empty_cells, wall_cells, False)

    if is_state_valid(puzzle):
        print("puzzle after pre-processing")
        print_puzzle(puzzle)
        print("Chosen heuristic: {}.".format(heuristic))
        return forward_checking(puzzle, empty_cells, wall_cells, stack_of_empty_cells, heuristic)
    else:
        return "Failure: Puzzle not valid after pre_processing"


def test_main():
    file_name = "test.txt"
    heuristic = "H1"
    puzzle_dict = read_file(file_name)
    for i in puzzle_dict.keys():

        # node_count = 0
        puzzle = puzzle_dict[i]

        if i != 0:
            print()

        print('The puzzle is:')
        print_puzzle(puzzle)

        starting_time = time.time()
        solution = solve_puzzle(puzzle, heuristic)
        ending_time = time.time()

        print()

        if solution == 'Too many nodes. Timeout!':
            print('Number of nodes processed is too high!! Timeout!\nIt took {} seconds.'.format(
                ending_time - starting_time))

        elif solution == 'stop':
            print('Please retry!')

        elif solution == 'failure':
            print('Fail to solve this puzzle. Seems like it\'s unsolvable!!')

        else:
            print('*** Done! ***\nThe solution is printed out below:')
            print_puzzle(solution)
            print("The puzzle was solved in {} seconds.".format(ending_time - starting_time))
        print('Visited {} nodes.'.format(node_count))


test_main()

# receive input, process input and call necessary methods to solve the puzzle.
# def main(argv=None):
#
#     if argv is None:
#         argv = sys.argv[1:]
#
#         arg_parser = argparse.ArgumentParser(add_help=False)
#         arg_parser.add_argument('-p', action='store', dest='file_name', type=str)
#         arg_parser.add_argument('-h', action='store', dest='heuristic', type=str, default='H1')
#
#         arguments = arg_parser.parse_args(argv)
#         file_name = arguments.file_name
#         heuristic = arguments.heuristic
#         puzzle_dict = read_file(file_name)
#
#         for i in puzzle_dict.keys():
#
#             #node_count = 0
#             puzzle = puzzle_dict[i]
#
#             if i != 0:
#                 print()
#
#             print('The puzzle is:')
#             print_puzzle(puzzle)
#
#             starting_time = time.time()
#             solution = solve_puzzle(puzzle, heuristic)
#             ending_time = time.time()
#
#             print()
#
#             if solution == 'Too many nodes. Timeout!':
#                 print('Number of nodes processed is too high!! Timeout!\nIt took {} seconds.'.format(ending_time - starting_time))
#
#             elif solution == 'stop':
#                 print('Please retry!')
#
#             elif solution == 'failure':
#                 print('Fail to solve this puzzle. Seems like it\'s unsolvable!!')
#
#             else:
#                 print('*** Done! ***\nThe solution is printed out below:')
#                 print_puzzle(solution)
#                 print("The puzzle was solved in {} seconds.".format(ending_time - starting_time))
#             print('Visited {} nodes.'.format(node_count))
#
# if __name__ == '__main__':
#     main()