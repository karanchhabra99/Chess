### Reference: https://github.com/MikeCreator-put/Chess/tree/887e6d08b27dc79d61a447a8c31236cfb7dbbfbc
# https://www.youtube.com/watch?v=EnYui0e73Rs&list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_&ab_channel=EddieSharick
'''
Storing all the information about the current state of chess game.
Determining valid moves at current state.
It will keep move log.
'''

## Assumption : No En Passant, No Castling
import numpy as np

class GameState():
    def __init__(self):
        #Board is an 8x8 2d list, each element in list has 2 characters.
        #The first character represtents the color of the piece: 'b' or 'w'.
        #The second character represtents the type of the piece: 'R', 'N', 'B', 'Q', 'K' or 'p'.
        #"--" represents an empty space with no piece.
        self.board = np.array([
            [-5, -3, -2, -9, -7, -2, -3, -5],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [5, 3, 2, 9, 7, 2, 3, 5]])
        self.is_whites_Turn = True
        self.last_move = None
        self.move = Move()
        
    def makeMove(self, start_square, end_square):
        flag = 0
        if abs(self.board[start_square[0], start_square[1]]) == 1:
            check = self.move.is_possible_pawn(self.board, self.is_whites_Turn, start_square, end_square, self.last_move)
            if check[0]:
                flag = 1
                ## En passant
                if check[1] == 1:
                    if self.is_whites_Turn:
                        self.board[start_square[0], end_square[1]] = 0
                    else:
                        self.board[start_square[0], end_square[1]] = 0
        if flag == 1:
            self.last_move = (self.board[start_square[0], start_square[1]], end_square[0], end_square[1])
            self.board[end_square[0], end_square[1]] = self.board[start_square[0], start_square[1]]
            self.board[start_square[0], start_square[1]] = 0

            self.is_whites_Turn = not self.is_whites_Turn #switch players
            if self.is_whites_Turn:
                print("\n\nWhites Turn")
            else:
                print('\n\nBlacks Turn')

class Move():
    def __init__(self):
        self.king_first_move = False
        self.rook_first_move = {}
        self.en_passant_potentials = None
    def is_possible_pawn(self, board, is_whites_Turn, current_location, next_location, last_move):
        # Checking if it is attack or straight move
        if board[next_location[0], next_location[1]] == 0:
            ## Straight move
            if is_whites_Turn == True:
                ## Checking if the move is possible or not
                check= self.is_possible_pawn_helper(board, is_whites_Turn, current_location, next_location)
                ## if the move is possibel
                if check[0]:
                    ## Checking if the move is 2 steps ahead
                    if check[1] ==1:
                        self.en_passant_potentials = next_location
                    return (True, 0)
            else:
                check = self.is_possible_pawn_helper(board, is_whites_Turn, next_location, current_location)
                if check[0]:
                    ## Checking if the move is 2 steps ahead
                    if check[1] ==1:
                        self.en_passant_potentials = next_location
                    return (True, 0)
        ## Attach move
        if (current_location[1]+1 == next_location[1]) or (current_location[1]-1 == next_location[1]):
            if is_whites_Turn == True:
                # change in row by 1
                if current_location[0] - next_location[0] == 1:
                    if board[next_location[0], next_location[1]] < 0:
                        return (True, 0)
                    ## En Passant
                    if (last_move[1] == self.en_passant_potentials[0]) and (last_move[2] == self.en_passant_potentials[1]):
                        if last_move[0] == -1:
                            if board[current_location[0], next_location[1]] == -1:
                                return (True, 1)

            else:
                if next_location[0] - current_location[0] == 1:
                    if board[next_location[0], next_location[1]] > 0:
                        return (True, 0)
                    ## En Passant
                    if (last_move[1] == self.en_passant_potentials[0]) and (last_move[2] == self.en_passant_potentials[1]):
                        if last_move[0] == 1:
                            if board[current_location[0], next_location[1]] == 1:
                                return (True, 1)
        return (False, 0)

    def is_possible_pawn_helper(self, board, is_whites_Turn, higher_location_index, lower_location_index):
        ## One move forward
        if higher_location_index[0] - lower_location_index[0] == 1:
            if higher_location_index[1] == lower_location_index[1]:
                return (True, 0)
        ## Two moves forward
        elif higher_location_index[0] - lower_location_index[0] == 2:
            ## Whites Turn
            if is_whites_Turn:
                if higher_location_index[0] != board.shape[0] - 2:
                    return (False, 0)
                else:
                    if board[higher_location_index[0] - 1, higher_location_index[1]] == 0:
                        return (True, 1)
            ## Blacks_turn
            else:
                if lower_location_index[0] != 1:
                    return (False, 0)
                else:
                    if board[higher_location_index[0] - 1, higher_location_index[1]] == 0:
                        return (True, 1)
        return (False, 0)

# class Move():
#     '''
#     in chess the fields on the board are described by two symbols, one of them being number between 1-8 (which is corespodning to rows)
#     and the second one being a letter between a-f (coresponding to columns), in order to use this notation we need to map our [row][col] coordinates
#     to match the ones used in the original chess game
#     '''
#     ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
#                      "5": 3, "6": 2, "7": 1, "8": 0}
#     rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
#     files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
#                      "e": 4, "f": 5, "g": 6, "h": 7}
#     cols_to_files = {v: k for k, v in files_to_cols.items()}
#
#     def __init__(self, start_square, end_square, board):
#         self.start_row = start_square[0]
#         self.start_col = start_square[1]
#         self.end_row = end_square[0]
#         self.end_col = end_square[1]
#         self.piece_moved =
#         self.piece_captured = board[self.end_row][self.end_col]
#
#     def getChessNotation(self):
#         return self.piece_moved + " " + self.getRankFile(self.start_row, self.start_col) + "->" + self.getRankFile(self.end_row, self.end_col) + " " + self.piece_captured
#
#     def getRankFile(self, row, col):
#         return self.cols_to_files[col] + self.rows_to_ranks[row]
#
        
        
        
        
        