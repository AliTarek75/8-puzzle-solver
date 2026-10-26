import tkinter as tk
import time
from board import Board
from algorithm import *
from heuristic import *

class GUI:

    # Default board on startup
    start_nums = [[1, 2, 5], [3, 4, 0], [6, 7, 8]]

    # The colors for empty and nonempty cells
    color_empty = "#d6d6d6"
    color_full = "white"
    color_main = "#0D1C42"
    color_main_second = "#22396F"

    # Direction translation for each specific move
    moves = {(-1, 0): "UP", (1, 0): "DOWN", (0, -1): "LEFT", (0, 1): "RIGHT", (0, 0): "START"}


    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        
        # Add padding to all four sides of the entire application window
        self.root.config(padx=30, pady=30)
        self.root.bind("<Return>", lambda event: self.solve_button.invoke())
        self.root.bind("<Control-v>", self.handle_paste)
        self.root.bind_all("<Button-1>", self.handle_bg_click)

        self.path = []
        self.moves_list = []
        self.root.minsize(350, 460)

        # 1. The 3x3 Editable Board
        board_frame = tk.Frame(root, bg=self.color_main, highlightcolor=self.color_main, highlightbackground=self.color_main, highlightthickness=1, bd=0)
        board_frame.pack(pady=10)
        
        self.cells = []
        
        for i in range(3):
            row_cells = []
            for j in range(3):
                cell = tk.Entry(
                    board_frame, width=3, font=("Arial", 36, "bold"), justify="center", fg = "black",
                    selectforeground="black",

                    # border for when selected
                    highlightthickness=1,
                    highlightcolor = "black",

                    # remove the 3d look
                    relief="flat", bd=0
                )
                cell.grid(row=i, column=j, padx=1, pady=1)
            
                # binds the keypress event to intercept any typed text and handle it correctly
                cell.bind("<KeyPress>", self.on_input_change)

                row_cells.append(cell)
            self.cells.append(row_cells)
        
        self.update_board(self.start_nums)

        # 2. Move Label & Slider
        self.move_label = tk.Label(root, text="Ready", font=("Arial", 14, "bold"))
        self.move_label.pack()

        self.slider = tk.Scale(
            root, from_=0, to=0, orient="horizontal", command=self.on_slide, showvalue=0, width=12, takefocus=True, length=220,

            # Colors when focused and clicked
            highlightcolor = "black",
            highlightthickness=1,
            activebackground=self.color_main_second,

            # Colors of the handle and rest of the slider
            bg=self.color_main,
            troughcolor=self.color_empty, 

            # Change the look of the slider to make it a solid color and remove the 3d look
            sliderrelief="flat", bd=0,

        )
        self.slider.pack(pady=10)

        # make it so that when the slider is clicked on using a mouse button it gets focused
        self.slider.bind("<Button-1>", lambda event: self.slider.focus_set())

        # 3. Metrics Label
        self.metrics = tk.Label(root, text="Type numbers directly into the cells. \n Select an algorithm and click Solve. ", font=("Arial", 12), justify="left")
        self.metrics.pack(pady=5)

        # 4. Algorithm Selector 
        dropdown_frame = tk.Frame(root)
        dropdown_frame.pack(pady=10)

        # map display names to their solver functions
        self.dropdown_map = {
            "BFS": lambda: self.solve(bfs),
            "DFS": lambda: self.solve(dfs),
            "IDS": lambda: self.solve(ids),
            "A* (Manhattan)": lambda: self.solve(astar, manhattan),
            "A* (Euclidean)": lambda: self.solve(astar, euclidean)
        }
        
        # variable fro the dropdown to store the selected algorithm
        self.dropdown_var = tk.StringVar(value="BFS")

        self.dropdown = tk.OptionMenu(dropdown_frame, self.dropdown_var, *self.dropdown_map.keys())
        self.dropdown.config(
            font=("Arial", 11), width=14, bg="white",

            # Change the look to give it a border with the main color and remove the 3d look
            highlightbackground=self.color_main,
            relief="flat", bd=0, indicatoron=False,
        )
        self.dropdown.config(font=("Arial", 11), width=15)
        self.dropdown.pack(side="left", padx=5)

        self.solve_button = tk.Button(
            dropdown_frame, text="Solve", font=("Arial", 11, "bold"), padx=12, pady=2,
            command=lambda: self.dropdown_map[self.dropdown_var.get()](),

            # change button background and text colors
            bg=self.color_main,  fg="white",
            activebackground=self.color_main_second,
            activeforeground="white",
            
            # remove the 3d look
            relief="flat", bd=0,
        )
        self.solve_button.pack(side="left", padx=5)
    

    # Handles when clicking anywhere, it checks if it's an element that doesn't need focus so it gives the focus to the root
    def handle_bg_click(self, event):
        # winfo_class() tells us what type of widget was clicked.
        # If it's the background, a frame, or a text label, steal the focus back.
        if event.widget.winfo_class() in ("Tk", "Frame", "Label"):
            self.root.focus_set()


    # Handles when pasting a board from the clipboard, it's bound to the root so this works anywhere
    def handle_paste(self, event):
        # get clipboard and remove spaces or next space
        clipboard = self.root.clipboard_get().replace(" ", "").replace("\n", "")

        # temporary grid to be changed later
        temp = [[0,0,0],[0,0,0],[0,0,0]]

        # check if the clipboard is a valid input by using the fact that order in sets doesn't matter
        if len(clipboard) == 9 and set(clipboard) == set("012345678"):
            for idx, char in enumerate(clipboard):
                r = idx//3
                c = idx%3

                temp[r][c] = int(char)
                
            self.update_board(temp)


    # custom behaviour for cells, using return "break" to stop default behaviour
    # the cells has a custom selectbackground (the text selection) and insertbackground (the vertical bar)
    # so their values are equal to the cell background itself (to make them disappear) and is different based on if its an empty cell or not
    def on_input_change(self, event):
        box = event.widget
        char = event.char

        # ignore tab and continue with default behaviour
        if event.keysym == "Tab":
            return

        # arrow key navigation between cells
        if event.keysym in ("Up", "Down", "Left", "Right"):
            info = box.grid_info()  # Get the current focus cell info from the grid layout
            r, c = info["row"], info["column"]

            # Get the next cell to be focused
            # up or down navigation
            if event.keysym == "Up" and r > 0: r -= 1
            elif event.keysym == "Down" and r < 2: r += 1

            # left or right navigation, when going outside the board it will go to the next/previous row
            if event.keysym == "Left":
                if c > 0:
                    c -= 1
                else:
                    c = 2
                    r = (r-1+3)%3
            elif event.keysym == "Right":
                if c < 2:
                    c += 1
                else:
                    c = 0
                    r = (r+1)%3

            self.cells[r][c].focus_set()
            return "break"
        
        # handle manual clearing by backspace or delete
        if event.keysym in ("BackSpace", "Delete"):
            box.delete(0, "end")
            box.config(bg=self.color_empty, insertbackground=self.color_empty, selectbackground=self.color_empty, highlightbackground=self.color_empty)
            return "break"

        # intercept any typed character
        if char:
            if char in "12345678":
                box.delete(0, "end")
                box.insert(0, char)
                box.config(bg=self.color_full, insertbackground=self.color_full, selectbackground=self.color_full, highlightbackground=self.color_full)
                return "break"
                
            elif char in ["0", " "]:
                box.delete(0, "end")
                box.config(bg=self.color_empty, insertbackground=self.color_empty, selectbackground=self.color_empty, highlightbackground=self.color_empty)
                return "break"
                
            else:
                # reject any other characters
                return "break"


    # Get the current board on the cells and return it as a Board object
    def get_current_board(self):
        rows = []
        for i in range(3):
            row = []
            for j in range(3):
                text = self.cells[i][j].get()

                # add the text in each cell as an integer and readd the 0 from the empty cell
                row.append(0 if text == "" else int(text))
            rows.append(row)
        return Board(rows)


    # Update the board cells with a specific grid
    def update_board(self, grid):
        for i in range(3):
            for j in range(3):
                val = grid[i][j]
                box = self.cells[i][j]
                
                box.delete(0, "end")
                if val != 0:
                    box.insert(0, str(val))
                    
                    # configure the background and other related cell behaviour based on the cell text
                    # since the empty cell has a different behaviour other than the rest
                    box.config(bg=self.color_full, insertbackground=self.color_full, selectbackground=self.color_full, highlightbackground=self.color_full)
                else:
                    box.config(bg=self.color_empty, insertbackground=self.color_empty, selectbackground=self.color_empty, highlightbackground=self.color_empty)


    # Solve the game based on the algortihm and any extra arguments (heuristics for A*)
    def solve(self, algo, *args):
        self.metrics.config(text="Solving...")

        # update label to show the "Solving..." text without having to wait for the function to end
        self.root.update()
        
        # test the current board (even though the cells has validation logic, but it doesn't test everything)
        try:
            start_board = self.get_current_board()
        except ValueError:
            self.metrics.config(text="  Error: Use numbers 1-8 \n and leave one box empty.")
            return

        if not solvable(start_board):
            self.metrics.config(text="No solution found for this board.")
            return

        self.move_label.config(text="Use arrows to step")

        t0 = time.time()
        res, exp, depth = algo(start_board, *args)
        t1 = time.time()

        # find the path by following the parent pointers
        self.path = []
        while res:
            self.path.append(res)
            res = res.parent
        self.path.reverse()
        
        cost = len(self.path)-1

        # the moves list (LEFT, UP...) takes every move_done from the solution and translates it into the direction
        self.moves_list = [self.moves[b.move_done] for b in self.path]
            
        self.metrics.config(text=f"Time: {t1-t0:.4f}s\t Cost: {cost}\nExpanded: {exp}\t Depth: {depth}")
        
        # configures the slider with the total cost path and resets it and sets it in focus 
        self.slider.config(to=cost)
        self.slider.set(0)
        self.slider.focus_set()


    # The slider function, it works by taking the current slider value as the index of the current node in the path list
    # and then updates the board with the node grid and the label with the direction
    def on_slide(self, val):

        # check if the self.path is empty (at the start of the app), so it doesn't try to access an empty list
        if not self.path:
            return
        
        idx = int(val)
        self.update_board(self.path[idx].grid)
        self.move_label.config(text=f"Step {idx}: {self.moves_list[idx]}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()