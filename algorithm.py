from collections import deque
from queue import PriorityQueue

def ids(board):
    """
    Iterative deepening search: depth-first search with a depth limit

    @param board: the starting board
    @return: the solved board
    """
    max_depth = 0
    while True:
        stack = []
        stack.append((board, 0))    # (board, depth)

        # Store the visited grids as a dict with the depth as value
        # so it can check that if it finds the same node with a lower depth
        visited = {board.grid : 0}
        needs_more = False

        while stack:
            brd, depth = stack.pop()

            # A shorter path was already found and was popped or currently setting in the stack
            # since repetition can occur in the stack since we insert a repeated node if it has a lower depth
            if depth > visited[brd.grid]:
                continue 

            if brd.check_solved():
                return brd

            new_depth = depth+1

            for state in brd.get_next_states():
                
                # Checkes if the new node is <= max_depth (check is only useful in the case of a new node not in vistied dict)
                if new_depth <= max_depth:

                    # Push if new or if we reached it faster than before 
                    # instead of updating the node in the stack, we push them both and skip the higher depth one
                    if state.grid not in visited or visited[state.grid] > new_depth:
                        visited[state.grid] = new_depth
                        stack.append((state, new_depth))

                # else it means that the new node is important and we need to do an extra depth to reach it
                elif state.grid not in visited:
                    needs_more = True

        if needs_more:
            max_depth += 1
            needs_more = False
        else:
            break


def bfs(board):
    """
    Breadth first search: explores the board level by level

    @param board: the starting board
    @return: the solved board with the fewest moves (optimal) or False if there is no solution
    """
    q = deque()
    q.append(board)

    visited = set()
    visited.add(board.grid)

    while q:
        brd = q.popleft()
        if (brd.check_solved()):
            return brd

        for state in brd.get_next_states():
            if state.grid not in visited:
                visited.add(state.grid)
                q.append(state)
    return False

def dfs(board):
    """
    Depth-first search: keeps going down one path before trying others

    @param board: the starting board
    @return: a solved board (any solution, not necessarily optimal) or False if there is no solution
    """

    stack = [board]
    visited = {board.grid}

    while stack:
        brd = stack.pop()
        if (brd.check_solved()):
            return brd

        for state in brd.get_next_states():
            if state.grid not in visited:
                visited.add(state.grid)
                stack.append(state)
    return False


def astar(board, heuristic):
    """
    A* search: always expands the board with the lowest cost
    where cost = moves so far g(x) (depth) + heuristic h(x)

    @param board: the starting board
    @param heuristic: estimated moves to the goal
    @return: the solved board or False if there is no solution
    """
    q = PriorityQueue()
    id = 1                                  # tie breaker so the queue never has to compare boards
    q.put((heuristic(board), id, 0, board)) # (cost, tie, depth, board)
    best_depth = {board.grid: 0}

    while not q.empty():
        _, _, depth, brd = q.get()

        # a better path to this state was found
        if depth != best_depth[brd.grid]:
            continue

        if brd.check_solved():
            return brd

        new_depth = depth + 1
        for state in brd.get_next_states():
            # only queue it if this path is shorter than any seen before
            if ((state.grid not in best_depth) or (new_depth < best_depth[state.grid])):
                id += 1
                best_depth[state.grid] = new_depth
                new_cost = new_depth + heuristic(state)
                q.put((new_cost, id,new_depth, state))
    return False