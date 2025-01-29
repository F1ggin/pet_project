class Piece:
    def __init__(self, color):
        self.color = color

    def can_move(self, board, start, end):
        # Базовая логика, которая будет переопределена в наследниках
        pass


class Pawn(Piece):
    def __str__(self):
        return 'P' if self.color == 'white' else 'p'

    def can_move(self, board, start, end):
        start_col, start_row = ord(start[0]) - ord('a'), 8 - int(start[1])
        end_col, end_row = ord(end[0]) - ord('a'), 8 - int(end[1])

        if self.color == 'white':
            if start_col == end_col and start_row == 6 and end_row == 4 and board[end_row][end_col] == '.':
                return True
            if start_col == end_col and end_row == start_row - 1 and board[end_row][end_col] == '.':
                return True
            if abs(start_col - end_col) == 1 and end_row == start_row - 1 and board[end_row][end_col] != '.' and \
                    board[end_row][end_col].color != self.color:
                return True
        else:
            if start_col == end_col and start_row == 1 and end_row == 3 and board[end_row][end_col] == '.':
                return True
            if start_col == end_col and end_row == start_row + 1 and board[end_row][end_col] == '.':
                return True
            if abs(start_col - end_col) == 1 and end_row == start_row + 1 and board[end_row][end_col] != '.' and \
                    board[end_row][end_col].color != self.color:
                return True

        return False


class Rook(Piece):
    def __str__(self):
        return 'R' if self.color == 'white' else 'r'

    def can_move(self, board, start, end):
        start_col, start_row = ord(start[0]) - ord('a'), 8 - int(start[1])
        end_col, end_row = ord(end[0]) - ord('a'), 8 - int(end[1])

        # Ладья должна двигаться только по прямой (либо по вертикали, либо по горизонтали)
        if start_col == end_col or start_row == end_row:
            # Проверим, что между начальной и конечной позицией нет препятствий
            step_col = (end_col - start_col) // max(1, abs(end_col - start_col)) if start_col != end_col else 0
            step_row = (end_row - start_row) // max(1, abs(end_row - start_row)) if start_row != end_row else 0
            current_col, current_row = start_col + step_col, start_row + step_row
            while current_col != end_col or current_row != end_row:
                if board[current_row][current_col] != '.':
                    return False
                current_col += step_col
                current_row += step_row
            if board[end_row][end_col] == '.' or board[end_row][end_col].color != self.color:
                return True
        return False


class Knight(Piece):
    def __str__(self):
        return 'N' if self.color == 'white' else 'n'

    def can_move(self, board, start, end):
        start_col, start_row = ord(start[0]) - ord('a'), 8 - int(start[1])
        end_col, end_row = ord(end[0]) - ord('a'), 8 - int(end[1])
        delta_col, delta_row = abs(end_col - start_col), abs(end_row - start_row)
        if (delta_col == 2 and delta_row == 1) or (delta_col == 1 and delta_row == 2):
            if board[end_row][end_col] == '.' or board[end_row][end_col].color != self.color:
                return True
        return False


class Bishop(Piece):
    def __str__(self):
        return 'B' if self.color == 'white' else 'b'

    def can_move(self, board, start, end):
        start_col, start_row = ord(start[0]) - ord('a'), 8 - int(start[1])
        end_col, end_row = ord(end[0]) - ord('a'), 8 - int(end[1])

        # Слон ходит по диагонали, проверяем разницу в строках и колонках
        if abs(start_row - end_row) == abs(start_col - end_col):
            # Проверяем, что путь свободен
            step_row = 1 if end_row > start_row else -1
            step_col = 1 if end_col > start_col else -1
            current_row, current_col = start_row + step_row, start_col + step_col

            while current_row != end_row and current_col != end_col:
                if board[current_row][current_col] != '.':
                    return False
                current_row += step_row
                current_col += step_col

            # Если клетка конечная свободна или там фигура противника
            if board[end_row][end_col] == '.' or board[end_row][end_col].color != self.color:
                return True

        return False


class Queen(Piece):
    def __str__(self):
        return 'Q' if self.color == 'white' else 'q'

    def can_move(self, board, start, end):
        start_col, start_row = ord(start[0]) - ord('a'), 8 - int(start[1])
        end_col, end_row = ord(end[0]) - ord('a'), 8 - int(end[1])

        # Королева ходит как слон или как ладья
        if abs(start_row - end_row) == abs(start_col - end_col):
            # Логика диагонального хода, как у слона
            step_row = 1 if end_row > start_row else -1
            step_col = 1 if end_col > start_col else -1
            current_row, current_col = start_row + step_row, start_col + step_col

            while current_row != end_row and current_col != end_col:
                if board[current_row][current_col] != '.':
                    return False
                current_row += step_row
                current_col += step_col

            # Проверка конечной клетки
            if board[end_row][end_col] == '.' or board[end_row][end_col].color != self.color:
                return True

        # Логика вертикального или горизонтального хода (как у ладьи)
        if start_row == end_row or start_col == end_col:
            if start_row == end_row:  # Горизонтальный ход
                step = 1 if end_col > start_col else -1
                for col in range(start_col + step, end_col, step):
                    if board[start_row][col] != '.':
                        return False
            else:  # Вертикальный ход
                step = 1 if end_row > start_row else -1
                for row in range(start_row + step, end_row, step):
                    if board[row][start_col] != '.':
                        return False

            if board[end_row][end_col] == '.' or board[end_row][end_col].color != self.color:
                return True

        return False


class King(Piece):
    def __str__(self):
        return 'K' if self.color == 'white' else 'k'

    def can_move(self, board, start, end):
        start_col, start_row = ord(start[0]) - ord('a'), 8 - int(start[1])
        end_col, end_row = ord(end[0]) - ord('a'), 8 - int(end[1])

        # Король может ходить на одну клетку в любом направлении
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            # Конечная клетка должна быть свободна или занята фигурой противника
            if board[end_row][end_col] == '.' or board[end_row][end_col].color != self.color:
                return True

        return False


class Board:
    def __init__(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.setup_pieces()

    def setup_pieces(self):
        # Устанавливаем пешки
        for i in range(8):
            self.board[1][i] = Pawn('black')
            self.board[6][i] = Pawn('white')

        # Устанавливаем остальные фигуры
        self.board[0] = [Rook('black'), Knight('black'), Bishop('black'), Queen('black'), King('black'),
                         Bishop('black'), Knight('black'), Rook('black')]
        self.board[7] = [Rook('white'), Knight('white'), Bishop('white'), Queen('white'), King('white'),
                         Bishop('white'), Knight('white'), Rook('white')]

    def __str__(self):
        result = "   A B C D E F G H\n\n"
        for i, row in enumerate(self.board):
            result += f"{8 - i}  " + ' '.join([str(piece) if piece != '.' else '.' for piece in row]) + f"  {8 - i}\n"
        result += "\n   A B C D E F G H\n"
        return result

    def move_piece(self, start, end):
        start_col, start_row = ord(start[0]) - ord('a'), 8 - int(start[1])
        end_col, end_row = ord(end[0]) - ord('a'), 8 - int(end[1])

        piece = self.board[start_row][start_col]
        if piece == '.':
            return "Error. Type: The piece cannot make the specified move."

        if not piece.can_move(self.board, start, end):
            return "Error. Type: The piece cannot make the specified move."

        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = '.'
        return None

    # Метод для подсчета количества белых фигур
    def num_white_pieces(self):
        count = 0
        for row in self.board:
            for piece in row:
                if piece != '.' and piece.color == 'white':
                    count += 1
        return count

    # Метод для подсчета количества черных фигур
    def num_black_pieces(self):
        count = 0
        for row in self.board:
            for piece in row:
                if piece != '.' and piece.color == 'black':
                    count += 1
        return count

    # Метод для расчета баланса
    def balance(self, color):
        white_score = 0
        black_score = 0

        # Стоимость фигур
        piece_values = {
            'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9,  # Черные фигуры
            'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9  # Белые фигуры
        }

        # Проходим по доске и подсчитываем очки для каждой фигуры
        for row in self.board:
            for piece in row:
                if piece != '.':
                    value = piece_values.get(str(piece).lower(), 0)
                    if piece.color == 'white':
                        white_score += value
                    else:
                        black_score += value

        # Возвращаем баланс в зависимости от цвета
        if color == 'white':
            return white_score - black_score
        elif color == 'black':
            return black_score - white_score


class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'white'
        self.move_count = 1
        self.black_move_count = 1

    def draw(self):
        print(self.board)

    def move(self, command):
        move_error = self.board.move_piece(command[:2], command[3:])
        if move_error:
            print(move_error)
        else:
            self.turn = 'black' if self.turn == 'white' else 'white'
            self.move_count += 1
        if self.turn == 'white':
            print(f"{self.turn} {(self.move_count // 2) + 1}:")
        else:
            print(f"{self.turn} {(self.move_count // 2)}:")

    def play(self):
        print(f"{self.turn} 1:")
        while True:
            command = input()
            if command == 'draw':
                self.draw()
                if self.turn == 'white':
                    print(f"{self.turn} {(self.move_count // 2) + 1}:")
                else:
                    print(f"{self.turn} {(self.move_count // 2)}:")

            elif command == 'exit':
                break
            elif command.startswith('balance white'):
                balance = self.board.balance('white')
                print(f"{balance}")
                if self.turn == 'white':
                    print(f"{self.turn} {(self.move_count // 2) + 1}:")
                else:
                    print(f"{self.turn} {(self.move_count // 2)}:")
            elif command.startswith('balance black'):
                balance = self.board.balance('black')
                print(f"{balance}")
                if self.turn == 'white':
                    print(f"{self.turn} {(self.move_count // 2) + 1}:")
                else:
                    print(f"{self.turn} {(self.move_count // 2)}:")
            elif len(command) == 5 and command[2] == '-' and command[1] in '12345678' and command[0] in 'abcdefgh' and command[4] in '12345678' and command[3] in 'abcdefgh':
                self.move(command)
            else:
                print("Error. Type: Wrong input format.")
                if self.turn == 'white':
                    print(f"{self.turn} {(self.move_count // 2) + 1}:")
                else:
                    print(f"{self.turn} {(self.move_count // 2)}:")


if __name__ == "__main__":
    game = Game()
    game.play()
