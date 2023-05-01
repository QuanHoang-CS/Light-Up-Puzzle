from utils import *


def most_constraining_variable_heuristic(curr_state, list_of_empty_cells):
    """
    The most constraining cell: the cell that causes most reduction in options for other cells.
    Found the most constraining cell by counting the number of cell a given cell can light up.
    Given the puzzle's current state and a list of empty cells, return the most constraining cell(s).

    :param curr_state: List[List[Cell]] - Current state of the puzzle
    :param list_of_empty_cells: List[List[int]] - List of positions of empty cells
    :return: List[List[int]] - List of position(s) of most constraining cell(s)
    """

    most_constraining_cells = []
    max_count  = 0

    for position in list_of_empty_cells:
        row, col = position[0], position[1]
        potential_cells_lighten_up = num_cells_lighten(curr_state, row, col) # Count potential lighten cells
        if potential_cells_lighten_up > max_count:
            most_constraining_cells = [position]
            max_count = potential_cells_lighten_up
        elif potential_cells_lighten_up == max_count:
            most_constraining_cells.append(position)

    return most_constraining_cells


def most_constrained_variable_heuristic(curr_state, list_of_empty_cells):
    """
    Find most constrained: Select the cell/node with the least remaining options as the next move based on:
        + The number of walls surrounding the cell.
        + If the cell is on and edge, or in a corner.

    :param curr_state: List[List[Cell]] - Current state of the puzzle
    :param list_of_empty_cells: List[List[int]] - List of positions of empty cells
    :return: List[List[int]] - List of position(s) of most constrained cell(s)
    """

    most_constrained_cells = []
    max_constrained = 0

    for position in list_of_empty_cells:
        row, col = position[0], position[1]
        adjacent_walls = count_adjacent_walls(curr_state, row, col) # Count the # of walls around a cell
        location_constraints = edge_corner_constraints(curr_state, row, col)  # check the location constraints

        constrained_index = adjacent_walls + location_constraints

        if max_constrained < constrained_index:
            most_constrained_cells = [position]
        elif max_constrained == constrained_index:
            most_constrained_cells.append(position)

    return most_constrained_cells


def hybrid_heuristic(curr_state, list_of_empty_cells):
    """
    Get The list of candidate(s) by:
        + Applying most_constrained_variable heuristic first,
        + then apply most_constraining_variable heuristic on the result to get the final list.

    :param curr_state: List[List[Cell]] - Current state of the puzzle
    :param list_of_empty_cells: List[List[int]] - List of positions of empty cells
    :return: List[List[int]] - List of cells to choose next
    """

    candidate_cells = most_constrained_variable_heuristic(curr_state, list_of_empty_cells)

    if len(candidate_cells) > 1:
        candidate_cells = most_constraining_variable_heuristic(curr_state, candidate_cells)

    return candidate_cells
