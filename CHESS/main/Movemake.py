import random

piecescores = {"K":0 , "Q":10 , "R":5 , "B":4 , "N":3 , "p":1}
checkmate = 1000
stalemate = 0

def randommove(validmoves):
    return validmoves[random.randint(0 , len(validmoves) - 1)]

def bestmove(gs , validmoves):
    turnmultiplier = 1 if gs.whitetomove else -1
    maxscore = -checkmate
    bestmove = None
    for playermove in validmoves:
        gs.makeMove(playermove)
        if gs.checkmate :
            score = checkmate
        elif gs.stalemate:
            score = stalemate
        else:
            score = turnmultiplier * scorematerial(gs.board)
        if score > maxscore:
            maxscore = score
            bestmove = playermove
        gs.undomove()
    return bestmove

def scorematerial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += piecescores[square[1]]
            elif square[0] == "b":
                score -= piecescores[square[1]]
    return score