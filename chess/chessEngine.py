class GameState():
    def __init__(self):
        self.board = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bp','bp','bp','bp','bp','bp','bp','bp'],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ['wp','wp','wp','wp','wp','wp','wp','wp'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']
        ]
        self.moveFunctions = {'p':self.getPawnMoves, 'R':self.getRookMoves, 'N':self.getKnightMoves, 'B':self.getBishopMoves, 'Q':self.getQueenMoves, 'K':self.getKingMoves}
        self.whiteToMove = True
        self.movelog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)      
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = () #coordinates of square where en passant is possible

    
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)
        self.whiteToMove = not self.whiteToMove #next turn of other player
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow,move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow,move.endCol)
        if move.pawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
        if move.enpassantMove:
            self.board[move.startRow][move.endCol] = '--' #capturing pawn in en passant
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()


        

    def undoMove(self):
        if len(self.movelog) != 0:
            move=self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow,move.startCol)
            if move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow,move.startCol)
            if move.enpassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()
            

    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        moves = self.getAllPossibleMoves()
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves)==0: #either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        

            
        self.enpassantPossible = tempEnpassantPossible
        return moves
    
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])


    def squareUnderAttack(self,r,c):
        self.whiteToMove = not self.whiteToMove #enemy POV
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow==r and move.endCol==c:
                return True
        return False


    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves
    
    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r,c), (r-1,c), self.board))
                if r==6 and self.board[r-2][c]=="--":
                    moves.append(Move((r,c), (r-2,c), self.board))
            if c-1>=0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r,c), (r-1,c-1), self.board))
                elif (r-1,c-1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r-1,c-1), self.board, enpassantMove = True))
            if c+1<=7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c), (r-1,c+1), self.board))
                elif (r-1,c+1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r-1,c+1), self.board, enpassantMove = True))
        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c), (r+1,c), self.board))
                if r==1 and self.board[r+2][c]=="--":
                    moves.append(Move((r,c), (r+2,c), self.board))
            if c-1>=0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c), (r+1,c-1), self.board))
                elif (r+1,c-1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r+1,c-1), self.board, enpassantMove = True))
            if c+1<=7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c), (r+1,c+1), self.board))
                elif (r+1,c+1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r+1,c+1), self.board, enpassantMove = True))











    def getRookMoves(self,r,c,moves):
        directions = ((-1,0),(0,-1),(1,0),(0,1)) #up, left, down, right
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0<=endRow<8 and 0<=endCol<8: #on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space valid
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy place valid
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                        break
                    else: #friendly place invalid
                        break
                else: #off board
                    break

                         

        
    def getKnightMoves(self,r,c,moves):
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0<=endRow<8 and 0<=endCol<8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c), (endRow,endCol), self.board))

        
        
    def getBishopMoves(self,r,c,moves):
        directions = ((-1,-1),(-1,1),(1,-1),(1,1)) #up, left, down, right
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0<=endRow<8 and 0<=endCol<8: #on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space valid
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy place valid
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                        break
                    else: #friendly place invalid
                        break
                else: #off board
                    break

    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    def getKingMoves(self,r,c,moves):
        kingMoves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0<=endRow<8 and 0<=endCol<8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c), (endRow,endCol), self.board))


    





class Move():
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRanks = {v:k for k,v in ranksToRows.items()}
    filesToCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v:k for k,v in filesToCols.items()}
    def __init__(self, startSq, endSq, board, enpassantMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        #pawn promotion
        self.pawnPromotion = (self.pieceMoved=='wp' and self.endRow==0) or (self.pieceMoved=='bp' and self.endRow==7)
        

        #en passant
        self.enpassantMove = enpassantMove
        if self.enpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'


        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        
    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

