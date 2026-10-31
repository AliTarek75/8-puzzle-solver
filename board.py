class Board:
    
    # Direction list: (dy, dx) -> (row_change, col_change)
    directions = (
        (-1, 0),  # UP
        (0, -1),  # LEFT
        (1, 0),   # DOWN
        (0, 1),    # RIGHT
    )

    def __init__(self, rows, parent = None, move_done = (0, 0), trusted_zero_pos = None):

        # Storing the move done and parent from the previous state for path tracing
        self.move_done = move_done 
        self.parent = parent

        # trusted_zero_pos is flag that indicates the Borad was initilized internally from the search algortihms
        # instead of the user, it works as a flag and as the zero position at the same time.
        # it is used to skip board validation, skip finding the zero, and it trusts that the given board is already a tuple
        if not trusted_zero_pos:
            self.grid = tuple(tuple(row) for row in rows)
        
            # Initilize a freq map to check for any repeated integers in the given grid
            exist = set()

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
        else:
            self.zero = trusted_zero_pos
            self.grid = rows

    def print_board(self):
        """
        Prints the grid to the console for testing and debugging.
        """
        for row in self.grid:
            for i in range(3):
                print(row[i], end=' ')
            print()
    
    def get_next_states(self):
        """
        Generates a list of all valid adjacent Board states resulting from legal moves.
        """
        next_states = []
        y, x = self.zero

        for dy, dx in self.directions:
            ny = y + dy
            nx = x + dx

            # Check if the new zero location will be out of the grid (thus illegal) or not
            if 0 <= ny <= 2 and 0 <= nx <= 2:

                # Optimization: shallow copy the outer tuple into a list, and change the necessary things only
                # A lot of the parent-children relationship have shallow copied parts of the board
                # since they are tuples and cannot be changed without creating a new copy
                temp = list(self.grid)

                # Horizontal move: only one row changes
                if ny == y:  
                    # copy the required row, then turn it back into a tuple
                    row = list(self.grid[y])
                    row[x], row[nx] = row[nx], row[x]
                    temp[y] = tuple(row)

                # Vertical move: two rows change
                else:  
                    # Copy the two required rows, swap the two elements, then turn back to tuples
                    row1 = list(self.grid[y])
                    row2 = list(self.grid[ny])
                    row1[x], row2[x] = row2[x], row1[x]
                    temp[y] = tuple(row1)
                    temp[ny] = tuple(row2)

                next_states.append(Board(tuple(temp), self, (dy, dx), (ny, nx)))

        return next_states
    
    def check_solved(self):
        """
        Checks if the current board grid perfectly matches the target goal configuration.
        """
        target = (
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8)
        )

        return self.grid == target