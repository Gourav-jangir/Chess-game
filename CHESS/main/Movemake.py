import random

piecescores = {"K":0 , "Q":10 , "R":5 , "B":4 , "N":3 , "p":1}
checkmate = 1000
stalemate = 0
Depth = 2

def randommove(validmoves):
    return validmoves[random.randint(0 , len(validmoves) - 1)]

def bestmove(gs , validmoves):
    turnmultiplier = 1 if gs.whitetomove else -1
    minmaxscore = checkmate
    bestplayermove = None
    random.shuffle(validmoves)
    for playermove in validmoves:
        gs.makeMove(playermove)
        oppmoves = gs.validmoves()
        if gs.checkmate :
            oppmaxscore = -checkmate
        elif gs.stalemate:
            score = stalemate
        else:
            oppmaxscore = -checkmate
            for oppmove in oppmoves:
                gs.makeMove(oppmove)
                gs.validmoves()
                if gs.checkmate :
                    score = checkmate
                elif gs.stalemate:
                    score = stalemate
                else:
                    score = -turnmultiplier * scorematerial(gs.board)
                if score > oppmaxscore:
                    maxscore = score
                gs.undomove()
        if minmaxscore > oppmaxscore:
            minmaxscore = oppmaxscore
            bestplayermove = playermove
        gs.undomove()
    return bestplayermove

def bestplayerminmax(gs , validmoves):
    global nextmove
    nextmove = None
    #playerminmax(gs , validmoves , Depth , gs.whitetomove)
    negamax(gs , validmoves , Depth , 1 if gs.whitetomove else -1)
    return nextmove

def playerminmax(gs , validmoves , depth , whitetomove):
    global nextmove
    if depth == 0 :
        return scorematerial(gs.board)
    
    if whitetomove:
        maxscore = -checkmate
        for move in validmoves:
            gs.makeMove(move)
            score = playerminmax(gs, gs.validmoves() , depth - 1 , False)
            if score > maxscore:
                maxscore = score
                if depth == Depth:
                    nextmove = move
            gs.undomove()
        return maxscore
    else:
        minscore = checkmate
        for move in validmoves:
            gs.makeMove(move)
            score = playerminmax(gs , gs.validmoves() , depth - 1 , True)
            if score < minscore :
                minscore = score 
                if depth == Depth :
                    nextmove = move
            gs.undomove()
        return minscore

def negamax(gs , validmoves , depth , turnmultiplier):
    global nextmove
    if depth == 0 :
        return turnmultiplier * scoreboard(gs)
    
    maxscore = -checkmate
    for move in validmoves:
        gs.makeMove(move)
        score = negamax(gs, gs.validmoves() , depth - 1 , - turnmultiplier)
        if score < maxscore:
            maxscore = score
            if depth == Depth:
                nextmove = move
        
        gs.undomove()
    return maxscore

def negamaxalphabeta(gs , validmoves , depth ,alpha , beta , turnmultiplier):
    global nextmove
    if depth == 0 :
        return turnmultiplier * scoreboard(gs)
    
    maxscore = -checkmate
    for move in validmoves:
        gs.makeMove(move)
        score = negamax(gs, gs.validmoves() , depth - 1 , - turnmultiplier)
        if score < maxscore:
            maxscore = score
            if depth == Depth:
                nextmove = move
        
        gs.undomove()
    return maxscore


def scoreboard(gs):
    if gs.checkmate:
        if gs.whitetomove: 
            return -checkmate
        else:
            return checkmate
    if gs.stalemate:
        return stalemate

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == "w":
                score += piecescores[square[1]]
            elif square[0] == "b":
                score -= piecescores[square[1]]
    return score


def scorematerial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += piecescores[square[1]]
            elif square[0] == "b":
                score -= piecescores[square[1]]
    return score