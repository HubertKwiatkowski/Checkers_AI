import pygame
from .constants import BLACK, RED, WHITE, ROWS, COLS, SQUARE_SIZE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0

        self.create_board()

    def draw_squares(self, win):
        # draw checker board
        win.fill(BLACK)
        for row in range(ROWS):
            """
            rysuje czerwone pola zaczynajac od pierwszego jesli modulo bedzie 0
            lub od drugiego jesli modulo bedzie 1, i przeskakuje o 2 pola
            poczatek range - modulo
            koniec range - ROWS
            skok - 2
            """
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED,
                    (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                )

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        """Usuwa pionek nad ktorym przeskoczyl nasz pionek"""
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED

        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            """
            czerwone ida do gory:
            row -1 sprawdza rzad bezposrednio nad wybranym elementem
            max(row-3, -1) - wybiera nawyzsza wartosc - albo dwa rzedy nad wybranym elementem,
                albo koniec planszy
            -1 - przesuniecie o tyle rzedow do gory
            piece.color - kolor wybranego elementu (?)
            left - pierwszy kierunek przesuniecia elementu
            """
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))

        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), +1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), +1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0: #jesli znalazl puste pole
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped=last))
                break
            elif current.color == color:
                #jesli pole jest zajete przez ten sam kolor - nie mozemy sie ruszac
                break
            else:
                #w pozostalych przypadkach sprawdza, czy kolejne pole jest puste, zeby przeskoczyc nad elementem przeciwnika
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0: #jesli znalazl puste pole
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped=last))
                break
            elif current.color == color:
                #jesli pole jest zajete przez ten sam kolor - nie mozemy sie ruszac
                break
            else:
                #w pozostalych przypadkach sprawdza, czy kolejne pole jest puste, zeby przeskoczyc nad elementem przeciwnika
                last = [current]

            right += 1

        return moves
