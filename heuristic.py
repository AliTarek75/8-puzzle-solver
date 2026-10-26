from math import sqrt

# store the position that each number should end up in
goal_pos = {
    1: (0, 1),
    2: (0, 2),
    3: (1, 0),
    4: (1, 1),
    5: (1, 2),
    6: (2, 0),
    7: (2, 1),
    8: (2, 2)
}

def manhattan(board):
    """
    Calculates the total Manhattan distance of all tiles from their goal positions.
    """
    total = 0
    for i in range(3):
        for j in range(3):
            number = board.grid[i][j]

            if number != 0:
                goal_i, goal_j = goal_pos[number]
                total += abs(i - goal_i) + abs(j - goal_j)
    return total


def euclidean(board):
    """
    Calculates the total Euclidean distance of all tiles from their goal positions.
    """
    total = 0
    for i in range(3):
        for j in range(3):
            number = board.grid[i][j]

            if number != 0:
                goal_i, goal_j = goal_pos[number]
                total += sqrt((i - goal_i)**2 + (j - goal_j)**2)
    return total
