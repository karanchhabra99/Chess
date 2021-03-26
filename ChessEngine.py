### Reference: https://github.com/MikeCreator-put/Chess/tree/887e6d08b27dc79d61a447a8c31236cfb7dbbfbc
# https://www.youtube.com/watch?v=EnYui0e73Rs&list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_&ab_channel=EddieSharick

## Assumption : No Castling
            # Pawn can't check King
import numpy as np
import copy

class GameState():
    def __init__(self, dim):
        self.move = Move(dim)
        self.dim = dim
        self.board = self.get_board()
        self.black_board = np.flipud(self.board)
        self.Player_turn = 1
        self.last_move = None

        ## ToDO: AI and Human
        self.human = HumanPlayer(self.dim, self.move)
        self.human2 = HumanPlayer(self.dim, self.move)

    def get_board(self):
        board = np.array([
            [-5, -3, -2, -9, -1000, -2, -3, -5],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [5, 3, 2, 9, 1000, 2, 3, 5]])

        return copy.deepcopy(board[:,:self.dim])


    def makeMove(self, start_square, end_square):
        flag = 0
        # Change Player turns and Check if move is valid
        if self.Player_turn == 1:
            ## Checking if the correct piece is chosen
            if self.board[start_square[0],start_square[1]] > 0:
                flag = self.human.play(self.board, start_square, end_square, self.Player_turn, self.last_move)
        else:
            ## Checking if the correct piece is chosen
            if self.board[start_square[0],start_square[1]] < 0:
                if self.board[start_square[0], start_square[1]] == -1:
                    temp1 = self.board[start_square[0], start_square[1]]
                    self.board[start_square[0], start_square[1]] = 25
                    inverse_start = np.where(self.black_board == 25)
                    self.board[start_square[0], start_square[1]] = temp1

                    temp2 = self.board[end_square[0], end_square[1]]
                    self.board[end_square[0], end_square[1]] = 25
                    inverse_end = np.where(self.black_board == 25)
                    self.board[end_square[0], end_square[1]] = temp2

                    flag = self.human2.play(self.black_board, (inverse_start[0][0], inverse_start[1][0]), (inverse_end[0][0], inverse_end[1][0]), self.Player_turn, self.last_move)
                else:
                    flag = self.human2.play(self.board, start_square, end_square, self.Player_turn, self.last_move)

        ## Makes the move
        if flag == 1:
            self.last_move = (self.board[start_square[0], start_square[1]], end_square[0], end_square[1])
            self.board[end_square[0], end_square[1]] = self.board[start_square[0], start_square[1]]
            self.board[start_square[0], start_square[1]] = 0

            if self.Player_turn == 1:
                self.Player_turn = -1
                print('\n\nBlacks Turn')
            else:
                self.Player_turn = 1
                print("\n\nWhites Turn")

class Pawn():
    def __init__(self, dim):
        self.en_passant_potentials = None
        self.dim = dim
        self.Player_turn = 1

    def pawn_move_checker_en_passant(self, board, current_location, next_location, last_move, Player_turn):
        self.Player_turn = Player_turn
        if next_location in self.all_move_pawn(current_location, next_location):
            check = self.is_possible_pawn(board, current_location, next_location, last_move)
            if check[0]:
                flag = 1
                ##ToDo:
                if (next_location[0] == 0):
                    new_piece = input("Q or R or K or B: ")
                    if new_piece.lower() == "q":
                        board[current_location[0], current_location[1]] = self.Player_turn * 9
                    elif new_piece.lower() == "r":
                        board[current_location[0], current_location[1]] = self.Player_turn * 5
                    elif new_piece.lower() == "k":
                        board[current_location[0], current_location[1]] = self.Player_turn * 3
                    elif new_piece.lower() == "b":
                        board[current_location[0], current_location[1]] = self.Player_turn * 2
                    else:
                        print("Invalid Input\nConverting the piece to Queen")
                        board[current_location[0], current_location[1]] = self.Player_turn * 9

                ## En passant
                if check[1] == 1:
                    board[current_location[0], next_location[1]] = 0
                return flag
        return 0

    def all_move_pawn(self, start_square, end_square):
        if end_square[1] >= self.dim:
            return []

        return [(start_square[0]- 1, start_square[1]), (start_square[0]-2, start_square[1]),
                (start_square[0]-1, start_square[1]-1), (start_square[0]-1, start_square[1]+1)]

    def is_possible_pawn(self, board, current_location, next_location, last_move):
        # Checking if it is attack or straight move
        if board[next_location[0], next_location[1]] == 0:
            ## Straight move
            ## Checking if the move is possible or not
            check= self.is_possible_pawn_helper(board, current_location, next_location)
            ## if the move is possible
            if check[0]:
                ## Checking if the move is 2 steps ahead
                if check[1] ==1:
                    if self.Player_turn == -1:
                        board[next_location[0], next_location[1]] = 25
                        inverse_board = np.flipud(board)
                        inverse_move = np.where(inverse_board == 25)
                        self.en_passant_potentials = (inverse_move[0][0], next_location[1])
                    else:
                        self.en_passant_potentials = next_location
                return (True, 0)

        ## Attach move
        if (current_location[1]+1 == next_location[1]) or (current_location[1]-1 == next_location[1]):
            if current_location[0] - next_location[0] == 1:
                if board[next_location[0], next_location[1]] != 0:
                    return (True, 0)
                if self.en_passant_potentials != None:
                    ## En Passant
                    if ((last_move[1] == self.en_passant_potentials[0]) and (last_move[2] == self.en_passant_potentials[1])):
                        if (current_location[0] == 3) and (next_location[1] == self.en_passant_potentials[1]):
                            if board[current_location[0], next_location[1]] == self.Player_turn *-1:
                                return (True, 1)

        return (False, 0)

    def is_possible_pawn_helper(self, board, higher_location_index, lower_location_index):
        ## One move forward
        if higher_location_index[0] - lower_location_index[0] == 1:
            if higher_location_index[1] == lower_location_index[1]:
                return (True, 0)

        ## Two moves forward
        elif higher_location_index[0] - lower_location_index[0] == 2:
            if higher_location_index[0] != board.shape[0] - 2:
                return (False, 0)
            else:
                if board[higher_location_index[0] - 1, higher_location_index[1]] == 0:
                    return (True, 1)
        return (False, 0)

class Knight():
    def __init__(self, dim):
        self.dim = dim
        self.Player_turn = 1

    def knight_move_checker(self, board, current_location, next_location, Player_turn):
        self.Player_turn =Player_turn
        if next_location in self.all_move_knight(current_location, next_location):
            if self.Player_turn == 1:
                if board[next_location[0], next_location[1]] <= 0:
                    return 1
            else:
                if board[next_location[0], next_location[1]] >= 0:
                    return 1
        return 0

    def all_move_knight(self, start_square, end_square):
        if end_square[1] >= self.dim:
            return []

        return [(start_square[0] + 1, start_square[1] + 2),
                (start_square[0] - 1, start_square[1] - 2),
                (start_square[0] + 1, start_square[1] - 2),
                (start_square[0] - 1, start_square[1] + 2),
                (start_square[0] + 2, start_square[1] + 1),
                (start_square[0] - 2, start_square[1] - 1),
                (start_square[0] + 2, start_square[1] - 1),
                (start_square[0] - 2, start_square[1] + 1)]

class Bishop():
    def __init__(self, dim):
        self.dim = dim
        self.Player_turn = 1

    def bishop_move_checker(self, board, current_location, next_location, Player_turn):
        self.Player_turn = Player_turn
        if next_location in self.diagonal_moves(board, current_location):
            return 1
        return 0

    def diagonal_moves(self, board, current_location):
        all_moves = []
        forward_col = current_location[1]
        backward_col = current_location[1]
        for i in range(current_location[0]+1, self.dim):
            forward_col, backward_col = self.diagonal_moves_helper(board, i, forward_col, backward_col, all_moves)

        forward_col = current_location[1]
        backward_col = current_location[1]
        for i in range(current_location[0]-1, -1, -1):
            forward_col, backward_col = self.diagonal_moves_helper(board, i, forward_col, backward_col, all_moves)

        return all_moves

    def diagonal_moves_helper(self, board, i, forward_col, backward_col, all_moves):
        forward_col += 1
        backward_col -= 1
        if forward_col <= 7:
            forward_col = self.diagonal_moves_helpers_helper(board, i, forward_col, all_moves, 'forward')

        if not backward_col < 0:
            backward_col = self.diagonal_moves_helpers_helper(board, i, backward_col, all_moves, 'backward')

        return forward_col, backward_col

    def diagonal_moves_helpers_helper(self, board, i, col, all_moves, direction):
        if board[i, col] == 0:
            all_moves.append((i, col))
        elif board[i, col] < 0:
            if self.Player_turn == 1:
                all_moves.append((i, col))

            ## Intend the below logic to make the bishop jump accross his pieces
            if direction == 'forward':
                col = 8
            else:
                col = 0
        elif board[i, col] > 0:
            if self.Player_turn == -1:
                all_moves.append((i, col))
            ## Intend the below logic to make the bishop jump accross his pieces
            if direction == 'forward':
                col = 8
            else:
                col = 0
        else:
            col = 8

        return col


class Rook:
    def __init__(self, dim):
        self.dim = dim
        self.Player_turn = 1

    def rook_move_checker(self, board, current_location, next_location, Player_turn):
        self.Player_turn = Player_turn
        if next_location in self.straight_moves(board, current_location):
            return 1
        return 0

    def straight_moves(self, board, current_location):
        all_moves = []
        i = current_location[0]+1
        while self.dim > i:
            i = self.straight_moves_col_helper(board, i, current_location, all_moves, 'forward')
        i = current_location[0]-1
        while 0 <= i:
            i = self.straight_moves_col_helper(board, i, current_location, all_moves, 'backward')

        ## Horizontal
        i = current_location[1]+1
        while self.dim > i:
            i = self.straight_moves_horizontal_helper(board, i, current_location, all_moves, 'forward')
        i = current_location[1]-1
        while 0 <= i:
            i = self.straight_moves_horizontal_helper(board, i, current_location, all_moves, 'backward')
        print(all_moves)
        return all_moves

    def straight_moves_col_helper(self, board, i, current_location, all_moves, direction):
        if board[i, current_location[1]] == 0:
            all_moves.append((i, current_location[1]))
        elif board[i, current_location[1]] < 0:
            if self.Player_turn == 1:
                all_moves.append((i, current_location[1]))
            if direction == 'forward':
                i = 8
            else:
                i = 0
        elif board[i, current_location[1]] > 0:
            if self.Player_turn == -1:
                all_moves.append((i, current_location[1]))
            if direction == 'forward':
                i = 8
            else:
                i = 0
        else:
            i = 8
        if direction == 'forward':
            i+=1
        else:
            i-=1
        return i

    def straight_moves_horizontal_helper(self, board, i, current_location, all_moves, direction):
        if board[current_location[0], i] == 0:
            all_moves.append((current_location[0], i))
        elif board[current_location[0], i] < 0:
            if self.Player_turn == 1:
                all_moves.append((current_location[0], i))
            if direction == 'forward':
                i = 8
            else:
                i = 0
        elif board[current_location[0], i] > 0:
            if self.Player_turn == -1:
                all_moves.append((current_location[0], i))
            if direction == 'forward':
                i = 8
            else:
                i = 0
        else:
            i = 8
        if direction == 'forward':
            i+=1
        else:
            i-=1
        return i


class Move():
    def __init__(self, dim):
        # self.king_first_move = False
        # self.rook_first_move = {}
        self.pawn = Pawn(dim)
        self.knight = Knight(dim)
        self.bishop = Bishop(dim)
        self.rook = Rook(dim)
        self.dim = dim
        self.Player_turn = 1

    def check_piece_and_play(self, board, current_location, next_location, Player_turn, last_move):
        self.Player_turn = Player_turn
        if board[current_location[0], current_location[1]] == self.Player_turn * 1:
            return self.pawn.pawn_move_checker_en_passant(board, current_location, next_location, last_move, Player_turn)
        elif board[current_location[0], current_location[1]] == self.Player_turn * 2:
            return self.bishop.bishop_move_checker(board, current_location, next_location, Player_turn)
        elif board[current_location[0], current_location[1]] == self.Player_turn * 3:
            return self.knight.knight_move_checker(board, current_location, next_location, Player_turn)
        elif board[current_location[0], current_location[1]] == self.Player_turn * 5:
            return self.rook.rook_move_checker(board, current_location, next_location, Player_turn)




class HumanPlayer():
    def __init__(self, dim, move):
        self.move = move

    def play(self, board, current_location, next_location, Player_turn, last_move):
        # Checks if the move is valid
        return self.move.check_piece_and_play(board, current_location, next_location, Player_turn, last_move)
