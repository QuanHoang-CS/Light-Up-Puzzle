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


def print_puzzle(puzzle):
    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            if col == len(puzzle[0]) - 1:
                print(puzzle[row][col])
            else:
                print(puzzle[row][col], end='')


# Given the current state of the curr_state (the puzzle), with newly placed bulbs,
# light up all cells in the same row and col that is not obstructed by wall using * symbols
def light_up_puzzle(curr_state):
    """
    :param
    :return:
    """

    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    for x_direct, y_direct in directions:
        row_temp, col_temp = row + x_direct, col + y_direct
        while is_in_bounds(curr_state, row_temp, col_temp) and not curr_state[row_temp][col_temp].is_wall():
            if curr_state[row_temp][col_temp].is_bulb():
                return False
            row_temp, col_temp = row_temp + x_direct, col_temp + y_direct


    # Iterate through each cell in the current state
    for row in range(len(curr_state)):
        for col in range(len(curr_state[row])):
            if curr_state[row][col].is_bulb():
                directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
                for x_direct, y_direct in directions:
                    row_temp, col_temp = row + x_direct, col + y_direct
                    while is_in_bounds(curr_state, row_temp, col_temp) and not curr_state[row_temp][col_temp].is_wall():
                        if curr_state[row_temp][col_temp].is_empty():
                            curr_state[row_temp][col_temp].set_cell_value(CellState.LIGHT)


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


# Given the position of a bulb, count the number of cells that bulb can light up
# and return this number
def num_cells_light(curr_state, cell):
    """
    :param curr_state: the current state of the puzzle
    :param cell: [row, col] the coordinate of the given cell
    :return: Number of cells the bulb at cell can light up
    """
    count = 0
    row = cell[0]
    col = cell[1]
    upper_row = row - 1
    lower_row = row + 1
    col_left = col - 1
    col_right = col + 1

    # Light up the puzzle
    light_up_puzzle(curr_state)

    # Going up
    while upper_row >= 0 and curr_state[upper_row][col] in [CellState.EMPTY]:
        if curr_state[upper_row][col] == CellState.EMPTY:
            count += 1
        upper_row -= 1

    # Going down
    while lower_row < len(curr_state) and curr_state[lower_row][col] in [CellState.EMPTY]:
        if curr_state[lower_row][col] == CellState.EMPTY:
            count += 1
        lower_row += 1

    # To the left
    while col_left >= 0 and curr_state[row][col_left] in [CellState.EMPTY]:
        if curr_state[row][col_left] == CellState.EMPTY:
            count += 1
        col_left -= 1

    # To the right
    while col_right < len(curr_state[0]) and curr_state[row][col_right] in [CellState.EMPTY, CellState.LIGHT]:
        if curr_state[row][col_right] == CellState.EMPTY:
            count += 1
        col_right += 1

    # Unlit the puzzle to return it to the original state
    unlit_puzzle(curr_state)
    return count


def count_adjacent_bulbs(puzzle, row, col):
    # count adjacent lights if a cell with a number
    # Only used to check cells with number - WALL
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


def num_adjacent_walls(puzzle, cell):
    # count how many walls surround the given cell [row, col]
    num_walls = 0
    row = cell[0]
    col = cell[1]
    rows = len(puzzle)
    cols = len(puzzle)

    if row > 0 and puzzle[row - 1][col].isdigit():  # down
        num_walls += 1
    if row < rows - 1 and puzzle[row + 1][col].isdigit():  # up
        num_walls += 1
    if col > 0 and puzzle[row][col - 1].isdigit():  # left
        num_walls += 1
    if col < cols - 1 and puzzle[row][col + 1].isdigit():  # right
        num_walls += 1

    return num_walls


def edge_corner_constraints(puzzle, cell):
    """
    Check if the given cell (row, col) is in edge/corner
        - not an edge/corner = 0 (no constraint)
        - edge = 1
        - corner = 2
    :return: its constraint level
    """
    constraints = 0
    row = cell[0]
    col = cell[1]
    rows = len(puzzle)
    cols = len(puzzle)

    if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:  # edge
        constraints = 1

    if (row == 0 or row == rows - 1) and (col == 0 or col == cols - 1):  # corner
        constraints = 2

    return constraints


def neighbor_constraints(puzzle, cell):
    """
    Check how many neighbors of the given cell (row, col) is lit up out of 4 of them
    :param puzzle: the current state of the puzzle
    :param cell: [row, col] - coordinate of the given cell
    :return: the number of neighbors that are lit up
    """
    constraints = 0
    row = cell[0]
    col = cell[1]
    rows = len(puzzle)
    cols = len(puzzle)

    light_up_puzzle(puzzle)

    if row > 0 and puzzle[row - 1][col] == CellState.LIGHT:  # down
        constraints += 1

    if row < rows - 1 and puzzle[row + 1][col] == CellState.LIGHT:  # up
        constraints += 1

    if col > 0 and puzzle[row][col - 1] == CellState.LIGHT:  # left
        constraints += 1

    if col < cols - 1 and puzzle[row][col + 1] == CellState.LIGHT:  # right
        constraints += 1

    unlit_puzzle(puzzle)
    return constraints


# Return True if map is lit up entirely, False otherwise
def is_map_lit_entirely(curr_state):
    """
    :param curr_state: List[List[str]] - the puzzle
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


def is_in_bounds(curr_state, row, col):
    """
    Check if a given position [row, col] is inside the current puzzle
    :param curr_state: List[List[Cell]] - the current state of the puzzle
    :param row: int - the row number of the cell
    :param col: int - the col number of the cell
    :return: bool
    """

    return 0 <= row < len(curr_state) and 0 <= col < len(curr_state[0])


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


def is_solved(curr_state):
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


