# Инициализация шахматной доски
def create_chess_board():
    chess_board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    ]
    return chess_board


# Функция для отображения шахматной доски
def display_board(chess_board):
    print("\n   A B C D E F G H\n")
    for index, row in enumerate(chess_board):
        print(f"{8 - index}  {' '.join(row)}  {8 - index}")
    print("\n   A B C D E F G H\n")


# Преобразование координат в числовые индексы
def transform_coords(coordinate):
    column_index = ord(coordinate[0]) - ord('a')
    row_index = 8 - int(coordinate[1])
    return column_index, row_index


# Проверка формата ввода
def validate_input_format(move_command):
    if len(move_command) == 5 and move_command[2] == '-':
        start, end = move_command[:2], move_command[3:]
        if (start[0] in 'abcdefgh' and start[1] in '12345678' and
                end[0] in 'abcdefgh' and end[1] in '12345678'):
            return True
    return False


# Функция для проверки свободного пути
def is_path_clear(board, start_row, start_col, end_row, end_col):
    if start_col == end_col:  # Вертикальный ход
        step = 1 if end_row > start_row else -1
        for row in range(start_row + step, end_row, step):
            if board[row][start_col] != '.':
                return False
    elif start_row == end_row:  # Горизонтальный ход
        step = 1 if end_col > start_col else -1
        for col in range(start_col + step, end_col, step):
            if board[start_row][col] != '.':
                return False
    elif abs(start_row - end_row) == abs(start_col - end_col):  # Диагональный ход
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        for i in range(1, abs(end_row - start_row)):
            if board[start_row + i * row_step][start_col + i * col_step] != '.':
                return False
    return True


# Проверка корректности хода пешки
def validate_pawn_move(board, start, end, player_color):
    start_col, start_row = transform_coords(start)
    end_col, end_row = transform_coords(end)
    pawn_piece = board[start_row][start_col]

    if player_color == 'white' and pawn_piece == 'P':
        if end_col == start_col and board[end_row][end_col] == '.':
            if end_row == start_row - 1:  # На одну клетку вперёд
                return True
            if start_row == 6 and end_row == start_row - 2 and board[end_row + 1][end_col] == '.':
                return True  # На две клетки вперёд
        if abs(end_col - start_col) == 1 and end_row == start_row - 1 and board[end_row][end_col].islower():
            return True  # Взятие фигуры
    elif player_color == 'black' and pawn_piece == 'p':
        if end_col == start_col and board[end_row][end_col] == '.':
            if end_row == start_row + 1:  # На одну клетку вперёд
                return True
            if start_row == 1 and end_row == start_row + 2 and board[end_row - 1][end_col] == '.':
                return True  # На две клетки вперёд
        if abs(end_col - start_col) == 1 and end_row == start_row + 1 and board[end_row][end_col].isupper():
            return True  # Взятие фигуры
    return False


# Проверка корректности хода ладьи
def validate_rook_move(board, start, end):
    start_col, start_row = transform_coords(start)
    end_col, end_row = transform_coords(end)
    return (start_col == end_col or start_row == end_row) and is_path_clear(board, start_row, start_col, end_row, end_col)


# Проверка корректности хода слона
def validate_bishop_move(board, start, end):
    start_col, start_row = transform_coords(start)
    end_col, end_row = transform_coords(end)
    return abs(start_row - end_row) == abs(start_col - end_col) and is_path_clear(board, start_row, start_col, end_row, end_col)


# Проверка корректности хода ферзя
def validate_queen_move(board, start, end):
    return validate_rook_move(board, start, end) or validate_bishop_move(board, start, end)


# Проверка корректности хода коня
def validate_knight_move(board, start, end):
    start_col, start_row = transform_coords(start)
    end_col, end_row = transform_coords(end)
    return (abs(start_col - end_col) == 2 and abs(start_row - end_row) == 1) or \
           (abs(start_col - end_col) == 1 and abs(start_row - end_row) == 2)


# Проверка корректности хода короля
def validate_king_move(board, start, end):
    start_col, start_row = transform_coords(start)
    end_col, end_row = transform_coords(end)
    return abs(start_col - end_col) <= 1 and abs(start_row - end_row) <= 1


# Проверка корректности хода любой фигуры
def is_move_valid(board, start, end, player_color):
    start_col, start_row = transform_coords(start)
    end_col, end_row = transform_coords(end)
    piece = board[start_row][start_col]

    if player_color == 'white' and piece.islower():
        return False  # На стартовой позиции белых должна быть белая фигура
    if player_color == 'black' and piece.isupper():
        return False  # На стартовой позиции черных должна быть черная фигура

    # Нельзя двигаться на клетку с фигурой того же цвета
    if (player_color == 'white' and board[end_row][end_col].isupper()) or \
            (player_color == 'black' and board[end_row][end_col].islower()):
        return False

    if piece.lower() == 'p':  # Пешка
        return validate_pawn_move(board, start, end, player_color)
    if piece.lower() == 'r':  # Ладья
        return validate_rook_move(board, start, end)
    if piece.lower() == 'n':  # Конь
        return validate_knight_move(board, start, end)
    if piece.lower() == 'b':  # Слон
        return validate_bishop_move(board, start, end)
    if piece.lower() == 'q':  # Ферзь
        return validate_queen_move(board, start, end)
    if piece.lower() == 'k':  # Король
        return validate_king_move(board, start, end)
    return False


# Функция для выполнения хода
def execute_move(board, start, end):
    start_col, start_row = transform_coords(start)
    end_col, end_row = transform_coords(end)
    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = '.'


# Главный игровой цикл
# Функция для получения всех возможных ходов для фигуры
def get_possible_moves(board, start, player_color):
    possible_moves = []
    start_col, start_row = transform_coords(start)
    piece = board[start_row][start_col]

    if piece == '.':  # Если на выбранной клетке нет фигуры
        return possible_moves

    for row in range(8):
        for col in range(8):
            end = f"{chr(col + ord('a'))}{8 - row}"
            if is_move_valid(board, start, end, player_color):
                possible_moves.append(end)

    possible_moves.sort()  # Сортируем по алфавиту
    return possible_moves


# Функция для получения всех фигур противника, которые можно взять
def get_capturable_pieces(board, start, player_color):
    capturable_pieces = []
    start_col, start_row = transform_coords(start)
    piece = board[start_row][start_col]

    if piece == '.':  # Если на выбранной клетке нет фигуры
        return capturable_pieces

    for row in range(8):
        for col in range(8):
            end = f"{chr(col + ord('a'))}{8 - row}"
            if is_move_valid(board, start, end, player_color):
                # Проверяем, что на клетке есть фигура противника
                end_piece = board[8 - int(end[1])][ord(end[0]) - ord('a')]
                if (player_color == 'white' and end_piece.islower()) or (
                        player_color == 'black' and end_piece.isupper()):
                    capturable_pieces.append(end)

    capturable_pieces.sort()  # Сортируем по алфавиту
    return capturable_pieces


# Главный игровой цикл с добавлением новых команд
def start_game():
    chess_board = create_chess_board()
    turn_count = 1
    active_player = 'white'

    while True:
        print(f"{active_player} {turn_count}:")
        user_command = input().strip()

        if user_command == "exit":
            break
        elif user_command == "draw":
            display_board(chess_board)
            continue

        # Если команда формата xi-, запрашиваем возможные ходы для выбранной фигуры
        if len(user_command) == 3 and user_command[2] == '-':
            source = user_command[:2]
            possible_moves = get_possible_moves(chess_board, source, active_player)
            if possible_moves:
                print(f"possible moves: {', '.join(possible_moves)}")
            else:
                print("possible moves: none")
            continue

        # Если команда формата xi, запрашиваем фигуры противника, которые можно взять
        if len(user_command) == 2:
            source = user_command[:2]
            capturable_pieces = get_capturable_pieces(chess_board, source, active_player)
            if capturable_pieces:
                print(f"enemy figures under attack: {', '.join(capturable_pieces)}")
            else:
                print("enemy figures under attack: none")
            continue

        # Проверка формата хода
        if not validate_input_format(user_command):
            print("Error. Type: Wrong input format.")
            continue

        source, destination = user_command[:2], user_command[3:]

        # Проверка корректности хода
        if not is_move_valid(chess_board, source, destination, active_player):
            print("Error. Type: The piece cannot make the specified move.")
            continue

        # Выполнение хода
        execute_move(chess_board, source, destination)

        # Переход к следующему ходу
        active_player = 'black' if active_player == 'white' else 'white'
        if active_player == 'white':
            turn_count += 1


if __name__ == "__main__":
    start_game()
