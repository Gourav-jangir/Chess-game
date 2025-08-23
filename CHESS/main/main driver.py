import pygame as p
import storage , Movemake
width = height = 512
dime = 8
sq_size = height // dime
fps = 15
image = {}


def LoadImages():
    pieces = ["bR","bN","bB","bQ","bK","bp","wR","wN","wB","wQ","wK","wp"]
    for piece in pieces:
        image[piece] = p.image.load(f"chess-game/CHESS/main/pics/{piece}.png")


def main():
    p.init()
    screen = p.display.set_mode((width,height))
    screen.fill(p.Color("white"))
    clock = p.time.Clock()
    gs = storage.GameState()
    LoadImages()
    valid = gs.validmoves()
    animate = False
    movemade = False
    running = True
    gameover = False
    sqsel = ()
    playerclick = []
    playerone = True
    playertwo = False
    while running:
        humanturn = (gs.whitetomove and playerone) or (not gs.whitetomove and playertwo)
        for e in p.event.get():
            if e.type == p.QUIT :
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if humanturn and not gameover:
                    loc = p.mouse.get_pos()
                    col = loc[0]//sq_size
                    row = loc[1]//sq_size
                    if sqsel == (row , col):
                        sqsel = ()
                        playerclick = []
                    else :
                        sqsel = (row,col)
                        playerclick.append(sqsel)
                    
                    if len(playerclick) == 2 :
                        move = storage.Move(playerclick[0], playerclick[1] , gs.board)
                        print(move.getchessNotation())
                        for i in range(len(valid)):
                            if move == valid[i]:
                                gs.makeMove(valid[i])
                                movemade = True
                                animate = True
                                sqsel = ()
                                playerclick = []
                        if not movemade:
                            playerclick = [sqsel]
            

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undomove()
                    movemade = True 
                    animate = False
                if e.key == p.K_r :
                    gs = storage.GameState()
                    valid = gs.validmoves()
                    sqsel = ()
                    playerclick = []
                    movemade = False 
                    animate = False
                    

        if movemade:
            if animate:
                animateit(gs.movelog[-1] , screen , gs.board , clock)
            valid = gs.validmoves()
            movemade = False
            animate = False

        drawGameState(screen , gs , valid , sqsel)
        clock.tick(fps)
        p.display.flip()


def highlightsquares(screen , gs , valid , sqsel):
    if sqsel != ():
        r,c = sqsel
        if gs.board[r][c][0] == ("w" if gs.whitetomove else "b"):
            s = p.Surface((sq_size , sq_size))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s, (c*sq_size , r*sq_size))
            s.fill(p.Color("yellow"))
            for move in valid:
                if move.startrow == r and move.startcol == c :
                    screen.blit(s , (move.endcol * sq_size , move.endrow * sq_size))


def drawGameState(screen , gs , valid , sqsel):
    drawboard(screen)
    highlightsquares(screen , gs , valid , sqsel)
    drawpieces(screen,gs.board)


def drawboard(screen):
    global colors
    colors = [p.Color("light gray") , p.Color("dark gray")]
    for r in range(dime):
        for i in range(dime):
            color = colors[(r+i) % 2]
            p.draw.rect(screen, color ,p.Rect(i*sq_size , r*sq_size , sq_size , sq_size))


def drawpieces(screen , board):
    for r in range(dime):
        for c in range(dime):
            piece = board[r][c]
            if piece != "--" :
                 screen.blit(image[piece], p.Rect(c*sq_size , r*sq_size , sq_size , sq_size))

def animateit(move , screen , board , clock):
    global colors
    coords = []
    dR = move.endrow - move.startrow
    dC = move.endcol - move.startcol
    fps = 10
    framecount = (abs(dR) + abs(dC)) + fps
    for frame in range(framecount + 1):
        r,c = (move.startrow + dR*frame/framecount ,move.startcol + dC * frame/framecount)
        drawboard(screen)
        drawpieces(screen ,board)
        color = colors[(move.endrow + move.endcol) % 2]
        endsquare = p.Rect(move.endcol*sq_size , move.endrow * sq_size , sq_size , sq_size)
        p.draw.rect(screen , color , endsquare)
        if move.piececaptured != '--':
            screen.blit(image[move.piececaptured] , endsquare)
        screen.blit(image[move.piecemoved] , p.Rect(c*sq_size , r * sq_size , sq_size , sq_size))
        p.display.flip()
        clock.tick(60)

if __name__ == "__main__" :
    main()