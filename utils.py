import os
from CellState import *


def read_file(filename):
    file = open(os.getcwd() + '/data/' + filename)
    puzzle_dict = {}
    count = 0
    for line in file:
        if line[0] != "#":
            line = line.split()
            rows, cols = int(line[0].strip()), int(line[1].strip())
            puzzle_dict[count] = [['' for x in range(cols)] for y in range(rows)]

            for row in range(rows):
                line = file.readline()
                for col in range(cols):
                    cell = line[col]
                    puzzle_dict[count][row][col] = cell
            count += 1

    return puzzle_dict


# Modified
def print_puzzle(puzzle):
    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            if col == len(puzzle[0]) - 1:
                print(puzzle[row][col].get_cell_value())
            else:
                print(puzzle[row][col].get_cell_value(), end='')


# Modified
def light_up_puzzle(curr_state):
    """
    Given the current state of the puzzle, with newly placed bulbs
    light up all cells in the same row and col that is not obstructed by wall
    :param curr_state: List[List[Cell]] - the current state of the puzzle
    :return: NA
    """
    # Iterate through each cell in the current state
    for row in range(len(curr_state)):
        for col in range(len(curr_state[row])):

            # For each cell that contains a bulb
            if curr_state[row][col].is_bulb():
                # Iterate on the 4 directions of this cell
                directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
                for x_direct, y_direct in directions:
                    row_temp, col_temp = row + x_direct, col + y_direct
                    # While still in bound and not encounter a wall, keep going
                    while is_in_bounds(curr_state, row_temp, col_temp) and not curr_state[row_temp][col_temp].is_wall():
                        # If the cell is empty, change its state to "LIGHT"
                        if curr_state[row_temp][col_temp].is_empty():
                            curr_state[row_temp][col_temp].set_cell_value(CellState.LIGHT)
                        row_temp, col_temp = row_temp + x_direct, col_temp + y_direct   # Keep going


# Modified
def unlit_puzzle(curr_state):
    """
    Changing state of cells that are in "LIGHT" state to "EMPTY" state
    :param curr_state: List[List[Cell]] - the current state of the puzzle
    """
    # Iterate through all cells to look for empty cells that are in "LIGHT" state
    # and turn those into "EMPTY" state
    for row in range(len(curr_state)):
        for col in range(len(curr_state[row])):
            if curr_state[row][col].is_light():
                curr_state[row][col].set_cell_value(CellState.EMPTY)


# Modified
def num_cells_lighten(curr_state, row, col):
    """
    Given the position [row,col] of a bulb, count the number of cells that that bulb can light up
    Return number of cells the bulb at [row,col] can light up
    :param curr_state: the current state of the puzzle
    :param row: row number of given cell
    :param col: col number of given cell
    :return: int
    """
    count = 0

    # Iterate on the 4 directions of this cell
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    for x_direct, y_direct in directions:
        row_temp, col_temp = row + x_direct, col + y_direct
        # While still in bound and not encounter a wall, keep going
        while is_in_bounds(curr_state, row_temp, col_temp) and not curr_state[row_temp][col_temp].is_wall():
            count += 1
            row_temp, col_temp = row_temp + x_direct, col_temp + y_direct  # Keep going

    return count


# Modified
def count_adjacent_bulbs(puzzle, row, col):
    """
    Count the number of adjacent bulbs around a cell at position [row, col]
    Should only be used to check wall cells
    :param puzzle: List[List[Cell]] - Current state of the puzzle
    :param row: row number of the given cell
    :param col: col number of the given cell
    :return: int
    """

    count = 0
    rows = len(puzzle)
    cols = len(puzzle)

    if row > 0 and puzzle[row - 1][col].is_bulb():  # down
        count += 1
    if row < rows - 1 and puzzle[row + 1][col].is_bulb():  # up
        count += 1
    if col > 0 and puzzle[row][col - 1].is_bulb():  # left
        count += 1
    if col < cols - 1 and puzzle[row][col + 1].is_bulb:  # right
        count += 1

    return count


# Modified
def count_adjacent_walls(puzzle, row, col):
    """
    Count how many walls surround the given cell at [row, col]
    and return this number
    :param puzzle: List[List[Cell]] - Current state of the puzzle
    :param row: row number of the given cell
    :param col: col number of the given cell
    :return: int
    """
    num_walls = 0
    rows = len(puzzle)
    cols = len(puzzle[0])

    if row > 0 and puzzle[row - 1][col].is_wall():  # down
        num_walls += 1
    if row < rows - 1 and puzzle[row + 1][col].is_wall():  # up
        num_walls += 1
    if col > 0 and puzzle[row][col - 1].is_wall():  # left
        num_walls += 1
    if col < cols - 1 and puzzle[row][col + 1].is_wall():  # right
        num_walls += 1

    return num_walls


# Modified
def edge_corner_constraints(puzzle, row, col):
    """
    Check if the given cell at [row, col] is in edge/corner
        - not an edge/corner = 0 (no constraint)
        - edge = 1 (1 side is constrained)
        - corner = 2 (2 sides are constrained)
    :param puzzle: List[List[Cell]] - Current state of the puzzle
    :param row: row number of the given cell
    :param col: col number of the given cell
    :return: int
    """
    constraints = 0
    rows = len(puzzle)
    cols = len(puzzle[0])

    if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:  # edge
        constraints = 1

    if (row == 0 or row == rows - 1) and (col == 0 or col == cols - 1):  # corner
        constraints = 2

    return constraints


# Modified
def is_map_lit_entirely(curr_state):
    """
    Return True if map is lit up entirely, False otherwise
    :param curr_state: List[List[str]] - the current state of the puzzle
    :return: bool
    """

    is_lit_up = True
    light_up_puzzle(curr_state)

    # Iterate through all cells to look for any empty cell that is NOT lit up
    # if we see such cell, solution is not complete
    for row in range(len(curr_state)):
        for col in range(len(curr_state[0])):
            if curr_state[row][col].get_cell_value() == '_':
                is_lit_up = False

    unlit_puzzle(curr_state)
    return is_lit_up


# Modified
def is_in_bounds(curr_state, row, col):
    """
    Check if a given position [row, col] is inside the current puzzle
    :param curr_state: List[List[Cell]] - the current state of the puzzle
    :param row: int - the row number of the cell
    :param col: int - the col number of the cell
    :return: bool
    """

    return 0 <= row < len(curr_state) and 0 <= col < len(curr_state[0])


# Modified
def is_valid_bulb(curr_state, row, col):
    """
    Given a cell, check to see if this cell can "see" another bulb directly
    :param curr_state: List[List[Cell]] - the current state of the puzzle
    :param row: int - the row number of the cell
    :param col: int - the col number of the cell
    :return: bool
    """

    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    for x_direct, y_direct in directions:
        row_temp, col_temp = row + x_direct, col + y_direct
        while is_in_bounds(curr_state, row_temp, col_temp) and not curr_state[row_temp][col_temp].is_wall():
            if curr_state[row_temp][col_temp].is_bulb():
                return False
            row_temp, col_temp = row_temp + x_direct, col_temp + y_direct

    return True


# Modified
def is_solved(curr_state):
    """
    Check if the current state of the puzzle is a solved state (all requirements are satisfied)
    Return True if solved, False otherwise
    :param curr_state: List[List[Cell]] - the current state of the puzzle
    :return: bool
    """
    rows = len(curr_state)
    cols = len(curr_state)

    # Check for any violation of rules
    for row in range(rows):
        for col in range(cols):

            # If the cell is a wall and the number of bulbs around it != its value
            if curr_state[row][col].is_wall():
                if int(curr_state[row][col].get_cell_value()) != count_adjacent_bulbs(curr_state, row, col):
                    return False

            # If the cell is a bulb, and it's not a valid placement
            if curr_state[row][col].is_bulb() and not is_valid_bulb(curr_state, row, col):
                return False

    # Check if the entire puzzle is lit up
    is_all_light_up = is_map_lit_entirely(curr_state)

    return is_all_light_up


# Modified
def is_state_valid(curr_state):
    """
    Check if for each wall cell, the number of bulbs placed around it is <= the value of the wall
    Check if feach bulb we have placed is valid (no 2 bulbs should directly "see" each other)
    :param curr_state: The current state of the puzzle
    :return: bool
    """
    rows = len(curr_state)
    cols = len(curr_state[0])

    for row in range(rows):
        for col in range(cols):

            # If the wall has more bulbs around it than its value, return False
            if curr_state[row][col].is_wall():
                if int(curr_state[row][col].get_cell_value()) < count_adjacent_bulbs(curr_state, row, col):
                    return False

            # If a bulb we place "see" another bulb (invalid placement), return False
            elif curr_state[row][col].is_bulb() and not is_valid_bulb(curr_state, row, col):
                return False

    return True

