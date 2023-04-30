from utils import *

def most_constraining_variable_heuristic(curr_state, list_of_empty_cells):
    """
    The most constraining cell: the cell that causes most reduction in options for other cells. Found by counting the number of cell a given cell can light up.
    Given the puzzle's current state and a list of empty cells, return the most constraining cell(s).

    :param curr_state: Current state of the puzzle
    :param list_of_empty_cells: List of coordinates of empty cells
    :return: List of most constraining cells
    """

    most_constraining_cells = []
    max_count  = 0

    for cell in list_of_empty_cells:
        potential_cells_lighten_up = num_cells_light(curr_state, cell) # Count potential lighten cells
        if potential_cells_lighten_up > max_count:
            most_constraining_cells = cell
            max_count = potential_cells_lighten_up
        elif potential_cells_lighten_up == max_count:
            most_constraining_cells.append(cell)

    return most_constraining_cells

def most_constrained_variable_heuristic(curr_state, list_of_empty_cells):
    """
    Find most constrained: Select the cell/node with the least remaining options as the next move based on:
        - number of walls surrounding the cell
        - if it is in middle or edge/corner
        - if its neighbor constraints (how many has been lit up?)

    :param curr_state: Current state of the puzzle
    :param list_of_empty_cells: List of coordinates of empty cells
    :return: List of most constrained cells
    """

    most_constrained_cells = []
    max_constrained = 0

    for cell in list_of_empty_cells:
        adjacent_walls = num_adjacent_walls(curr_state, cell)
        location_constraints = edge_corner_constraints(curr_state, cell)  # check the location constraints
        light_constraints = neighbor_constraints(curr_state, cell)

        constrained_index = adjacent_walls + location_constraints + light_constraints

        if max_constrained < constrained_index:
            most_constrained_cells = cell
        elif max_constrained == constrained_index:
            most_constrained_cells.append(cell)

    return most_constrained_cells

def hybrid_heuristic(curr_state, list_of_empty_cells):
    """
    Applying most_constrained_variable heuristic first, then apply most_constraining_variable heuristic on the result to get the final list
    :param curr_state: Current state of the puzzle
    :param list_of_empty_cells: List of coordinates of empty cells
    :return: List of cells to choose next
    """

    candidate_cells = most_constrained_variable_heuristic(curr_state, list_of_empty_cells)

    if len(candidate_cells) > 1:
        candidate_cells = most_constraining_variable_heuristic(curr_state, candidate_cells)

    return candidate_cells
