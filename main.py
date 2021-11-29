import pygame as p 
import engine
import cheesAi

WIDTH = HEIGHT =575
DIM =8
SQ_SIZE = HEIGHT // DIM
MAX_FPS = 15
IMAGES= {}

def loadImages():
    pieces = ['wP','wR','wN','wB','wK','wQ','bP','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+ piece + ".png"),(SQ_SIZE,SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    p.display.set_caption("Chess Game....")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs =engine.Gamestate()
    
    vaildMoves = gs.getVaildMoves()
    moveMade = False
    animate = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    playerOne = True
    playerTwo = False
    
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        #mouse handled
        for e in p.event.get():
            if e.type == p.QUIT:
                running =False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row,col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = engine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range (len(vaildMoves)):
                            if move == vaildMoves[i]:
                                gs.makeMove(move)
                                moveMade = True
                                animate = True
                                sqSelected = () #reset sq sqlected
                                playerClicks = [] #reset palyer cilikes
                        if not moveMade:
                            playerClicks =[sqSelected] # remove last cliks 

            #key handled
            elif e.type == p.KEYDOWN:
                if e.key == p.K_x:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_s:
                    gs= engine.Gamestate()
                    vaildMoves= gs.getVaildMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        if not gameOver and  not humanTurn:
            AIMove = cheesAi.AIMoves(gs, vaildMoves)
            if AIMove is None:
                AIMove = cheesAi.RandomMoves(vaildMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True


        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            vaildMoves =gs.getVaildMoves() 
            moveMade = False  
            animate = False         

        drawGameState(screen, gs, vaildMoves, sqSelected)
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black Wins')
            else :
                drawText(screen, 'White Wins')
        elif gs.check:
            gameOver = True
            drawText(screen, 'check do safe your KING')
        
        clock.tick(MAX_FPS)
        p.display.flip()


def highLightSqure(screen, gs, vaildMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            #hihtlight sq
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #transperancy value
            s.fill(p.Color('blue'))
            screen.blit(s,(c*SQ_SIZE, r*SQ_SIZE))
            #moves colors
            s.fill(p.Color('green'))
            for move in vaildMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s,(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


def drawGameState(screen,gs, vaildMoves, sqSelected):
    drawBorad(screen)
    highLightSqure(screen, gs, vaildMoves, sqSelected)
    drawPieces(screen,gs.board)        

def drawBorad(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray ")]
    for r in range(DIM):
        for c in range(DIM):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen,board):
    for r in range(DIM):
        for c in range(DIM):
            piece = board[r][c]
            if piece !="--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))            


def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    frames = 4
    frameCount =(abs(dR) + abs(dC))* frames
    for frame in range (frameCount + 1):
        r ,c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBorad(screen)
        drawPieces(screen, board)
        #erase piece moved from end sq
        color =  colors[(move.endRow + move.endCol) % 2]
        endSqure = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSqure)
        #draw capture puece into rectangle
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], endSqure)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 30, True, False)
    textObj = font.render(text, 0, p.Color('Red'))
    loction = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObj.get_width()/2, HEIGHT/2 - textObj.get_height()/2)
    screen.blit(textObj,loction)
    #textObj = font.render(text, 0, p.Color('gray'))
    #screen.blit(text, loction.move((2,2))



if __name__ == "__main__":
    main()