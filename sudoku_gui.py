import pygame as pg
from pygame.locals import RESIZABLE
from sudoku_solver import Sudoku
from matrices import matrices
from random import randint

SIZE_X = 450 # window size

BLACK = (0,0,0)
WHITE = (255, 255, 255) 
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 128) 

################################################

class SudokuUI:

    BOARD_SIZE = 9

    def __init__(self, size, matrices):
        self._size_x = size # window size
        self._size_y = self._size_x
        self._block_size = self._size_x/9 # cell
        self._matrices = matrices
        self._window = pg.display.set_mode((self._size_x, self._size_y), RESIZABLE)
        self._window.fill(WHITE) # background color
        pg.display.set_caption("Sudoku Solver")
        pg.init()

    def generate_matrix(self):
        matrix = self._matrices[randint(0,len(self._matrices)-1)] # get a random matrix
        return matrix

    def prepare_board(self, matrix):
        font = pg.font.Font('freesansbold.ttf', int(self._block_size*0.6))
        for y in range(self.BOARD_SIZE):
            for x in range(self.BOARD_SIZE):         
                submatrix_rect = pg.Rect(x*(self._block_size*3), y*(self._block_size*3), self._block_size*3, self._block_size*3)
                pg.draw.rect(self._window, BLACK, submatrix_rect, int(self._block_size/10))
                cell_rect = pg.Rect(x*self._block_size, y*self._block_size, self._block_size, self._block_size)
                pg.draw.rect(self._window, (0,0,0), cell_rect, 1)

                text = font.render(matrix[x][y], True, BLUE)
                textRect = text.get_rect()
                textRect.center = (self._block_size/2+(self._block_size*x), self._block_size/2+(self._block_size*y))
                self._window.blit(text, textRect)

                pg.display.update()

    def play(self, matrix): # this function is not ready yet
        run = True
        while run:   
            for event in pg.event.get():
                if event.type == pg.QUIT: 
                    run = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    pass
                # other events ...
            pg.display.update()

    def solve(self, matrix):
        s = Sudoku(matrix)
        s.solve()
        self._window.fill((WHITE)) # clear the board
        return matrix # makes changes in-place
    
    def show(self, seconds=None): # display indefinitely if seconds not supplied
        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT: 
                    run = False
            pg.display.update()
            if seconds:
                pg.time.wait(seconds*1000)
                run = False


 #####################################################
              
if __name__ == '__main__':

    sudoku = SudokuUI(SIZE_X, matrices)
    matrix = sudoku.generate_matrix()
    sudoku.prepare_board(matrix)
    sudoku.show(3)
    sudoku.solve(matrix)
    sudoku.prepare_board(matrix)
    sudoku.show()

    pg.quit()

