from collections import deque
from queue import PriorityQueue

def solvable(board):
    """
    Determines if a board configuration is solvable based on its inversion count.
    """
    # Flatten the grid into a single list, skipping the empty space (0)
    flat = []
    inversions = 0

    for row in board.grid:
        for val in row:
            if val != 0:
                flat.append(val)
    
    # Compare each number with every number that comes after it, total is 8 since we removed 0
    for i in range(8):
        for j in range(i + 1, 8):
            if flat[i] > flat[j]:
                inversions += 1
                
    return inversions % 2 == 0

def ids(board):
    """
    Iterative deepening search: depth-first search with a depth limit
    solution must be checked first before running this, or else it will result in an infinite loop

    @param board: the starting board
    @return: (solved_board, nodes_expanded, max_depth)
    """
    max_depth = 0
    nodes_expanded = 0
    
    while True:
        stack = []
        stack.append((board, 0))    # (board, depth)

        # Store the vistied grids as a dict with the depth as value
        # so it can check that if it finds the same node with a lower depth
        visited = {board.grid : 0}

        while stack:
            brd, depth = stack.pop()
            nodes_expanded += 1

            # A shorter path was already found and was popped or currently sitting in the stack
            # since repetition can occur in the stack since we insert a repeated node if it has a lower depth
            if depth > visited[brd.grid]:
                continue 

            if brd.check_solved():
                return (brd, nodes_expanded, max_depth)

            new_depth = depth+1

            for state in brd.get_next_states():
                # Checkes if the new node is <= max_depth (check is only useful in the case of a new node not in visited dict)
                if new_depth <= max_depth:

                    # Push if new or if we reached it faster than before 
                    # instead of updating the node in the stack, we push them both and skip the higher depth one
                    if state.grid not in visited or visited[state.grid] > new_depth:
                        visited[state.grid] = new_depth
                        stack.append((state, new_depth))
        max_depth += 1

def bfs(board):
    """
    Breadth first search: explores the board level by level

    @param board: the starting board
    @return: the solved board with the fewest moves (optimal) or False if there is no solution
    """
    q = deque()
    q.append((board, 0))    # (board, depth)
    nodes_expanded = 0
    max_depth = 0

    visited = set()
    visited.add(board.grid)

    while q:
        brd, depth = q.popleft()
        nodes_expanded += 1
        max_depth = max(max_depth, depth)

        if (brd.check_solved()):
            return (brd, nodes_expanded, max_depth)

        for state in brd.get_next_states():
            if state.grid not in visited:
                visited.add(state.grid)
                q.append((state, depth+1))
    return (False, 0, 0)

def dfs(board):
    """
    Depth-first search keeps going down one path before trying others

    @param board: the starting board
    @return: (solved_board, nodes_expanded, max_depth) or False if there is no solution
    """

    stack = []
    stack.append((board, 0))    # (board, depth)
    visited = {board.grid}
    nodes_expanded = 0
    max_depth = 0

    while stack:
        brd, depth = stack.pop()
        nodes_expanded += 1
        max_depth = max(max_depth, depth)

        if (brd.check_solved()):
            return (brd, nodes_expanded, max_depth)

        for state in brd.get_next_states():
            if state.grid not in visited:
                visited.add(state.grid)
                stack.append((state, depth+1))
    return (False, 0, 0)


def astar(board, heuristic):
    """
    A* search: always expands the board with the lowest cost
    where cost = moves so far g(x) (depth) + heuristic h(x)

    @param board: the starting board
    @param heuristic: estimated moves to the goal
    @return: (solved_board, nodes_expanded, max_depth) or False if there is no solution
    """
    q = PriorityQueue()
    tie_breaker = 1                                  # Tie breaker so the queue never has to compare boards
    q.put((heuristic(board), tie_breaker, 0, board)) # (tota_score, tie, cost, board)

    # Store the visited grids as a dict with the cost (same thing as depth)
    # so it can check that if it finds the same node with a lower depth
    visited = {board.grid: 0}
    nodes_expanded = 0
    max_depth = 0

    while not q.empty():
        _, _, cost, brd = q.get()
        nodes_expanded += 1
        max_depth = max(max_depth, cost)

        # A better path was already found (same thing as the IDS code)
        if cost != visited[brd.grid]:
            continue

        if brd.check_solved():
            return (brd, nodes_expanded, max_depth)

        new_cost = cost + 1
        for state in brd.get_next_states():
            # only queue it if this path is shorter than any seen before
            # we push repeated nodes and skip the old ones (same thing as the IDS code)
            if state.grid not in visited or new_cost < visited[state.grid]:
                tie_breaker += 1
                visited[state.grid] = new_cost
                new_total = new_cost + heuristic(state)
                q.put((new_total, tie_breaker, new_cost, state))
    return (False, 0, 0)