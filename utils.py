import os


# Enums
class CellState:
    BULB = 'b'
    EMPTY = '_'
    LIGHT = '*'


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
    # Iterate through each cell in the current state
    for row in range(len(curr_state)):
        for col in range(len(curr_state[row])):
            if curr_state[row][col] == CellState.BULB:
                # At the position of the light bulb, light up all
                travel_dist = 1
                # Light upward
                while row - travel_dist >= 0 and curr_state[row - travel_dist][col] in [CellState.EMPTY, CellState.LIGHT]:
                    curr_state[row - travel_dist][col] = CellState.LIGHT
                    travel_dist += 1

                travel_dist = 1
                # Light downward
                while row + travel_dist < len(curr_state) and curr_state[row + travel_dist][col] in [CellState.EMPTY, CellState.LIGHT]:
                    curr_state[row + travel_dist][col] = CellState.LIGHT
                    travel_dist += 1

                travel_dist = 1
                # Light leftward
                while col - travel_dist >= 0 and curr_state[row][col - travel_dist] in [CellState.EMPTY, CellState.LIGHT]:
                    curr_state[row][col - travel_dist] = CellState.LIGHT
                    travel_dist += 1

                travel_dist = 1
                # Light rightward
                while col + travel_dist < len(curr_state[row]) and curr_state[row][col + travel_dist] in [CellState.EMPTY, CellState.LIGHT]:
                    curr_state[row][col + travel_dist] = CellState.LIGHT
                    travel_dist += 1


# Removing all * symbols in current state.
def unlit_puzzle(curr_state):
    """
    :param curr_state: List[List[str]] - the puzzle
    """
    # Iterate through all cells to look for * symbol
    # if we see _, replace it with '_'
    for row in range(len(curr_state)):
        for col in range(len(curr_state[row])):
            if curr_state[row][col] == CellState.LIGHT:
                curr_state[row][col] = CellState.EMPTY


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


def num_adjacent_bulbs(puzzle, row, col):
    # count adjacent lights if a cell with a number
    # Only used to check cells with number - WALL
    count = 0
    rows = len(puzzle)
    cols = len(puzzle)

    if row > 0 and puzzle[row - 1][col] == CellState.BULB:  # down
        count += 1
    if row < rows - 1 and puzzle[row + 1][col] == CellState.BULB:  # up
        count += 1
    if col > 0 and puzzle[row][col - 1] == CellState.BULB:  # left
        count += 1
    if col < cols - 1 and puzzle[row][col + 1] == CellState.BULB:  # right
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

    # Iterate through all cells to look for _ symbol
    # if we  see _, solution is not complete
    for row in range(len(curr_state)):
        for col in range(len(curr_state[row])):
            if curr_state[row][col] == '_':
                is_lit_up = False

    unlit_puzzle(curr_state)
    return is_lit_up


# Check if a given cell is inside the current puzzle
def is_in_bounds(curr_state, cell, row, col):
    """
    :param curr_state: List[List[str]] - the puzzle
    :param row: int - the row number of the cell
    :param col: int - the col number of the cell
    :return: bool
    """
    row = cell[0]
    col = cell[1]
    return 0 <= row < len(curr_state) and 0 <= col < len(curr_state[0])


# Given a cell, check the surrounding to see if the bulb can be placed there
def is_valid_bulb(curr_state, row, col):
    """
    :param curr_state: List[List[str]] - the puzzle
    :param row: int - the row number of the cell
    :param col: int - the col number of the cell
    :return: bool
    """

    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    for x_direct, y_direct in directions:
        row_temp, col_temp = row + x_direct, col + y_direct
        while is_in_bounds(curr_state, row_temp, col_temp) and not curr_state[row_temp][col_temp].isdigit():
            if curr_state[row_temp][col_temp] == CellState.BULB:
                return False
            row_temp, col_temp = row_temp + x_direct, col_temp + y_direct

    return True


def is_solved(curr_state):
    rows = len(curr_state)
    cols = len(curr_state)

    for row in range(rows):
        for col in range(cols):
            if curr_state[row][col].isdigit() and int(curr_state[row][col]) != num_adjacent_bulbs(curr_state, row, col):
                return False
            if curr_state[row][col] == CellState.BULB and not is_valid_bulb(curr_state, row, col):
                return False

    is_all_light_up = is_map_lit_entirely(curr_state)

    return is_all_light_up


def is_state_valid(curr_state):
    rows = len(curr_state)
    cols = len(curr_state)

    for row in range(rows):
        for col in range(cols):
            if curr_state[row][col].isdigit() and int(curr_state[row][col]) < num_adjacent_bulbs(curr_state, row, col):
                return False
            if curr_state[row][col] == CellState.BULB and not is_valid_bulb(curr_state, row, col):
                return False

    return True


