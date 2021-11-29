
class Gamestate():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.moveFunction ={'P':self.getPawnMoves, 'R':self.getRockMoves, 
                            'B':self.getBishopMoves,'N':self.getNightMoves,
                             'K':self.getKingMoves, 'Q':self.getQueenMoves}


        self.whiteToMove = True
        self.moveLog = []   
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.check = False
        self.checkMate =False 
        self.currentCastleRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastleRight.wks,
                                            self.currentCastleRight.bks,
                                            self.currentCastleRight.wqs, 
                                            self.currentCastleRight.bqs)]


    def makeMove(self,move):
        self.board[move.endRow][move.endCol]=move.pieceMoved
        self.board[move.startRow][move.startCol] = "--"
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove #swap players    
        #update king location
        if move.pieceMoved == 'wK':      
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        #pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        #castle move
        if move.isCastleMoves:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = '--' #rease rock
            else:
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = '--' #rease rock
        
        #castle move in king and rock
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastleRight.wks,
                                                self.currentCastleRight.bks,
                                                self.currentCastleRight.wqs,
                                                self.currentCastleRight.bqs))
        
    
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # swap players
            #update king location
            if move.pieceMoved == 'wK':      
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            # undo castleing
            self.castleRightsLog.pop()
            self.currentCastleRight = self.castleRightsLog[-1] 

            if move.isCastleMoves:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '--'
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'


    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastleRight.wks = False
            self.currentCastleRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastleRight.bks = False
            self.currentCastleRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:# left rock
                    self.currentCastleRight.wqs = False
                elif move.startCol == 7: # right rock
                    self.currentCastleRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:# left rock
                    self.currentCastleRight.bqs = False
                elif move.startCol == 7: # right rock
                    self.currentCastleRight.bks = False
        

    def getVaildMoves(self):
        tempCastleRights = CastleRights(self.currentCastleRight.wks,
                                        self.currentCastleRight.bks,
                                        self.currentCastleRight.wqs,
                                        self.currentCastleRight.bqs)
        
        moves =self.getAllPossibelMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
       
        # generate all possible moves
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])

            self.whiteToMove = not self.whiteToMove
            if self.inCheak():
                moves.remove(moves[i])#attack your king ,not vaild moves
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0:#either check and checkmate
            if self.inCheak():
                self.checkMate = True
            else:
                self.check = True
        else:
            self.checkMate = False
            self.check = False        

        self.currentCastleRight = tempCastleRights
        return moves

    
    def inCheak(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])    

    
    def squareUnderAttack(self, r, c):   
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibelMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False             

    
    def getAllPossibelMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunction[piece](r, c, moves)   
        return moves

   
    def getRockMoves(self, r, c, moves):
        dirctions =((-1,0), (0,-1), (1,0),(0,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in dirctions:
            for i in range (1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break    


    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            if  c-1 >= 0: #capture left        
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7: #capture right
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))   

        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            if  c-1 >= 0: #capture left        
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7: #capture right
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))   
             

    def getBishopMoves(self, r, c, moves):
        dirctions =((-1,-1), (-1,1), (1,-1),(1,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in dirctions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break    

    
    def getNightMoves(self, r, c, moves):
        dirctions = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
        enemyColor = "w" if self.whiteToMove else "b" 
        for i in dirctions:
            endRow = r + i[0]
            endCol = c + i[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != enemyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
    
    
    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRockMoves(r, c, moves)

    
    def getKingMoves(self, r, c, moves):
        dirctions = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
        enemyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + dirctions[i][0]
            endCol = c + dirctions[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != enemyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
        

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return
        if (self.whiteToMove and self.currentCastleRight.wks) or (not self.whiteToMove and self.currentCastleRight.bks):
            self.getKingSide(r, c, moves)
        if (self.whiteToMove and self.currentCastleRight.wqs) or (not self.whiteToMove and self.currentCastleRight.bqs):
            self.getQueenSide(r, c, moves)

    
    def getKingSide(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMoves=True))


    def getQueenSide(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3]:
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMoves=True)) 



class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
   


class Move():
    #maps keys to values
    #key:value
    ranksToRows ={"1":7, "2":6, "3":5, "4":4,
                  "5":3, "6":2, "7":1, "8":0}
    rowsToRanks ={v: k for k, v in ranksToRows.items()}
    filesToClos ={"a":0, "b":1, "c":2, "d":3,
                  "e":4, "f":5, "g":6, "h":7}
    colsToFiles ={v: k for k, v in filesToClos.items()}


    def __init__(self, startSq, endSq, board, isCastleMoves=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol] 
        self.isPawnPromotion =False
        if (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7):
            self.isPawnPromotion =True
        self.isCastleMoves = isCastleMoves
        self. moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
        

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow,self.endCol)

    
    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]




