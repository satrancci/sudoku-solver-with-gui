import pygame as pg
from pygame.locals import RESIZABLE
from sudoku_solver import Sudoku
from matrices import matrices
from random import randint
from copy import deepcopy

SIZE_X = 450 # window size

BLACK = (0,0,0)
WHITE = (255, 255, 255) 
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 128) 

################################################ Utils

def generate_matrix(matrices):
    matrix = matrices[randint(0,len(matrices)-1)] # get a random matrix
    return matrix

#################################################

class SudokuUI:

    BOARD_SIZE = 9

    def __init__(self, size, matrix):
        self._size_x = size # window size
        self._size_y = self._size_x
        self._block_size = self._size_x/9 # cell
        self.sudoku_solver = Sudoku(matrix)
        pg.init()
        pg.display.set_caption("Sudoku Solver")
        self._window = pg.display.set_mode((self._size_x, self._size_y), RESIZABLE)
        self._window.fill(WHITE)
        self.prepare_board()
        self.clicked = None
        self.key = None
        self.delete = False
        self.simulate = False

    def clear_window(self):
        self._window.fill(WHITE)

    def clear_cell(self, y, x):
        cell_rect = pg.Rect(x*self._block_size+self._block_size*0.1, y*self._block_size+self._block_size*0.1, self._block_size*0.8, self._block_size*0.8)
        self._window.fill(WHITE, cell_rect)

    def draw(self, x, y, color=BLUE):
        font = pg.font.Font('freesansbold.ttf', int(self._block_size*0.6))
        submatrix_rect = pg.Rect(x*(self._block_size*3), y*(self._block_size*3), self._block_size*3, self._block_size*3)
        pg.draw.rect(self._window, BLACK, submatrix_rect, int(self._block_size/10))
        cell_rect = pg.Rect(x*self._block_size, y*self._block_size, self._block_size, self._block_size)
        pg.draw.rect(self._window, (0,0,0), cell_rect, 1)
        val = self.sudoku_solver.get_cell(x,y)
        val = val if val != '.' else ''
        #print('color:', color, 'x:', x, 'y:', y, 'val:', val)
        text = font.render(val, True, color)
        textRect = text.get_rect()
        textRect.center = (self._block_size/2+(self._block_size*y), self._block_size/2+(self._block_size*x))
        self._window.blit(text, textRect)
        pg.display.update()

    def prepare_board(self):
        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):         
                self.draw(x, y)
        pg.display.update()
                
    def click(self, pos):
        if pos[0] < self._size_x and pos[1] < self._size_y:
            x = pos[0] // self._block_size
            y = pos[1] // self._block_size
            return (int(y),int(x))

    def solve(self):
        return self.sudoku_solver.solve()

    def revert(self, matrix):
        self.sudoku_solver.reset_board(matrix)
    
    def make_backup(self):
        return self.sudoku_solver.make_backup()
    
    def place(self, x, y, num):
        self.sudoku_solver.place_cell(x,y,num)
    
    def remove(self, x, y):
        self.sudoku_solver.remove_cell(x,y)

    def play(self):
        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    self.clicked = self.click(pos)
                else:
                    self.clicked = False

                if event.type == pg.KEYDOWN:
                    keys = pg.key.get_pressed()
                    if keys[pg.K_1] or keys[pg.K_KP1]:
                        self.key = '1'
                    if keys[pg.K_2] or keys[pg.K_KP2]:
                        self.key = '2'
                    if keys[pg.K_3] or keys[pg.K_KP3]:
                        self.key = '3'
                    if keys[pg.K_4] or keys[pg.K_KP4]:
                        self.key = '4'
                    if keys[pg.K_5] or keys[pg.K_KP5]:
                        self.key = '5'
                    if keys[pg.K_6] or keys[pg.K_KP6]:
                        self.key = '6'
                    if keys[pg.K_7] or keys[pg.K_KP7]:
                        self.key = '7'
                    if keys[pg.K_8] or keys[pg.K_KP8]:
                        self.key = '8'
                    if keys[pg.K_9] or keys[pg.K_KP9]:
                        self.key = '9'

                    if keys[pg.K_SPACE]:
                        self.simulate = True
                    else:
                        self.simulate = False
                    
                    if keys[pg.K_DELETE] or keys[pg.K_BACKSPACE] or keys[pg.K_d]:
                        self.delete = True
                    else:
                        self.delete = False

            if self.simulate:
                print('\nTrying to solve....')
                current_matrix = self.make_backup()
                can_solve = self.solve()
                #print('Can solve:', can_solve)
                if not can_solve:
                    self.revert(current_matrix)
                    print('\nThe position cannot be solved. Remove elements from arbitrary cells and try again.')
                else:
                    self.clear_window()
                    self.prepare_board()
                    pg.display.update()
                    run = False
                self.simulate = False
                pg.display.update()

            if self.delete:        
                if self.clicked:
                    #print('val before removing:', self.sudoku_solver.get_cell(self.clicked[0],self.clicked[1]))
                    self.remove(self.clicked[0], self.clicked[1])
                    #print('val after removing:', self.sudoku_solver.get_cell(self.clicked[0],self.clicked[1]))
                    self.clear_cell(self.clicked[0], self.clicked[1])
                    self.draw(self.clicked[0], self.clicked[1])
                    self.delete = False
                    #[print(row) for row in self.sudoku_solver._matrix]
                    pg.display.update()

            if self.key:
                if self.clicked:
                    #print('self.clicked:', self.clicked, 'self.key:', self.key)
                    is_valid_placement = self.sudoku_solver.is_valid(self.clicked[0], self.clicked[1], self.key)

                    self.clear_cell(self.clicked[0], self.clicked[1])
                    self.place(self.clicked[0], self.clicked[1], self.key)
                    self.draw(self.clicked[0], self.clicked[1])
                    pg.display.update()

                    if not is_valid_placement:
                        self.clear_cell(self.clicked[0], self.clicked[1])
                        self.draw(self.clicked[0], self.clicked[1], RED)
                        pg.display.update()
                        self.delete = True
                        print(f"\nThe placement of {self.key} on ({self.clicked[0]},{self.clicked[1]}) is invalid. Please remove current element and try something else")
                        #[print(row) for row in self.sudoku_solver._matrix]
                    else:   
                        current_matrix = self.make_backup()
                        can_solve = self.solve()
                        #print('Can solve:', can_solve)
                        self.revert(current_matrix) 
                        if not can_solve:         
                            self.clear_cell(self.clicked[0], self.clicked[1])
                            self.draw(self.clicked[0], self.clicked[1], RED)
                            pg.display.update()
                            self.delete = True
                            print ('\nThe cell is valid, BUT the position CANNOT be solved from here. Please remove current element and try something else')
                            #[print(row) for row in self.sudoku_solver._matrix]
                        else:
                            if self.sudoku_solver.is_full():       
                                print("\nWOW, you've solved it!")
                                run = False
                            else:
                                print('\nThe cell is valid AND you CAN solve from here on. Good job!')
                    self.clicked = False
                    self.key = None
            pg.display.update()


 #####################################################
              
if __name__ == '__main__':

    play = True
    while play:
        matrix = deepcopy(generate_matrix(matrices)) # use deepcopy to be able to reuse the same matrix for next games!
        sudoku = SudokuUI(SIZE_X, matrix)
        pg.time.wait(3000) # display solution to the previous puzzle
        sudoku.play()
        play = int(input('\nDo you want to play another game? Press 1 for YES and 0 for NO: '))
        print("\n OK, let's play more!")
    print('Thanks, bye!')

    pg.quit()

