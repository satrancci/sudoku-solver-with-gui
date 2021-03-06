from copy import deepcopy

class Sudoku:

    BOARD_SIZE = 9

    def __init__(self, matrix):
        self._matrix = matrix
    
    ####################### Methods that solve sudoku ############################

    def is_full(self):
        return False if any(self._matrix[i][j] == '.' for i in range(self.BOARD_SIZE) for j in range(self.BOARD_SIZE)) else True

    def is_valid(self, x, y, num):
        for i in range(self.BOARD_SIZE):
            if self._matrix[x][i] == num or self._matrix[i][y] == num or self._matrix[3*(x//3)+i//3][3*(y//3)+i%3] == num:
                return False
        return True
    
    def solve(self):
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self._matrix[i][j] == '.': # if a cell is empty,
                    for num in range (1,10): # try every number
                        if self.is_valid(i,j,str(num)): # if we can place the current number,
                            self._matrix[i][j] = str(num) # we place it
                            if self.solve(): # if we can solve the problem recursively,
                                return True # then we are done
                            self._matrix[i][j] = '.' # otherwise, we set the current cell to empty (backtrack)
                        if num == 9: # if we tried all numbers for this cell and still didn't solve it,
                            return False # then there is no solution and we need to backtrack to make changes in earlier cells

        return self.is_full()

    #################### Methods that facilitate GUI implementation ################################

    def get_cell(self, x, y):
        return self._matrix[x][y]
    
    def place_cell(self, x, y, num):
        self._matrix[x][y] = num

    def remove_cell(self, x, y):
        self._matrix[x][y] = '.'

    def reset_board(self, matrix):
        self._matrix = matrix
    
    def make_backup(self):
        matrix = deepcopy(self._matrix)
        return matrix