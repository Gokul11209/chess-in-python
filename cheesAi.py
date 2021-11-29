import random

pieceScore = {"K": 0 , "Q": 10, "R": 5, "B": 5, "N": 3, "P": 1}
CHECKMATE = 1000
CHECK = 0


def RandomMoves(vaildMoves):
    return vaildMoves[random.randint(0, len(vaildMoves)-1)]


def AIMoves(gs, vaildMoves):
    turnPlayer = 1 if gs.whiteToMove else -1
    oppentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(vaildMoves)
    for playerMove in vaildMoves:
        gs.makeMove(playerMove)
        oppentsMoves = gs.getVaildMoves()
        oppentMaxScore = -CHECKMATE
        for oppentMove in oppentsMoves:
            gs.makeMove(oppentMove)
            if gs.checkMate:
                score = -turnPlayer * CHECKMATE
            elif gs.check:
                score = CHECK
            else:
                score = -turnPlayer * ScoreMaterial(gs.board)
            if score > oppentMaxScore:
                oppentMaxScore = score
            gs.undoMove()
        if oppentMaxScore < oppentMinMaxScore:
            oppentMinMaxScore = oppentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove


def ScoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -+ pieceScore[square[1]]
    return score
            