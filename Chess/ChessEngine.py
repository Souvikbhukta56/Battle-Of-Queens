from numpy import array

class GameState:
    def __init__(self):
        self.board = array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ])
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

        self.wkMoveLog = []
        self.bkMoveLog = []
        self.br1MoveLog = []
        self.br2MoveLog = []
        self.wr1MoveLog = []
        self.wr2MoveLog = []

        self.bkMoved = False
        self.wkMoved = False
        self.br1Moved = False
        self.br2Moved = False
        self.wr1Moved = False
        self.wr2Moved = False

        self.CHECKMATE = False
        self.STALEMATE = False

    ###########################################################
    def makeMove(self, move):
        # general move
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        # castling move
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
            self.wkMoved = True
            self.wkMoveLog.append(move)
            if move.startCol - move.endCol == 2:
                self.board[7][0] = "--"
                self.board[move.endRow][move.endCol + 1] = "wR"
            if move.startCol - move.endCol == -2:
                self.board[7][7] = "--"
                self.board[move.endRow][move.endCol - 1] = "wR"

        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
            self.bkMoved = True
            self.bkMoveLog.append(move)
            if move.startCol - move.endCol == 2:
                self.board[0][0] = "--"
                self.board[move.endRow][move.endCol + 1] = "bR"
            if move.startCol - move.endCol == -2:
                self.board[0][7] = "--"
                self.board[move.endRow][move.endCol - 1] = "bR"

        # if rooks are moved then you cant do castling
        elif move.pieceMoved == "bR" and move.startRow == 0 and move.startCol == 0:
            self.br1Moved = True
            self.br1MoveLog.append(move) # storing record for undoing
        elif move.pieceMoved == "bR" and move.startRow == 0 and move.startCol == 7:
            self.br2Moved = True
            self.br2MoveLog.append(move)
        elif move.pieceMoved == "wR" and move.startRow == 7 and move.startCol == 0:
            self.wr1Moved = True
            self.wr1MoveLog.append(move)
        elif move.pieceMoved == "wR" and move.startRow == 7 and move.startCol == 7:
            self.wr2Moved = True
            self.wr2MoveLog.append(move)

    ###############################################################
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()

            if move.promotedPawn:
                self.board[move.startRow][move.startCol] = move.pieceMoved[0] + "P"
                self.board[move.endRow][move.endCol] = move.pieceCaptured
                move.promotedPawn = False

            elif move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
                self.wkMoveLog.pop()
                if len(self.wkMoveLog) == 0:
                    self.wkMoved = False
                if move.startCol - move.endCol == 2:
                    self.board[7][0] = "wR"
                    self.board[7][3] = "--"
                    self.board[7][4] = "wK"
                    self.board[7][2] = "--"
                elif move.startCol - move.endCol == -2:
                    self.board[7][7] = "wR"
                    self.board[7][5] = "--"
                    self.board[7][4] = "wK"
                    self.board[7][6] = "--"
                else:
                    self.board[move.startRow][move.startCol] = move.pieceMoved
                    self.board[move.endRow][move.endCol] = move.pieceCaptured

            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
                self.bkMoveLog.pop()
                if len(self.bkMoveLog) == 0:
                    self.bkMoved = False
                if move.startCol - move.endCol == 2:
                    self.board[0][0] = "bR"
                    self.board[0][3] = "--"
                    self.board[0][4] = "bK"
                    self.board[0][2] = "--"
                elif move.startCol - move.endCol == -2:
                    self.board[0][7] = "bR"
                    self.board[0][5] = "--"
                    self.board[0][4] = "bK"
                    self.board[0][6] = "--"
                else:
                    self.board[move.startRow][move.startCol] = move.pieceMoved
                    self.board[move.endRow][move.endCol] = move.pieceCaptured

            elif move.pieceMoved == "bR" and move.startRow == move.startCol == 0:
                self.br1MoveLog.pop()
                self.board[move.startRow][move.startCol] = move.pieceMoved
                self.board[move.endRow][move.endCol] = move.pieceCaptured
                if len(self.br1MoveLog) == 0:
                    self.br1Moved = False

            elif move.pieceMoved == "bR" and move.startRow == 0 and move.startCol == 7:
                self.board[move.startRow][move.startCol] = move.pieceMoved
                self.board[move.endRow][move.endCol] = move.pieceCaptured
                self.br2MoveLog.pop()
                if len(self.br2MoveLog) == 0:
                    self.br2Moved = False

            elif move.pieceMoved == "wR" and move.startRow == 7 and move.startCol == 0:
                self.board[move.startRow][move.startCol] = move.pieceMoved
                self.board[move.endRow][move.endCol] = move.pieceCaptured
                self.wr1MoveLog.pop()
                if len(self.wr1MoveLog) == 0:
                    self.wr1Moved = False

            elif move.pieceMoved == "wR" and move.startRow == move.startCol == 7:
                self.board[move.startRow][move.startCol] = move.pieceMoved
                self.board[move.endRow][move.endCol] = move.pieceCaptured
                self.wr2MoveLog.pop()
                if len(self.wr2MoveLog) == 0:
                    self.wr2Moved = False

            else:
                self.board[move.startRow][move.startCol] = move.pieceMoved
                self.board[move.endRow][move.endCol] = move.pieceCaptured

            self.whiteToMove = not self.whiteToMove
            if self.CHECKMATE:
                self.CHECKMATE = not self.CHECKMATE
            elif self.STALEMATE:
                self.STALEMATE = not self.STALEMATE

    def checkMate(self, moves):
        if len(moves) == 0:
            if self.inCheck():
                self.CHECKMATE = True
            else:
                self.STALEMATE = True

    # eliminating invalid moves
    def getValidMoves(self):
        moves = self.getAllPossibleMoves()
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])

            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.pop(i)
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.CHECKMATE = True
            else:
                self.STALEMATE = True
        return moves

    def inCheck(self):
        if self.whiteToMove:
            return self.sqUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        if not self.whiteToMove:
            return self.sqUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def sqUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        moves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in moves:
            if move.endCol == c and move.endRow == r:
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == "P":
                        self.getPawnMoves(r, c, moves)
                    elif piece == "R":
                        self.getRookMoves(r, c, moves)
                    elif piece == "B":
                        self.getBishopMoves(r, c, moves)
                    elif piece == "Q":
                        self.getQueenMoves(r, c, moves)
                    elif piece == "N":
                        self.getKnightMoves(r, c, moves)
                    elif piece == "K":
                        self.getKingMoves(r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        # for white pawn
        if self.whiteToMove:
            if r>0:
                # normal move 
                if self.board[r - 1][c] == "--":
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    # first move case
                    if r == 6 and self.board[r - 2][c] == "--":
                        moves.append(Move((r, c), (r - 2, c), self.board))

                # capture move
                if 0 <= c <= 6:
                    if self.board[r - 1][c + 1][0] == "b":
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
                if 1 <= c <= 7:
                    if self.board[r - 1][c - 1][0] == "b":
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
            
            # en-passant move
            if r == 3 and self.moveLog[-1].endRow == 3 and self.board[self.moveLog[-1].endRow][
                self.moveLog[-1].endCol] == "bP":
                if self.moveLog[-1].endRow - self.moveLog[-1].startRow == 2:
                    if self.moveLog[-1].endCol - c == 1:
                        m = Move((r, c), (r - 1, c + 1), self.board)
                        m.enPassant = True
                        moves.append(m)

                    if self.moveLog[-1].endCol - c == -1:
                        m = Move((r, c), (r - 1, c - 1), self.board)
                        m.enPassant = True
                        moves.append(m)

        # for black pawn
        elif not self.whiteToMove:
            if r<7:
                if self.board[r + 1][c] == "--":
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "--":
                        moves.append(Move((r, c), (r + 2, c), self.board))
                if 0 <= c <= 6:
                    if self.board[r + 1][c + 1][0] == "w":
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))
                if 1 <= c <= 7:
                    if self.board[r + 1][c - 1][0] == "w":
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
                        
            if r == 4 and self.moveLog[-1].endRow == 4 and self.board[self.moveLog[-1].endRow][
                self.moveLog[-1].endCol] == "wP":
                if self.moveLog[-1].endRow - self.moveLog[-1].startRow == -2:
                    if self.moveLog[-1].endCol - c == 1:
                        m = Move((r, c), (r + 1, c + 1), self.board)
                        m.enPassant = True
                        moves.append(m)

                    if self.moveLog[-1].endCol - c == -1:
                        m = Move((r, c), (r + 1, c - 1), self.board)
                        m.enPassant = True
                        moves.append(m)

    def getRookMoves(self, r, c, moves):
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    piece = self.board[endRow][endCol]
                    if piece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif piece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getBishopMoves(self, r, c, moves):
        directions = ((1, 1), (-1, 1), (-1, -1), (1, -1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    piece = self.board[endRow][endCol]
                    if piece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif piece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    piece = self.board[endRow][endCol]
                    if piece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif piece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        directions = ((2, 1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2), (-2, 1), (-2, -1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                piece = self.board[endRow][endCol]
                if piece == "--":
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                elif piece[0] == enemyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getKingMoves(self, r, c, moves):
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                piece = self.board[endRow][endCol]
                if piece == "--":
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                elif piece[0] == enemyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def castling(self):
        moves = []
        if self.whiteToMove and not self.inCheck() and self.board[7][1] == "--" and self.board[7][2] == "--" and self.board[7][3] == "--":
            if not self.sqUnderAttack(7, 3) and not self.sqUnderAttack(7, 2) and not self.wkMoved and not self.wr1Moved:
                moves.append(Move((7, 4), (7, 2), self.board))

        if not self.whiteToMove and not self.inCheck() and self.board[0][1] == "--" and self.board[0][2] == "--" and self.board[0][3] == "--":
            if not self.sqUnderAttack(0, 3) and not self.sqUnderAttack(0, 2) and not self.bkMoved and not self.br1Moved:
                moves.append(Move((0, 4), (0, 2), self.board))

        if self.whiteToMove and not self.inCheck() and self.board[7][5] == "--" and self.board[7][6] == "--":
            if not self.sqUnderAttack(7, 5) and not self.sqUnderAttack(7, 6) and not self.wkMoved and not self.wr2Moved:
                moves.append(Move((7, 4), (7, 6), self.board))

        if not self.whiteToMove and not self.inCheck() and self.board[0][5] == "--" and self.board[0][6] == "--":
            if not self.sqUnderAttack(0, 5) and not self.sqUnderAttack(0, 6) and not self.bkMoved and not self.br2Moved:
                moves.append(Move((0, 4), (0, 6), self.board))
        return moves


class Move:
    def __init__(self, start_sq, end_sq, board):
        self.startRow = start_sq[0]
        self.startCol = start_sq[1]
        self.endRow = end_sq[0]
        self.endCol = end_sq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.enPassant = False
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        self.promotedPawn = False

    def __eq__(self, other):
        if isinstance(other, Move):
            if self.moveID == other.moveID:
                other.enPassant = self.enPassant
                return True
        return False


