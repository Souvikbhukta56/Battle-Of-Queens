
import random
import numpy as np
pieceScore = {"R": 5, "N": 3, "B": 3, "Q": 10, "P": 1, "K": 0, "-":0}
CHECKMATE = 1000
STALEMATE = 0

turnMultiplier = 1

def scoreMaterial(gs):
    score = 0
    if gs.CHECKMATE:
        score = CHECKMATE
    elif gs.STALEMATE:
        score = STALEMATE
    else:
        for r in gs.board:
            for c in r:
                if c[0] == "w":
                    score += pieceScore[c[1]]
                elif c[0] == "b":
                    score -= pieceScore[c[1]]
    return score

def getRandomMove(moves):
    if np.shape(moves)[0] > 0:
        n = random.randint(0, np.shape(moves)[0] - 1)
        return moves[n]

def findBestMove(gs, moves, DEPTH):
    global D
    D = DEPTH
    
    global bestMove
    bestMove = None
    depth = DEPTH
    random.shuffle(moves)
    negaMaxMove(gs, moves, depth, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    return bestMove

def negaMaxMove(gs, moves, depth, alpha, beta, turnMultiplier):
    global bestMove
    if depth == 0:
        return turnMultiplier * scoreMaterial(gs)
    maxScore = -CHECKMATE
    for move in moves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves() + gs.castling()
        gs.checkMate(nextMoves)
        score = -negaMaxMove(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == D:
                bestMove = move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore






