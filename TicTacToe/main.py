import copy
import random
import numpy as np

# Constants
ROWS = 3
COLS = 3

class Board:

    def __init__(self):
        self.sqrs = np.zeros((ROWS,COLS))
        self.moves_made = 0

    def print_board(self):
        for i in range(ROWS):
            for j in range(COLS):
                print(int(self.sqrs[i][j]),end=" ")
            print()

    def leftover_moves(self):
        lm = []

        for i in range(ROWS):
            for j in range(COLS):
                if self.is_valid(i, j):
                    lm.append((i,j))

        return lm
    
    def is_full(self):
        if self.moves_made == 9:
            return True
        return False
    
    def mark_move(self, i, j, plyr):
        self.sqrs[i][j] = plyr
        self.moves_made += 1

    def is_valid(self, i, j):
        if self.sqrs[i][j] == 0:
            return True
        return False
    
    def is_winner(self):
        for j in range(3):
            if self.sqrs[0][j] == self.sqrs[1][j] == self.sqrs[2][j] != 0:
                return self.sqrs[0][j]
        for i in range(3):
            if self.sqrs[i][0] == self.sqrs[i][1] == self.sqrs[i][2] != 0:
                return self.sqrs[i][0]   
        if self.sqrs[0][0] == self.sqrs[1][1] == self.sqrs[2][2] != 0:
            return self.sqrs[0][0]
        if self.sqrs[2][0] == self.sqrs[1][1] == self.sqrs[0][2] != 0:
            return self.sqrs[2][0]
        
        return -1


class AI:

    def __init__(self, plyr = 2):
        self.plyr = plyr

    def rnd_move(self, brd):
        lm = brd.leftover_moves()
        idx = random.randrange(0, len(lm))

        return lm[idx]
    
    def minimax(self, board, ismaximizing = False):

        state = board.is_winner()

        if state == 1:
            return 1, None
        
        if state == 2:
            return -1, None
        
        elif board.is_full():
            return 0, None
        
        if ismaximizing:
            alpha = -1000
            best = None
            nxt_move = board.leftover_moves()

            for (r, c) in nxt_move:
                tmp = copy.deepcopy(board)
                tmp.mark_move(r, c, 1)
                val = self.minimax(tmp, False)[0]

                if val > alpha:
                    alpha = val
                    best = (r, c)

               
            return alpha, best

        elif not ismaximizing:
            beta = 1000
            best = None
            nxt_move = board.leftover_moves()

            for (r, c) in nxt_move:
                tmp = copy.deepcopy(board)
                tmp.mark_move(r, c, self.plyr)
                val = self.minimax(tmp, True)[0]

                if val < beta:
                    beta = val
                    best = (r, c)

            return beta, best
    
    def nxt_move(self, brd):
        #move = self.rnd_move(brd)
        val, move = self.minimax(brd, False)

        return move
        

class Game:

    def __init__(self):
        self.board = Board()
        self.plyr = 1
        self.ai = AI()
        self.gameover = False

    def chng_plyr(self):
        self.plyr = self.plyr % 2 + 1

    def make_move(self, i, j):
        self.board.mark_move(i, j, self.plyr)
        self.chng_plyr()
        self.board.print_board()

    




def main():
    game = Game()
    board = game.board
    puter = game.ai

    board.print_board()
    while True:

        

        k = int(input("Row (1 - 3):"))
        l = int(input("Column (1 - 3):"))

        while not board.is_valid(k-1,l-1):
            print("Invalid input! Try again.")
            k = int(input("Row (1 - 3):"))
            l = int(input("Column (1 - 3):"))

        game.make_move(k-1, l-1)

        if board.is_winner() == 1:
            print("You WIN!")
            break
        if board.is_full():
            print("DRAW!")
            break

        
        if game.plyr == puter.plyr:

            (i,j) = puter.nxt_move(board)
            game.make_move(i, j)

            if board.is_winner() == 2:
                print("You LOSE!")
                break
            if board.is_full():
                print("DRAW!")
                break






main()