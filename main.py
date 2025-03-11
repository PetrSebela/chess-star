import math


class Cell:
    g_cost = 0
    h_cost = 0
    f_cost = 0

    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent

    def __eq__(self, other):
        if type(other) != Cell:
            return False
        return self.x == other.x and self.y == other.y
    

    def get_pos_str(self):
        return f"[{self.x},{self.y}]"
    

    def __str__(self):
        parent_pos = "NULL" if self.parent == None else self.parent.get_pos_str()
        return f"({self.get_pos_str()}, {parent_pos}, {self.g_cost}, {self.h_cost}, {self.f_cost})"


KNIGHT_MOVES = [
    (-1, -2),
    (1, -2),
    (-2, -1),
    (2, -1),
    (-2, 1),
    (2, 1),
    (-1, 2),
    (1, 2),
]


class ChessStar:
    def __init__(self, start: Cell, finish: Cell):
        self.start = start
        self.finish = finish
        self.opened = [start]
        self.closed = []
        self.step()

    def get_g_cost(self, old_cell):
        return old_cell.g_cost + 1

    def get_h_cost(self, new_cell):
        x_cost = math.ceil(abs(new_cell.x - self.finish.x) / 2)
        y_cost = math.ceil(abs(new_cell.y - self.finish.y) / 2)
        return max(x_cost, y_cost)


    def step(self, max_depth=5):
        if(max_depth <= 0):
            return
        
        best = min(self.opened, key=lambda cell: cell.f_cost) 
        self.expand(best)

        next = min(self.opened, key=lambda cell: cell.f_cost) 

        print("Opened: " + ";".join(str(x) for x in self.opened))
        print("Closed: " +";".join(str(x) for x in self.closed))
        self.show_board()


        if next == self.finish:
            path = []
            current = next
            while current != None:
                path.append(current)
                current = current.parent

            print([str(x) for x in path[::-1]])
            return

        self.step(max_depth-1)

    def expand(self, cell):
        for move in KNIGHT_MOVES[::-1]:
            next_cell = Cell(move[0] + cell.x, move[1] + cell.y, cell)
            if not ChessStar.is_valid(next_cell):
                continue

            if next_cell in self.closed:
                continue

            next_cell.g_cost = self.get_g_cost(next_cell)
            next_cell.h_cost = self.get_h_cost(next_cell)
            next_cell.f_cost = next_cell.g_cost + next_cell.h_cost

            if next_cell in self.opened:
                for existing in self.opened.copy():
                    if next_cell == existing:
                        if next_cell.f_cost < existing.f_cost:
                            self.opened.remove(existing)
                            self.opened.insert(0, next_cell)
            else:
                self.opened.insert(0, next_cell)

        self.opened.remove(cell)
        self.closed.append(cell)

    def is_valid(cell):
        return cell.x >= 0 and cell.x < 8 and cell.y >= 0 and cell.y < 8
    
    def show_board(self):
        def get_repr(cell):
            if cell == self.start:
                return " S "
            
            if cell == self.finish:
                return " T "
            
            if cell in self.opened:
                return " o "

            if cell in self.closed:
                return " x "

            return "   "
            
        for row_index in range(0,8):
            columns = [get_repr(Cell(x, row_index)) for x in range(0,8)]
            print("|".join(columns))
            if(row_index) >= 7:
                continue
            print("+".join(["---" for x in range(0,8)]))
        


if __name__ == "__main__":
    start = Cell(0,4)
    finish = Cell(5,4)
    solver = ChessStar(start, finish)
