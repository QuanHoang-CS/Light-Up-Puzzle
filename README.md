# Light-Up-Puzzle

- Light-up puzzle (also known as Akari) is a grid puzzles developed by the company Nikoli first introduced in 2001.
- In this project, we implement a solver for the light-up puzzles using the following algorithms:
  - Back tracking
  - Forward checking
- **Heuristics**:
  - **Heuristic 1 (H1)**: Most Constrained Variable
      - The heuristic selects the node with the least remaining options as the next move. The idea behind this is that picking such a node will result in earlier backtracking. If multiple nodes have the same minimum number of options, then one of them is selected randomly. The criterias are:
        - number of walls surrounding the cell
        - if it is in middle or edge/corner
        - if its neighbor constraints (how many has been lit up?)
      
  - **Heuristic 2 (H2)**: Most Constraining Variable
      - The heuristic chooses the node that causes the most reduction in options for other nodes as the next step. In other words, it selects the node that imposes the greatest restrictions on other nodes. If there are multiple nodes with equal potential to limit other nodes, one is selected randomly. The criteria is:
        - Counting the num cells that (potential) bulb can light up - choose the maximum
  - **Heuristic 3 (H3)**: Hybrid
      - This heuristic will combine both H1 and H2.



### To run the program: 
- python algorithm_name.py -p input_name.txt -h heuristic
  - algorithm_name: backtrack, forward_checking
  - heuristics: H1, H2, H3
- Ex: python backtracking.py -p samples.txt -h H1
