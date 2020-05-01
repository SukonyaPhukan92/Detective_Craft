from tkinter import *
from tkinter import ttk
from random import random
from functools import partial

class MineField:
    """Manages a map of the field. Where mines are, which spaces have been discovered and flagged.

    Convention for field array:
        '.' = no mines, has not been stepped upon or marked
        0-8 = Had been stepped on. Value is number of adjacent squares containing mines
        'x' = mine
    """

    def __init__(self, content, width=10, height=10, mines=10):
        self.width = width
        self.height = height
        self.mines = mines
        self.content = content
        self.cellcolors = {'0': 'black', '1': 'blue', '2': 'purple', '3': 'orange', '4': 'red', '5': 'brown',
                           '6': 'yellow', 'F': 'dark green', 'X': 'red'}

        for key, value in self.cellcolors.items():
            ttk.Style().configure(value + ".TButton", foreground=value)

        # Layout is: field[row][col]
        self.field = [['.' for x in range(self.width)] for x in range(self.height)]

        # Set the mines
        assert (self.mines < self.width * self.height), "Too many mines for field to accommodate"

        # Populate mines
        mines_sown = 0
        row = col = 0
        chance = float(self.mines) / (self.width * self.height)

        while mines_sown < self.mines:
            # Roll the die
            if random() < chance:
                if self.field[row][col] is not 'x':
                    self.field[row][col] = 'x'
                    mines_sown += 1

            col += 1
            if self.width == col:
                col = 0
                row += 1

                if self.height == row:
                    row = 0

        # Create the squares
        self.minefieldbuttons = []
        
        # row, col layout
        for y in range(height):
            new = []
            for x in range(width):
                new.append(ttk.Button(content, width=3))
            self.minefieldbuttons.append(new)
        
        for y in range(height):
            for x in range(width):
                self.minefieldbuttons[y][x].grid(column=x, row=y, sticky=(N, S, E, W), padx=0, pady=0)
                self.minefieldbuttons[y][x].bind("<Button-1>", partial(self.step, y, x))
                self.minefieldbuttons[y][x].bind("<Button-3>", partial(self.mark, y, x))

      
    def print_field(self):
        for row in range(self.height):
            text = ""
            for col in range(self.width):
                text = text + str(self.field[row][col])
            print(text)

    def step(self, row, col, event):
        "Here goes..."
        if 'x' == self.field[row][col]:
            print("You hit a mine!")
            self.exposebutton(row, col, "X")
            self.show_mines()
            #
            # Game over!
            #
            # Show remaining mines
            return True

        if '.' == self.field[row][col]:
            self.field[row][col] = self.count_neighbouring_mines(row, col)
            self.exposebutton(row, col)

            if 0 == self.field[row][col]:
                self.explore_further(row, col)
                self.print_field()

        # Every square trodden?
        remaining_spaces = 0
        for y in range(self.height):
            for x in range(self.width):
                if ('.' == self.field[y][x]) or ('x' == self.field[y][x]):
                    remaining_spaces += 1

        print ("Remaining spaces: %d" % remaining_spaces)

        if remaining_spaces == self.mines:
            print("You win!")
            self.show_mines()

        return False

    def show_mines(self):
        for y in range(self.height):
            for x in range(self.width):
                if ('x' == self.field[y][x]):
                    self.exposebutton(row=y, col=x, value="X")

    def mark(self, row, col, event):
        if ('.' == self.field[row][col]) or ('x' == self.field[row][col]):
            if self.minefieldbuttons[row][col]["text"] == "":
                self.exposebutton(row, col, 'F')
            else:
                self.minefieldbuttons[row][col].config(text="")

    def count_neighbouring_mines(self, row, col):
        mine_count = 0

        mine_count += self.mine_in_cell(row - 1, col - 1)
        mine_count += self.mine_in_cell(row - 1, col)
        mine_count += self.mine_in_cell(row - 1, col + 1)

        mine_count += self.mine_in_cell(row, col - 1)
        mine_count += self.mine_in_cell(row, col + 1)

        mine_count += self.mine_in_cell(row + 1, col - 1)
        mine_count += self.mine_in_cell(row + 1, col)
        mine_count += self.mine_in_cell(row + 1, col + 1)

        return mine_count

    def mine_in_cell(self, row, col):
        "Mainly an error checking function to see if row and col are valid"
        if (row < 0) or (row >= self.height) or (col < 0) or (col >= self.width):
            return 0

        if 'x' == self.field[row][col]:
            return 1

        return 0

    def explore_further(self, row, col):
        assert(0 == self.field[row][col]), "Can only explore from cells already marked as 0"

        if row > 0:
            self.map_area(row-1, col)

        if row < (self.height-1):
            self.map_area(row+1, col)

        if col > 0:
            self.map_area(row, col-1)

        if col < (self.width-1):
            self.map_area(row, col+1)

    def map_area(self, row, col):
        assert (((row < 0) or (row >= self.height) or (col < 0) or (col >= self.width)) is False), \
            "Can only explore cells within the grid (row=%d, col=%d, self.height=%d, self.width=%d)" \
            % (row, col, self.height, self.width)

        # Already explored cell
        if self.field[row][col] != '.':
            return

        self.field[row][col] = self.count_neighbouring_mines(row, col)
        self.exposebutton(row, col)
        #self.minefieldbuttons[row][col].config(text=str(self.field[row][col]), style="emptysquare.TButton")

        if 0 == self.field[row][col]:
            self.explore_further(row, col)

    def exposebutton(self, row, col, value=""):
    if value == "":
            value = str(self.field[row][col])

        styletext = self.cellcolors[value] + ".TButton"

        self.minefieldbuttons[row][col].config(text=value, style=styletext)

if __name__ == '__main__':
    root = Tk()

    content = ttk.Frame(root, padding=(3,3,12,12))
    frame = ttk.Frame(content, borderwidth=2, relief="sunken")

    content.grid(column=0, row=0, sticky=(N, S, E, W))

    mf = MineField(content, width=10, height=10, mines=10)

    root.mainloop()

