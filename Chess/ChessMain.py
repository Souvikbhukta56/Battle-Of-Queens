import pygame as pg
import ChessEngine, getAImove
from time import sleep
from random import randint

pg.init()
pg.mixer.init()

WIDTH = 640
HEIGHT = 512
DIMENSIONS = 8
SQ_SIZE = HEIGHT // DIMENSIONS
MAX_FPS = 60
IMAGES = {}

# loading images
theme1 = pg.transform.scale(pg.image.load("images/chess_theme1.jpg"), (WIDTH, HEIGHT))
backIcon = pg.transform.scale(pg.image.load("images/back.png"), (SQ_SIZE - 20, SQ_SIZE - 20))
undo = pg.transform.scale(pg.image.load("images/undo.png"), (SQ_SIZE - 20, SQ_SIZE - 20))
settings1 = pg.transform.scale(pg.image.load("images/settings.png"), (SQ_SIZE - 20, SQ_SIZE - 20))
settings2 = pg.transform.scale(pg.image.load("images/settings.png"), (SQ_SIZE, SQ_SIZE))
welcome = pg.transform.scale(pg.image.load("images/welcome.png"), (WIDTH, HEIGHT))
forward = pg.image.load("images/forward.png")
backward = pg.image.load("images/backward.png")
restart_icon = pg.transform.scale(pg.image.load("images/restart.png"), (SQ_SIZE - 20, SQ_SIZE - 20))
pg.display.set_caption("Battle of Queens")

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
gs = ChessEngine.GameState()

playerOne = True
playerTwo = False

font1 = pg.font.SysFont('roman', 40)
font2=pg.font.SysFont('curlz', 40)
font3 = pg.font.SysFont('footlight', 27)
font4 = pg.font.SysFont('footlight', 40)
font5 = pg.font.SysFont("georgia", 35, bold=1)
font6=pg.font.SysFont('ravie', 30)
font7 = pg.font.SysFont('roman', 20)

steelBlue = pg.Color("linen")
blueViolet = pg.Color("blueviolet")
white = pg.Color("white")
black = pg.Color("black")
green = pg.Color("green")
orange = pg.Color("dodgerblue")
yellow = pg.Color("yellow")

pointer_color1 = orange
pointer_color2 = yellow
pointer_color3 = orange
pointer_color4 = yellow

level = 1
sound = True
color = "w"
flag1 = True

# themes init
wooden1 = [pg.Color("wheat"), pg.Color("chocolate")]
wooden2 = [pg.Color("burlywood"), pg.Color("saddlebrown")]
marine = [pg.Color("cyan"), pg.Color("royalblue")]
sky = [pg.Color("white"), pg.Color("deepskyblue")]
reddish = [pg.Color("bisque"), pg.Color("orangered")]
golden = [pg.Color("white"), pg.Color("gold")]
pinkish = [pg.Color("pink"), pg.Color("deeppink")]
greenary = [pg.Color("white"), pg.Color("green")]
grey = [pg.Color("white"), pg.Color("grey")]
theme = [wooden1, wooden2, marine, sky, reddish, golden, pinkish, greenary, grey]
themes = ["Wooden1", "Wooden2", "Marine", "Sky", "Reddish", "Golden", "Pinkish", "Greenary", "Grey"]
theme_index = randint(0,8)

def loadImages():
    pieces = ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load("images/"+piece+".png"), (SQ_SIZE, SQ_SIZE))
loadImages()

def highlightingSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
            s = pg.Surface((SQ_SIZE, SQ_SIZE))
            my_list = [(move.startRow, move.startCol) for move in validMoves]
            s.fill(pg.Color("yellow" if (r, c) in my_list else "red"))
            s.set_alpha(150)
            screen.blit(s, ((c + 1) * SQ_SIZE, r * SQ_SIZE))
            s.fill(pg.Color("blue"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, ((move.endCol + 1) * SQ_SIZE, move.endRow * SQ_SIZE))

def drawBoard(screen, gs, validMoves, sqSelected, theme_index):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = theme[theme_index][(r+c) % 2]
            pg.draw.rect(screen, color, pg.Rect((c+1) * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(SQ_SIZE, 0, HEIGHT, HEIGHT), 4)

    highlightingSquares(screen, gs, validMoves, sqSelected)
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = gs.board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pg.Rect((c + 1) * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def getPieceList():
    pieceList = []
    for r in range(8):
        for c in range(8):
            if gs.board[r][c] != "--" or gs.board[r][c][1] != 'K':
                pieceList.append(gs.board[r][c])
    return pieceList

def draw():
    if gs.STALEMATE:
        return [True, "Draw By Stalemate"]
    elif len(getPieceList()) <=2:
        l = getPieceList()
        if l==[] or l==['bN'] or l==['wN'] or l==['bB'] or l==['wB'] or (l[0][0]!=l[1][0] and ("bQ" not in l or 'wQ' not in l or 'wR' not in l or 'bR' not in l)):
            return [True, "By Insufficient Material"]
    return [False, " "]

def text_screen(text, color, x, y, font):
    screen_text=font.render(text, True, color)
    screen.blit(screen_text,[x, y])

def pawnPromotion(move):
    if move.pieceMoved[1] == "P":
        if move.endRow == 0 or move.endRow == 7:
            r = True
            while r:
                pg.draw.rect(screen, pg.Color("black"), pg.Rect(3 * SQ_SIZE, 3 * SQ_SIZE, 4 * SQ_SIZE, 3 * SQ_SIZE), border_radius=4)
                text_screen("Press 'q' for Queen", white, 3.5 * SQ_SIZE, 3.5 * SQ_SIZE, font3)
                text_screen("Press 'r' for Rook", white, 3.5 * SQ_SIZE, 4 * SQ_SIZE, font3)
                text_screen("Press 'b' for Bishop", white, 3.5 * SQ_SIZE, 4.5 * SQ_SIZE, font3)
                text_screen("Press 'k' for Knight", white, 3.5 * SQ_SIZE, 5 * SQ_SIZE, font3)
                for e in pg.event.get():
                    if e.type == pg.KEYDOWN:
                        if e.key == pg.K_q:
                            move.pieceMoved = move.pieceMoved[0] + "Q"
                        elif e.key == pg.K_r:
                            move.pieceMoved = move.pieceMoved[0] + "R"
                        elif e.key == pg.K_b:
                            move.pieceMoved = move.pieceMoved[0] + "B"
                        elif e.key == pg.K_k:
                            move.pieceMoved = move.pieceMoved[0] + "N"
                        move.promotedPawn = True
                        r = False
                pg.display.update()

def restart():
    global flag1
    gs.board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ]
    gs.whiteToMove = True
    gs.moveLog = []
    gs.whiteKingLocation = (7, 4)
    gs.blackKingLocation = (0, 4)
    gs.wkMoveLog = []
    gs.bkMoveLog = []
    gs.br1MoveLog = []
    gs.br2MoveLog = []
    gs.wr1MoveLog = []
    gs.wr2MoveLog = []
    gs.bkMoved = False
    gs.wkMoved = False
    gs.br1Moved = False
    gs.br2Moved = False
    gs.wr1Moved = False
    gs.wr2Moved = False
    gs.CHECKMATE = False
    gs.STALEMATE = False
    flag1 = True

def settings():
    global level
    global playerOne
    global playerTwo
    global running
    global running1
    global pointer_color1
    global pointer_color2
    global pointer_color3
    global pointer_color4
    global color
    global sound
    global t
    global theme_index
    runningSettings = True
    while runningSettings:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                runningSettings = False
                running = False
                running1 = False
            elif e.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()
                if 10 <= location[0] <= SQ_SIZE - 10 and 10 <= location[1] <= SQ_SIZE - 10:
                    runningSettings = False
                    if t == 1:
                        main()
                    elif t == 2:
                        gamePlay()
                if runningSettings:
                    if 4.5 * SQ_SIZE <= location[0] <= 6 * SQ_SIZE and .5 * SQ_SIZE <= location[1] <= 1.5 * SQ_SIZE:
                        color = "w"
                        pointer_color1 = orange
                        pointer_color2 = yellow
                    elif 6 * SQ_SIZE <= location[0] <= 7.5 * SQ_SIZE and .5 * SQ_SIZE <= location[1] <= 1.5 * SQ_SIZE:
                        color = "b"
                        pointer_color2 = orange
                        pointer_color1 = yellow
                    elif 4.5 * SQ_SIZE <= location[0] <= 5 * SQ_SIZE and 4.7 * SQ_SIZE <= location[1] <= 5.7 * SQ_SIZE:
                        if level > 1:
                            level -= 1
                    elif 6.9 * SQ_SIZE <= location[0] <= 7.4 * SQ_SIZE and 4.7 * SQ_SIZE <= location[1] <= 5.7 * SQ_SIZE:
                        if level < 4:
                            level += 1
                    elif 4.5 * SQ_SIZE <= location[0] <= 5 * SQ_SIZE and 6.7 * SQ_SIZE <= location[1] <= 7.7 * SQ_SIZE:
                        if theme_index >= 1:
                            theme_index -= 1
                    elif 6.9 * SQ_SIZE <= location[0] <= 7.4 * SQ_SIZE and 6.7 * SQ_SIZE <= location[1] <= 7.7 * SQ_SIZE:
                        if theme_index < 8:
                            theme_index += 1
                    elif 4.5 * SQ_SIZE <= location[0] <= 6 * SQ_SIZE and 2.5 * SQ_SIZE <= location[1] <= 3.5 * SQ_SIZE:
                        sound = True
                        pointer_color3 = orange
                        pointer_color4 = yellow
                    elif 6 * SQ_SIZE <= location[0] <= 7.5 * SQ_SIZE and 2.5 * SQ_SIZE <= location[1] <= 3.5 * SQ_SIZE:
                        sound = False
                        pointer_color4 = orange
                        pointer_color3 = yellow
        if runningSettings:
            screen.blit(welcome, pg.Rect(0, 0, WIDTH, HEIGHT))
            screen.blit(backIcon, pg.Rect(10, 10, SQ_SIZE - 20, SQ_SIZE - 20))

            pg.draw.rect(screen, green, pg.Rect(2 * SQ_SIZE, .5 * SQ_SIZE, 6 * SQ_SIZE, SQ_SIZE),
                         border_radius=15)
            text_screen("Play as ", black, 2.4 * SQ_SIZE, .75 * SQ_SIZE, font4)
            pg.draw.rect(screen, pointer_color1, pg.Rect(4.5 * SQ_SIZE, .5 * SQ_SIZE, 1.5 * SQ_SIZE, SQ_SIZE))
            text_screen("WHITE", black, 4.65 * SQ_SIZE, .85 * SQ_SIZE, font3)
            pg.draw.rect(screen, pointer_color2, pg.Rect(6 * SQ_SIZE, .5 * SQ_SIZE, 1.5 * SQ_SIZE, SQ_SIZE))
            text_screen("BLACK", black, 6.15 * SQ_SIZE, .85 * SQ_SIZE, font3)
            pg.draw.rect(screen, black, pg.Rect(2 * SQ_SIZE, .5 * SQ_SIZE, 6 * SQ_SIZE, SQ_SIZE), width=3,
                         border_radius=15)
            # -----------------------------------------------------
            pg.draw.rect(screen, green, pg.Rect(2 * SQ_SIZE, 2.5 * SQ_SIZE, 6 * SQ_SIZE, SQ_SIZE),
                         border_radius=15)

            text_screen("Sound ", black, 2.4 * SQ_SIZE, 2.75 * SQ_SIZE, font4)
            pg.draw.rect(screen, pointer_color3, pg.Rect(4.5 * SQ_SIZE, 2.5 * SQ_SIZE, 1.5 * SQ_SIZE, SQ_SIZE))
            text_screen("  ON", black, 4.65 * SQ_SIZE, 2.85 * SQ_SIZE, font3)
            pg.draw.rect(screen, pointer_color4, pg.Rect(6 * SQ_SIZE, 2.5 * SQ_SIZE, 1.5 * SQ_SIZE, SQ_SIZE))
            text_screen("  OFF", black, 6.15 * SQ_SIZE, 2.85 * SQ_SIZE, font3)
            pg.draw.rect(screen, black, pg.Rect(2 * SQ_SIZE, 2.5 * SQ_SIZE, 6 * SQ_SIZE, SQ_SIZE), width=3,
                         border_radius=15)

            # ------------------------------------------------------
            pg.draw.rect(screen, green, pg.Rect(2 * SQ_SIZE, 4.5 * SQ_SIZE, 6 * SQ_SIZE, SQ_SIZE),
                         border_radius=15)
            text_screen("Level ", black, 2.4 * SQ_SIZE, 4.75 * SQ_SIZE, font4)
            screen.blit(backward, pg.Rect(4.5 * SQ_SIZE, 4.7 * SQ_SIZE, .5 * SQ_SIZE, SQ_SIZE))
            pg.draw.rect(screen, orange, pg.Rect(5 * SQ_SIZE, 4.5 * SQ_SIZE, 2 * SQ_SIZE, SQ_SIZE))
            text_screen(str(level), black, 5.85 * SQ_SIZE, 4.75 * SQ_SIZE, font4)
            screen.blit(forward, pg.Rect(6.9 * SQ_SIZE, 4.7 * SQ_SIZE, .5 * SQ_SIZE, SQ_SIZE))
            pg.draw.rect(screen, black, pg.Rect(2 * SQ_SIZE, 4.5 * SQ_SIZE, 6 * SQ_SIZE, SQ_SIZE), width=3,
                         border_radius=15)

            # ------------------------------------------------------
            pg.draw.rect(screen, green, pg.Rect(2 * SQ_SIZE, 6.5 * SQ_SIZE, 6 * SQ_SIZE, SQ_SIZE),
                         border_radius=15)
            text_screen("Theme ", black, 2.4 * SQ_SIZE, 6.75 * SQ_SIZE, font4)
            screen.blit(backward, pg.Rect(4.5 * SQ_SIZE, 6.7 * SQ_SIZE, .5 * SQ_SIZE, SQ_SIZE))
            pg.draw.rect(screen, orange, pg.Rect(5 * SQ_SIZE, 6.5 * SQ_SIZE, 2 * SQ_SIZE, SQ_SIZE))
            text_screen(themes[theme_index], black, 5.0 * SQ_SIZE, 6.75 * SQ_SIZE, font4)
            screen.blit(forward, pg.Rect(6.9 * SQ_SIZE, 6.7 * SQ_SIZE, .5 * SQ_SIZE, SQ_SIZE))
            
            pg.draw.rect(screen, black, pg.Rect(2 * SQ_SIZE, 6.5 * SQ_SIZE, 6 * SQ_SIZE, SQ_SIZE), width=4,
                         border_radius=15)

            pg.display.update()
            if color == "w":
                playerOne = True
                playerTwo = False
            else:
                playerOne = False
                playerTwo = True

def main():
    global running
    global playerOne
    global playerTwo
    global sound
    global t

    running = True
    t = 1 # layer of the window
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            if e.type == pg.MOUSEBUTTONDOWN:
                loc = pg.mouse.get_pos()
                if 9 * SQ_SIZE <= loc[0] <= 10 * SQ_SIZE - 20 and 7 * SQ_SIZE <= loc[1] <= 8 * SQ_SIZE - 20:
                    settings()
                elif 2 * SQ_SIZE <= loc[0] <= 8 * SQ_SIZE and 4 * SQ_SIZE <= loc[1] <= 5 * SQ_SIZE:
                    t += 1
                    restart()
                    gamePlay()
                elif 2 * SQ_SIZE <= loc[0] <= 8 * SQ_SIZE and 6 * SQ_SIZE <= loc[1] <= 7 * SQ_SIZE:
                    t += 1
                    playerOne = True
                    playerTwo = True
                    restart()
                    gamePlay()

        screen.blit(welcome, pg.Rect(0, 0, WIDTH, HEIGHT))
        text_screen("Welcome To Battle Of Queens", black, 1.8 * SQ_SIZE, 20, font2)
        pg.draw.rect(screen, white, pg.Rect(2 * SQ_SIZE, 4 * SQ_SIZE, 6 * SQ_SIZE, SQ_SIZE), width=4,
                     border_radius=15)
        text_screen("Play with Computer", white, 2.5 * SQ_SIZE, 4.1 * SQ_SIZE, font1)
        pg.draw.rect(screen, white, pg.Rect(2 * SQ_SIZE, 6 * SQ_SIZE, 6 * SQ_SIZE, SQ_SIZE), width=4,
                     border_radius=15)
        text_screen("Local Multiplayer", white, 2.75 * SQ_SIZE, 6.1 * SQ_SIZE, font1)
        text_screen("Developed by Souvik Bhukta ", white, .2 * SQ_SIZE, 7.5 * SQ_SIZE, font7)
        screen.blit(settings1, pg.Rect(9 * SQ_SIZE, 7 * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        clock.tick(MAX_FPS)
        pg.display.flip()


def gamePlay():
    global t
    global running
    global flag1
    global playerTwo
    global playerOne
    screen.blit(theme1, pg.Rect(0, 0, WIDTH, HEIGHT))
    screen.blit(backIcon, pg.Rect(10, 10, SQ_SIZE - 20, SQ_SIZE - 20))
    screen.blit(undo, pg.Rect(9 * SQ_SIZE + 10, 10, SQ_SIZE - 20, SQ_SIZE - 20))
    screen.blit(restart_icon, pg.Rect(10, SQ_SIZE + 10, SQ_SIZE - 20, SQ_SIZE - 20))
    if not (playerTwo and playerOne):
        screen.blit(settings1, pg.Rect(9 * SQ_SIZE + 10, SQ_SIZE + 10, SQ_SIZE - 20, SQ_SIZE - 20))
    global running1
    running1 = True
    sq_selected = ()
    player_clicks = []
    validMoves = gs.getValidMoves() + gs.castling()
    moveMade = False
    while running1:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running1 = False
                running = False

            elif e.type == pg.MOUSEBUTTONDOWN:
                if 10 <= pg.mouse.get_pos()[0] <= SQ_SIZE - 10 and 10 <= pg.mouse.get_pos()[1] <= SQ_SIZE - 10:
                    running1 = False
                    t -= 1
                    if playerOne and playerTwo:
                        playerOne = True
                        playerTwo = False
                elif 9 * SQ_SIZE + 10 <= pg.mouse.get_pos()[0] <= 10 * SQ_SIZE - 10 and SQ_SIZE + 10 <= pg.mouse.get_pos()[1] <= 2 * SQ_SIZE - 10:
                    if not (playerTwo and playerOne):
                        settings()
                elif 9 * SQ_SIZE + 10 <= pg.mouse.get_pos()[0] <= 10 * SQ_SIZE - 10 and 10 <= pg.mouse.get_pos()[1] <= SQ_SIZE - 10:
                    if playerTwo and playerOne:
                        gs.undoMove()
                    elif not (playerOne and playerTwo):
                        gs.undoMove()
                        gs.undoMove()
                    moveMade = True
                    flag1 = True
                elif 10 <= pg.mouse.get_pos()[0] <= SQ_SIZE - 10 and SQ_SIZE + 10 <= pg.mouse.get_pos()[1] <= 2 * SQ_SIZE - 10:
                    restart()
                    validMoves = gs.getValidMoves() + gs.castling()
                    humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)

                else:
                    if running1:
                        if humanTurn:
                            location = pg.mouse.get_pos()
                            col = (location[0] - 64) // SQ_SIZE
                            row = location[1] // SQ_SIZE
                            if  0 <= row <=7 and 0 <= col <=7:
                                if sq_selected == (row, col):
                                    sq_selected = ()
                                    player_clicks = []
                                elif sq_selected == () and ((gs.whiteToMove and gs.board[row][col][0] == "w") or (not gs.whiteToMove and gs.board[row][col][0] == "b")):
                                    sq_selected = (row, col)
                                    player_clicks.append(sq_selected)
                                elif sq_selected != ():
                                    if ((gs.whiteToMove and gs.board[row][col][0] == "w") or (not gs.whiteToMove and gs.board[row][col][0] == "b")):
                                        sq_selected = (row, col)
                                        player_clicks[0] = (row, col)
                                    else:
                                        sq_selected = (row, col)
                                        player_clicks.append(sq_selected)

                            if len(player_clicks) == 2 and (not gs.CHECKMATE or not gs.STALEMATE):  # making move
                                move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                                if move in validMoves:
                                    pawnPromotion(move)
                                    gs.makeMove(move)
                                    moveMade = True
                                    if moveMade:
                                        if sound:
                                            pg.mixer.music.load("pieceMove.wav")
                                            pg.mixer.music.play()
                                    if move.enPassant == True:
                                        gs.board[gs.moveLog[-2].endRow][gs.moveLog[-2].endCol] = "--"
                                sq_selected = ()
                                player_clicks = []

            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_u:
                    if playerTwo and playerOne:
                        gs.undoMove()

                    elif not (playerOne and playerTwo):
                        gs.undoMove()
                        gs.undoMove()
                    moveMade = True
        if running1:
            if moveMade:
                validMoves = gs.getValidMoves() + gs.castling()
                gs.checkMate(validMoves)
                moveMade = False

            if not humanTurn:
                if gs.STALEMATE:
                    a=2
                elif not gs.CHECKMATE:
                    move = getAImove.findBestMove(gs, validMoves, level - 1)
                    if move is None:
                        move = getAImove.getRandomMove(validMoves)
                    if 1 <= level <= 2:
                        sleep(0.8)
                    pawnPromotion(move)
                    gs.makeMove(move)
                    if sound:
                        pg.mixer.music.load("pieceMove.wav")
                        pg.mixer.music.play()
                    moveMade = True
                    if move.enPassant == True:
                        gs.board[gs.moveLog[-2].endRow][gs.moveLog[-2].endCol] = "--"
                    if move.pieceMoved == "wK":
                        gs.wkMoved = True
                        gs.wkMoveLog.append(move)
                        if move.startCol - move.endCol == 2:
                            gs.board[7][0] = "--"
                            gs.board[move.endRow][move.endCol + 1] = "wR"
                        if move.startCol - move.endCol == -2:
                            gs.board[7][7] = "--"
                            gs.board[move.endRow][move.endCol - 1] = "wR"

                    elif move.pieceMoved == "bK":
                        gs.bkMoved = True
                        gs.bkMoveLog.append(move)
                        if move.startCol - move.endCol == 2:
                            gs.board[0][0] = "--"
                            gs.board[move.endRow][move.endCol + 1] = "bR"
                        if move.startCol - move.endCol == -2:
                            gs.board[0][7] = "--"
                            gs.board[move.endRow][move.endCol - 1] = "bR"

                    elif move.pieceMoved == "bR" and move.startRow == 0 and move.startCol == 0:
                        gs.br1Moved = True
                        gs.br1MoveLog.append(move)
                    elif move.pieceMoved == "bR" and move.startRow == 0 and move.startCol == 7:
                        gs.br2Moved = True
                        gs.br2MoveLog.append(move)
                    elif move.pieceMoved == "wR" and move.startRow == 7 and move.startCol == 0:
                        gs.wr1Moved = True
                        gs.wr1MoveLog.append(move)
                    elif move.pieceMoved == "wR" and move.startRow == 7 and move.startCol == 7:
                        gs.wr2Moved = True
                        gs.wr2MoveLog.append(move)

            if moveMade:
                validMoves = gs.getValidMoves() + gs.castling()
                gs.checkMate(validMoves)
                moveMade = False

            Draw = draw()
            if gs.CHECKMATE:
                pg.draw.rect(screen, pg.Color("darkblue"),
                             pg.Rect(2.7 * SQ_SIZE, 2.7 * SQ_SIZE, 4.6 * SQ_SIZE, 2.6 * SQ_SIZE), border_radius=5)
                text_screen("GAME OVER", yellow, 4 * SQ_SIZE, 3 * SQ_SIZE, font6)
                text_screen("Checkmate", pg.Color("orange"), 4.2 * SQ_SIZE, 3.8 * SQ_SIZE, font3)
                if gs.whiteToMove:
                    text_screen("Black Wins!", white, 3.3 * SQ_SIZE, 4.5 * SQ_SIZE, font5)
                else:
                    text_screen("White Wins!", white, 3.3 * SQ_SIZE, 4.5 * SQ_SIZE, font5)
                if flag1:
                    if sound:
                        pg.mixer.music.load("game-over.wav")
                        pg.mixer.music.play()
                    flag1 = False
                pg.display.update()
                pg.display.flip()

            elif Draw[0]:
                pg.draw.rect(screen, pg.Color("darkblue"),
                             pg.Rect(2.7 * SQ_SIZE, 2.7 * SQ_SIZE, 4.6 * SQ_SIZE, 2.6 * SQ_SIZE), border_radius=5)
                text_screen("GAME OVER", yellow, 4 * SQ_SIZE, 3 * SQ_SIZE, font6)
                screen_text1 = font5.render("Draw!", True, white)
                text_rect1 = screen_text1.get_rect(center = (WIDTH/2, 3.8 * SQ_SIZE))
                screen.blit(screen_text1, text_rect1)
                screen_text2 = font3.render(Draw[1], True, pg.Color("orange"))
                text_rect2 = screen_text2.get_rect(center=(WIDTH / 2, 4.5 * SQ_SIZE))
                screen.blit(screen_text2, text_rect2)
                if flag1:
                    if sound:
                        pg.mixer.music.load("game-over.wav")
                        pg.mixer.music.play()
                    flag1 = False
                pg.display.update()
                pg.display.flip()

            drawBoard(screen, gs, validMoves, sq_selected, theme_index)
            clock.tick(MAX_FPS)
            pg.display.flip()
Checkmate=0
if __name__ == "__main__":
    main()