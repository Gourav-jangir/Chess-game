class GameState:
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.whitetomove = True
        self.movefunc = {"p" : self.pawnmoves , "R" : self.rookmoves , "N" : self.knightmoves , "B" : self.bishopmoves , "Q" : self.queenmoves ,
                         "K" : self.kingmoves}
        self.movelog = []
        self.whitekingloc = (7,4)
        self.blackkingloc = (0,4)
        self.checkmate = False
        self.stalemate = False
        self.pins = []
        self.checks = []
        self.incheck = False
        self.enpassant = ()
        self.currentrights = castlerights(True , True , True , True)
        self.rightslogs = [castlerights(self.currentrights.wks , self.currentrights.wqs , 
                                        self.currentrights.bks , self.currentrights.bqs)]
        
        


    def makeMove(self,move):
        self.board[move.startrow][move.startcol] = "--"
        self.board[move.endrow][move.endcol] = move.piecemoved
        self.movelog.append(move)
        self.whitetomove = not self.whitetomove 
        if move.piecemoved == "wK" :
            self.whitekingloc = (move.endrow , move.endcol)
        if move.piecemoved == "bK" :
            self.blackkingloc = (move.endrow , move.endcol)

        if move.pawnpromoted :
            self.board[move.endrow][move.endcol] = move.piecemoved[0] + 'Q'
        
        if move.isenpassant :
            self.board[move.startrow][move.endcol] = "--"
        
        if move.piecemoved[1] == "p" and abs(move.startrow - move.endrow) == 2 :
            self.enpassant = ((move.startrow + move.endrow)//2 , move.startcol)
        else :
            self.enpassant = ()


        if move.iscastle :
            if move.endcol - move.startcol == 2 :
                self.board[move.endrow][move.endcol - 1] = self.board[move.endrow][move.endcol +1]
                self.board[move.endrow][move.endcol + 1] = "--"
            else:
                self.board[move.endrow][move.endcol + 1] = self.board[move.endrow][move.endcol - 2]
                self.board[move.endrow][move.endcol - 2] = "--"                

        self.updaterights(move)
        self.rightslogs.append(castlerights(self.currentrights.wks , self.currentrights.wqs , 
                                        self.currentrights.bks , self.currentrights.bqs))

        



    
    def undomove(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.startrow][move.startcol] = move.piecemoved
            self.board[move.endrow][move.endcol] = move.piececaptured
            self.whitetomove = not self.whitetomove 
            if move.piecemoved == "wK" :
                self.whitekingloc = (move.startrow , move.startcol)
            if move.piecemoved == "bK" :
                self.blackkingloc = (move.startrow , move.startcol)

        if move.isenpassant :
            self.board[move.endrow][move.endcol] = "--"
            self.board[move.startrow][move.startcol] = move.piecemoved
            if self.whitetomove:  # black just moved
                self.board[move.endrow + 1][move.endcol] = "bp"
            else:
                self.board[move.endrow - 1][move.endcol] = "wp"
            self.enpassant = (move.endrow, move.endcol)
        
        if move.piecemoved[1] == "p" and abs(move.startrow - move.endrow) == 2 :
            self.enpassant = ()
        

        self.rightslogs.pop()
        self.currentrights = self.rightslogs[-1]


        if move.iscastle :
            if move.endcol - move.startcol == 2 :
                self.board[move.endrow][move.endcol + 1] = self.board[move.endrow][move.endcol - 1]
                self.board[move.endrow][move.endcol - 1] = "--"
            else:
                self.board[move.endrow][move.endcol - 2] = self.board[move.endrow][move.endcol + 1]
                self.board[move.endrow][move.endcol + 1] = "--"
        
    
    def updaterights(self , move) :
        if move.piecemoved == "wK" :
            self.currentrights.wks = False
            self.currentrights.wqs = False
        elif move.piecemoved == "bK" :
            self.currentrights.bks = False
            self.currentrights.bqs = False
        elif move.piecemoved[1] == "R" :
            if move.startrow == 7 :
                if move.startcol == 0 :
                    self.currentrights.wqs = False
                elif move.startcol == 7:
                    self.currentrights.wks = False
            elif move.startrow == 0 :
                if move.startcol == 0 :
                    self.currentrights.bqs = False
                elif move.startcol == 7:
                    self.currentrights.bks = False

    
    
    
    def validmoves(self) :
        tenpassant = self.enpassant
        moves = []
        self.incheck , self.pins , self.checks = self.checkforpinsandchecks()
        if self.whitetomove:
            kingrow = self.whitekingloc[0]
            kingcol = self.whitekingloc[1]
        else:
            kingrow = self.blackkingloc[0]
            kingcol = self.blackkingloc[1]

        if self.incheck:
            if len(self.checks) == 1:
                moves = self.possiblemoves()
                check = self.checks[0]
                checkrow = check[0]
                checkcol = check[1]
                piecechecking = self.board[checkrow][checkcol]
                validsq = []
                if piecechecking[1] == "N":
                    validsq = [(checkrow , checkcol)]
                else :
                    for i in range(1,8) :
                        valid_sq = (kingrow + check[2] * i , kingcol + check[3] * i)
                        validsq.append(valid_sq)
                        if valid_sq[0] == checkrow and valid_sq[1] == checkcol :
                            break
                for i in range(len(moves) -1 , -1 , -1) :
                    if moves[i].piecemoved[1] != "K":
                        if not (moves[i].endrow , moves[i].endcol) in validsq:
                            moves.remove(moves[i])
            else:
                self.kingmoves(kingrow , kingcol , moves)
        else:
            moves = self.possiblemoves() 

        self.enpassant = tenpassant  

        if len(moves) == 0:
            if self.incheck == True :
                self.checkmate = True
            else :
                self.stalemate = True
                 
        
        return moves



    def SqUA(self,r,c):
        self.whitetomove = not self.whitetomove  # Switch turn to check from opponent's perspective
        opp_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col][1]
                color = self.board[row][col][0]
                if (color == "w" and self.whitetomove) or (color == "b" and not self.whitetomove):
                    if piece != "K":
                        self.movefunc[piece](row , col , opp_moves)
        self.whitetomove = not self.whitetomove  # Switch back
        for move in opp_moves:
            if move.endrow == r and move.endcol == c:
                return True
        return False



    def checkforpinsandchecks(self) :
        pins = [] 
        checks = []
        incheck = False
        if self.whitetomove:
            enemycolor = "b"
            allycolor = "w"
            startrow = self.whitekingloc[0]
            startcol = self.whitekingloc[1]
        else:
            enemycolor = "w"
            allycolor = "b"
            startrow = self.blackkingloc[0]
            startcol = self.blackkingloc[1]
        directions = ((1,0) , (0,1) , (-1 , 0) , (0 , -1) , (-1,-1) , (-1,1) , (1,-1) , (1 , 1) )
        for j in range(len(directions)):
            d = directions[j]
            possiblepins = ()
            for i in range(1,8):
                endrow = startrow + d[0] * i
                endcol = startcol + d[1] * i
                if 0 <= endrow < 8 and 0<= endcol <8 :
                    endpiece = self.board[endrow][endcol]
                    if endpiece[0] == allycolor :
                        if possiblepins == ():
                            possiblepins = (endrow , endcol , d[0] , d[1])
                        else :
                            break
                    elif endpiece[0] == enemycolor :
                        type = endpiece[1]
                        if (0 <= j <= 3 and type == "R") or (4 <= j <= 7 and type == "B") or (i == 1 and type == "p" and ((enemycolor == "w" and 6 <= j <=7) or (enemycolor == "b" and 4 <= j <=5))) or (type == "Q") or (i==1 and type == "K") :
                            if (possiblepins == ()) :
                                incheck = True 
                                checks.append((endrow , endcol , d[0] , d[1]))
                                break
                            else:
                                pins.append(possiblepins)
                                break
                        else:
                            break
                else:
                    break
        knightmoves = ((2,1) , (1,2) , (-1 , 2) , (2 , -1) , (-2 ,1) , (1,-2) , (-1,-2) , (-2,-1))
        for m in knightmoves:
            endrow = startrow + m[0]
            endcol = startcol + m[1]
            if 0<=endrow<8 and 0<= endcol < 8 :
                endpiece = self.board[endrow][endcol]
                if endpiece[0] == enemycolor and endpiece[1] == "N" :
                    incheck = True
                    checks.append((endrow , endcol , m[0] , m[1]))
        
        return incheck , pins , checks 
    
    
    
    
    def possiblemoves(self , inc_castle = True):
        moves = [] 
        
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whitetomove ) or (turn == 'b' and not self.whitetomove ) :
                    piece = self.board[r][c][1]
                    self.movefunc[piece](r,c,moves)
        return moves
                    
                   

    

    
    def pawnmoves(self , r , c , moves):
        piecepinned = False
        pindirection = ()
        for i in range(len(self.pins) -1 , -1 ,-1):
            if self.pins[i][0] == r and self.pins[i][1]==c :
                piecepinned = True
                pinsdirection = (self.pins[i][2] , self.pins[i][3])
                self.pins.remove(self.pins[i])
                break       
        
        
        if self.whitetomove :
            if self.board[r-1][c] == "--" :
                if not piecepinned or pinsdirection == (-1 , 0) :
                    moves.append(Move((r,c) , (r-1 , c), self.board))
                    if r == 6 and self.board[r-2][c] == "--":
                        moves.append(Move((r,c),(r-2 , c) , self.board))
            if c - 1 >= 0 :
                if self.board[r-1][c-1][0] == "b":
                    if not piecepinned or pinsdirection == (-1, -1):
                        moves.append(Move((r,c),(r-1 , c-1), self.board))
                elif (r-1 , c-1) == self.enpassant :
                    if not piecepinned or pinsdirection == (-1 , -1) :
                        moves.append(Move((r,c) , (r-1 , c-1) , self.board , enpassant = True))
            if c + 1 <= 7 :
                if self.board[r-1][c+1][0] == "b" :
                    if not piecepinned or pinsdirection == (-1 ,1 ) :
                        moves.append(Move((r,c), (r-1 , c + 1), self.board))
                elif (r-1 , c+1) == self.enpassant :
                    if not piecepinned or pinsdirection == (-1 , 1) :
                        moves.append(Move((r,c) , (r-1 , c+1) , self.board , enpassant = True))
        else :
            if self.board[r+1][c]== "--" :
                if not piecepinned or pinsdirection == (1,0):
                    moves.append(Move((r,c), (r+1 , c), self.board))
                    if r == 1 and self.board[r+2][c] == "--":
                        moves.append(Move((r,c),(r+2 , c) , self.board))
                
            if c - 1 >= 0 :
                if not piecepinned or pinsdirection == (1 , -1) :
                    if self.board[r+1][c-1][0] == "w" :
                        moves.append(Move((r,c), (r+1 , c - 1) , self.board))
                if (r+1 , c-1) == self.enpassant :
                    if not piecepinned or pinsdirection == (1 , -1) :
                        moves.append(Move((r,c) , (r+1 , c-1) , self.board , enpassant = True))
            if c+1 <= 7 :
                if not piecepinned or pinsdirection == (1,1):
                    if self.board[r+1][c+1][0] == "w" :
                        moves.append(Move((r,c) , (r + 1 , c + 1) , self.board))
                if (r+1 , c+1) == self.enpassant :
                    if not piecepinned or pinsdirection == (1 , 1) :
                        moves.append(Move((r,c) , (r+1 , c+1) , self.board , enpassant = True))
    
    
    
    
    
    
    def rookmoves(self , r , c , moves):
        piecepinned = False
        pinsdirection = ()
        for i in range(len(self.pins) -1 , -1 ,-1):
            if self.pins[i][0] == r and self.pins[i][1] ==c :
                piecepinned = True
                pinsdirection = (self.pins[i][2] , self.pins[i][3])
                if self.board[r][c][1] == "Q":    
                    self.pins.remove(self.pins[i])
                break  


        direction = ((-1 , 0) , (1 , 0) , (0 , 1 ) , (0 ,-1))
        color = "b" if self.whitetomove else "w"
        for d in direction :
            for i in range(1,8):
                endrow = r + d[0] * i 
                endcol = c + d[1] * i
                if 0 <= endrow < 8 and 0<= endcol <8 :
                    if not piecepinned or pinsdirection == d or pinsdirection == (-d[0] , -d[1]):
                        endpiece = self.board[endrow][endcol]
                        if endpiece == "--" :
                            moves.append(Move((r,c) , (endrow , endcol) , self.board))
                        elif endpiece[0] == color :
                            moves.append(Move((r,c) , (endrow , endcol) , self.board))
                            break
                        else:
                            break
                else:
                    break


   
   
   
   
    def knightmoves(self , r , c , moves) :
        piecepinned = False
        for i in range(len(self.pins) -1 , -1 ,-1):
            if self.pins[i][0] == r and self.pins[i][1] ==c :
                piecepinned = True
                self.pins.pop(i)
                break  
        points = ((r+2 , c + 1) , (r - 2 , c + 1) , (r + 2 , c -1 ) , (r - 2, c - 1),
                 (r+1 , c+2) , (r + 1 , c - 2) , (r - 1 , c + 2) , (r - 1 , c - 2))
        color = "b" if not self.whitetomove else "w"
        for p in points :
            row , col = p
            if 0 <= row < 8 and 0 <= col < 8 :
                if not piecepinned :
                    place = self.board[row][col]
                    if place[0] != color :
                        moves.append(Move((r,c) , (row , col) , self.board))
                    


    
    
    
    def kingmoves(self , r , c , moves , inc_castler = True) :
        color = "b" if not self.whitetomove else "w"
        rowmoves = (-1,-1,-1,0,0,1,1,1)
        colmoves = (-1,0,1,-1,1,-1,0,1)
        for i in range(8):
            endrow = r + rowmoves[i]
            endcol = c + colmoves[i]
            if 0 <= endrow < 8 and 0 <= endcol <8 :
                endpiece = self.board[endrow][endcol]
                if endpiece[0] != color:
                    if color == "w":
                        self.whitekingloc = (endrow , endcol)
                    else:
                        self.blackkingloc = (endrow , endcol)
                    incheck ,pins , checks = self.checkforpinsandchecks()
                    if not incheck:
                        moves.append(Move((r,c) , (endrow , endcol) , self.board))
                    if color == "w" :
                        self.whitekingloc = (r,c)
                    else:
                        self.blackkingloc = (r,c)
        
        if inc_castler:
            self.castlemove(r,c,moves, color)


    def castlemove(self , r , c , moves , allycolor):
        if self.incheck:
            return
        if (self.whitetomove and self.currentrights.wks) or (not self.whitetomove and self.currentrights.bks) :
            self.kingsidecastle(r, c , moves , allycolor)
        if (self.whitetomove and self.currentrights.wqs) or (not self.whitetomove and self.currentrights.bqs) :
            self.queensidecastle(r,c , moves , allycolor)


    def kingsidecastle(self , r , c ,moves , allycolor):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--" :
            if not self.SqUA(r,c+1)  and not self.SqUA(r,c+2) :
                moves.append(Move((r,c) , (r , c+2) , self.board , cancastle = True))





    def queensidecastle(self , r , c , moves , allycolor) :
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
            if not self.SqUA(r,c-1)  and not self.SqUA(r,c-2) :
                moves.append(Move((r,c) , (r , c-2) , self.board , cancastle = True))
                





    def queenmoves(self , r , c , moves) :
        self.rookmoves(r,c,moves)
        self.bishopmoves(r,c,moves)

 
    
    
    def bishopmoves(self , r , c , moves) :
        piecepinned = False
        pinsdirection = ()
        for i in range(len(self.pins) -1 , -1 ,-1):
            if self.pins[i][0] == r and self.pins[i][1] ==c :
                piecepinned = True
                pinsdirection = (self.pins[i][2] , self.pins[i][3])
                self.pins.remove(self.pins[i])
                break  
        direction = ((1,1) , (1,-1) , (-1,1) , (-1,-1))
        color = "b" if self.whitetomove else "w"
        for d in direction:
           for i in range(1,8) :
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if 0<= endrow < 8 and 0 <= endcol < 8 :
                    if not piecepinned or pinsdirection == d or pinsdirection == (-d[0] , -d[1]):
                        point = self.board[endrow][endcol] 
                        if point == "--" :
                            moves.append(Move((r,c) , (endrow , endcol) , self.board))
                        elif point[0] == color :
                            moves.append(Move((r,c) , (endrow , endcol) , self.board))
                            break
                        else:
                            break
                else :
                    break  
    
class castlerights:
    def __init__(self,wks,bks,wqs,bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


   
class Move():
    
    ranktorow = {"1":7, "2" : 6 , "3":5 , "4":4 , "5":3 , "6" :2 , "7": 1 , "8" :0}
    rowtorank = {v: k for k, v in ranktorow.items()} 
    filetocol = {"a" : 0 , "b" : 1 , "c" : 2 ,"d":3 ,"e":4,"f":5 , "g":6 , "h":7}
    coltofile = {v : k for k,v in filetocol.items()}
    
    def __init__(self, start , end , board , enpassant = False , cancastle = False):
        self.startrow = start[0]
        self.startcol = start[1]
        self.endrow = end[0]
        self.endcol = end[1]
        self.piecemoved = board[self.startrow ][self.startcol]
        self.piececaptured = board[self.endrow][ self.endcol]
        self.pawnpromoted = False
        self.isenpassant = enpassant
        if (self.piecemoved == "wp" and self.endrow == 0) or (self.piecemoved == "bp" and self.endrow == 7) :
            self.pawnpromoted = True
        self.moveID = self.startrow * 1000 + self.startcol * 100 + self.endrow * 10 + self.endcol 
        self.iscastle = cancastle
    def __eq__(self,other):
        if isinstance(other , Move) :
            return self.moveID == other.moveID
        return False



    def getchessNotation(self):
        return self.getrankfile(self.startrow , self.startcol) + self.getrankfile(self.endrow , self.endcol)
    
    def getrankfile(self , r , c ):
        return self.coltofile[c] + self.rowtorank[r]