class Board:
    def __init__(self, rows, parent = None, move_done = (0, 0)):

        # The grid is stored as a tuple of tuples so it can be used in a visted map directly 
        # Because lists are unhashable but tuples are
        self.grid = tuple(tuple(row) for row in rows)

        # Storing the move done and parent from the previous state for path tracing
        self.move_done = move_done 
        self.parent = parent

        self.zero = (-1, -1)

        # Initilize a freq map to check for any repeated integers in the given grid
        exist = set()

        # Input check
        for i in range(3):
            for j in range(3):
                x = rows[i][j]

                # Check if the given grid has only non repeating integers from 0 to 8, thus having all the numbers 0 to 8
                if type(x) is not int or x > 8 or x < 0 or x in exist:
                    raise ValueError("Grid given is not allowed")

                # Store the zero index
                if x == 0:
                    self.zero = (i, j)

                exist.add(x)
        
    def print_board(self):
        for row in self.grid:
            for i in range(3):
                print(row[i], end=' ')
            print() 
        
    # Get all the allowed actions from the current state
    def get_moves(self):

        # Direction list: (dy, dx) -> (row_change, col_change)
        # (-1, 0): UP,  (0, -1): LEFT,  (1, 0): DOWN,  (0, 1): RIGHT
        directions = [
            (-1, 0), (0, -1),
            (1, 0), (0, 1)
        ]

        allowed = []
        y, x = self.zero

        for [dy, dx] in directions:
            nx = x + dx
            ny = y + dy

            # Check if the new zero location will be out of the grid (thus illegal) or not
            if 0 <= nx <= 2 and 0 <= ny <= 2:
                allowed.append((dy, dx)) 

        return allowed
    
    # Get all the next states from the current state
    def get_next_states(self):
        next_states = []
        allowed = self.get_moves()

        for direction in allowed:
            dy, dx = direction
            y, x = self.zero

            nx = x + dx
            ny = y + dy

            # Copy the current grid to a list to perform the action on it (because tuples are immutable)
            temp = list(list(row) for row in self.grid)
            temp[y][x], temp[ny][nx] = temp[ny][nx], temp[y][x]

            # Create a new board with the modified grid with the action, and the parent pointing to self (the current state)
            next_states.append(Board(temp, self, direction))

        return next_states
    
    # Goal check function
    def check_solved(self):
        target = (
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8)
        )

        return self.grid == target