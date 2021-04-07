### Most of the code in this file has been taken from the below links (Only minor changes has been done to it):
# Reference: https://github.com/MikeCreator-put/Chess/tree/887e6d08b27dc79d61a447a8c31236cfb7dbbfbc
# https://www.youtube.com/watch?v=EnYui0e73Rs&list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_&ab_channel=EddieSharick
'''
Main driver file.
Handling user input.
Displaying current GameStatus object.
'''

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8

SQUARE_SIZE = HEIGHT // DIMENSION

MAX_FPS = 15
    
IMAGES = {}

'''
Initialize a global directory of images.
This will be called exactly once in the main.
'''

def loadImages():
    pieces = ['1', '5', '3', '2', '1000', '9', '-1', '-5', '-3', '-2', '-1000', '-9']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE,SQUARE_SIZE))
        
        
'''
The main driver for our code.
This will handle user input and updating the graphics.
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = ChessEngine.GameState(DIMENSION)
    loadImages() #do this only once before while loop
    
    running = True
    square_selected = () #no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    player_clicks = [] #this will keep track of player clicks (two tuples)

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                p.quit()
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x, y) location of the mouse
                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE
                if square_selected == (row, col): #user clicked the same square twice
                    square_selected = () #deselect
                    player_clicks = [] #clear clicks
                else:
                    square_selected = (row, col)
                    player_clicks.append(square_selected) #append for both 1st and 2nd click
                if len(player_clicks) == 2: #after 2nd click
                    # move = game_state.gui_move(, game_state.board)
                    # print(move.getChessNotation())
                    # print(move.piece_moved)
                    game_state.makeMove(player_clicks[0], player_clicks[1])
                    square_selected = () #reset user clicks
                    player_clicks = []
                elif  len(player_clicks) == 1:
                    print('Piece Selected')
                else:
                    print('Nothing is selected')

        drawGameState(screen, game_state) 
        clock.tick(MAX_FPS)
        p.display.flip()



'''
Responsible for all the graphics within current game state.
'''
def drawGameState(screen, game_state):
    drawBoard(screen) #draw squares on the board
    #add in piece highlighting or move suggestions (later)
    drawPieces(screen, game_state.board) #draw pieces on top of those squares      

'''
Draw the squares on the board.
The top left square is always light.
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(8):
        for column in range(DIMENSION):
            color = colors[((row+column) % 2)]
            p.draw.rect(screen, color, p.Rect(column*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
'''
Draw the pieces on the board using the current game_state.board
'''
def drawPieces(screen, board):
    for row in range(8):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != 0:
                screen.blit(IMAGES[str(piece)], p.Rect(column*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
         
                
if __name__ == "__main__":
    ## ToDO: Uncomment below and comment Dim
    # DIMENSION = int(input("Enter the Board width: "))
    # while ((DIMENSION < 5) and (DIMENSION > 8)):
    #     DIMENSION = int(input("Enter the Board width: "))
    DIMENSION = 8

    main()
