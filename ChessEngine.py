### Reference: https://github.com/MikeCreator-put/Chess/tree/887e6d08b27dc79d61a447a8c31236cfb7dbbfbc
# https://www.youtube.com/watch?v=EnYui0e73Rs&list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_&ab_channel=EddieSharick
'''
Storing all the information about the current state of chess game.
Determining valid moves at current state.
It will keep move log.
'''

## Assumption : No Castling
import numpy as np
import copy

class GameState():
    def __init__(self, dim):
        #Board is an 8x8 2d list, each element in list has 2 characters.
        #The first character represtents the color of the piece: 'b' or 'w'.
        #The second character represtents the type of the piece: 'R', 'N', 'B', 'Q', 'K' or 'p'.
        #"--" represents an empty space with no piece.
        self.dim = dim
        self.board = self.get_board()
        self.black_board = self.board.T
        self.is_whites_Turn = True
        self.Player_turn = 1
        self.last_move = None
        self.move = Move(dim)
        self.human = HumanPlayer(self.dim)

    def get_board(self):
        board = np.array([
            [-5, -3, -2, -9, -7, -2, -3, -5],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [5, 3, 2, 9, 7, 2, 3, 5]])

        return copy.deepcopy(board[:,:self.dim])


    def makeMove(self, start_square, end_square):
        flag = 0

        if self.Player_turn == 1:
            flag = self.human.play(self.board, start_square, end_square, self.last_move)
        # # Checks if the move is valid
        # if abs(self.board[start_square[0], start_square[1]]) == 1:
        #     if end_square in self.possible_move_pawn(start_square, end_square):
        #         check = self.move.is_possible_pawn(self.board, self.is_whites_Turn, start_square, end_square, self.last_move)
        #         if check[0]:
        #             flag = 1
        #             if (end_square[0] == 7) or (end_square[0] == 0):
        #                 new_piece = input("Q or R or N or B: ")
        #                 if new_piece.lower() == "q":
        #                     self.board[start_square[0], start_square[1]] = self.Player_turn * 9
        #                 elif new_piece.lower() == "r":
        #                     self.board[start_square[0], start_square[1]] = self.Player_turn * 5
        #                 elif new_piece.lower() == "n":
        #                     self.board[start_square[0], start_square[1]] = self.Player_turn * 3
        #                 elif new_piece.lower() == "b":
        #                     self.board[start_square[0], start_square[1]] = self.Player_turn * 2
        #                 else:
        #                     print("Invalid Input\nConverting the piece to Queen")
        #                     self.board[start_square[0], start_square[1]] = self.Player_turn * 9
        #
        #             ## En passant
        #             if check[1] == 1:
        #                 if self.is_whites_Turn:
        #                     self.board[start_square[0], end_square[1]] = 0
        #                 else:
        #                     self.board[start_square[0], end_square[1]] = 0

        ## Makes the move
        if flag == 1:
            self.last_move = (self.board[start_square[0], start_square[1]], end_square[0], end_square[1])
            self.board[end_square[0], end_square[1]] = self.board[start_square[0], start_square[1]]
            self.board[start_square[0], start_square[1]] = 0

            self.is_whites_Turn = not self.is_whites_Turn #switch players
            if self.is_whites_Turn:
                self.Player_turn = 1
                print("\n\nWhites Turn")
            else:
                self.Player_turn = -1
                print('\n\nBlacks Turn')




class Move():
    def __init__(self, dim):
        self.king_first_move = False
        self.rook_first_move = {}
        self.en_passant_potentials = None
        self.dim = dim
        self.Player_turn = 1

    def check_piece_and_play(self, board, current_location, next_location, last_move):
        if next_location in self.possible_move_pawn(current_location, next_location):
            check = self.is_possible_pawn(board, True, current_location, next_location, last_move)
            if check[0]:
                flag = 1
                ##ToDo:
                if (current_location[0] == 7):

                    new_piece = input("Q or R or N or B: ")
                    if new_piece.lower() == "q":
                        board[current_location[0], current_location[1]] = self.Player_turn * 9
                    elif new_piece.lower() == "r":
                        board[current_location[0], current_location[1]] = self.Player_turn * 5
                    elif new_piece.lower() == "n":
                        board[current_location[0], current_location[1]] = self.Player_turn * 3
                    elif new_piece.lower() == "b":
                        board[current_location[0], current_location[1]] = self.Player_turn * 2
                    else:
                        print("Invalid Input\nConverting the piece to Queen")
                        board[current_location[0], current_location[1]] = self.Player_turn * 9

                ## En passant
                if check[1] == 1:
                    if self.Player_turn == 1:
                        board[current_location[0], next_location[1]] = 0
                    else:
                        board[current_location[0], next_location[1]] = 0
                return flag
        return 0

    def possible_move_pawn(self, start_square, end_square):
        if end_square[1] >= self.dim:
            return []

        return [(start_square[0]- (self.Player_turn *1), start_square[1]), (start_square[0]-(self.Player_turn *2), start_square[1]),
                (start_square[0]-(self.Player_turn *1), start_square[1]-(self.Player_turn *1)), (start_square[0]-(self.Player_turn *1), start_square[1]+(self.Player_turn *1))]

    def possible_move_knight(self, start_square, end_square):
        if end_square[1] >= self.dim:
            return []

        return [(start_square[0] + (self.Player_turn *1), start_square + (self.Player_turn *2)),
                (start_square[0] - (self.Player_turn *1), start_square + (self.Player_turn *2)),
                (start_square[0] + (self.Player_turn *1), start_square - (self.Player_turn *2))
                (start_square[0] - (self.Player_turn *1), start_square - (self.Player_turn *2)),
                (start_square[0] + (self.Player_turn *1), start_square + (self.Player_turn *2)),
                (start_square[0] + (self.Player_turn *1), start_square + (self.Player_turn *2)),
                (start_square[0] + (self.Player_turn *1), start_square + (self.Player_turn *2)),
                (start_square[0] + (self.Player_turn *1), start_square + (self.Player_turn *2))]


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


class HumanPlayer():
    def __init__(self, dim):
        self.move = Move(dim)
        self.Player_turn = 1

    def play(self, board, current_location, next_location, last_move):
        # Checks if the move is valid
        if board[current_location[0], current_location[1]] == 1:
            return self.move.check_piece_and_play(board, current_location, next_location, last_move)
            # if next_location in self.move.possible_move_pawn(current_location, next_location):
            #     check = self.move.is_possible_pawn(board, True, current_location, next_location, last_move)
            #     if check[0]:
            #         flag = 1
            #         ##ToDo:
            #         if (current_location[0] == 7):
            #
            #             new_piece = input("Q or R or N or B: ")
            #             if new_piece.lower() == "q":
            #                 board[current_location[0], current_location[1]] = self.Player_turn * 9
            #             elif new_piece.lower() == "r":
            #                 board[current_location[0], current_location[1]] = self.Player_turn * 5
            #             elif new_piece.lower() == "n":
            #                 board[current_location[0], current_location[1]] = self.Player_turn * 3
            #             elif new_piece.lower() == "b":
            #                 board[current_location[0], current_location[1]] = self.Player_turn * 2
            #             else:
            #                 print("Invalid Input\nConverting the piece to Queen")
            #                 board[current_location[0], current_location[1]] = self.Player_turn * 9
            #
            #         ## En passant
            #         if check[1] == 1:
            #             if Player_turn == 1:
            #                 board[current_location[0], next_location[1]] = 0
            #             else:
            #                 board[current_location[0], next_location[1]] = 0
        return False


        
        
        
        