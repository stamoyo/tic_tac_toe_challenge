import numpy as np

OPPONENT = -1
COMPUTER = 1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]


def get_score(current_board):
    if is_player_winning(current_board, COMPUTER):
        score = 1
    elif is_player_winning(current_board, OPPONENT):
        score = -1
    else:
        score = 0
    return score


def is_player_winning(current_board, player):
    current_board_combinations = [
        [current_board[0][0], current_board[0][1], current_board[0][2]],
        [current_board[1][0], current_board[1][1], current_board[1][2]],
        [current_board[2][0], current_board[2][1], current_board[2][2]],
        [current_board[0][0], current_board[1][0], current_board[2][0]],
        [current_board[0][1], current_board[1][1], current_board[2][1]],
        [current_board[0][2], current_board[1][2], current_board[2][2]],
        [current_board[0][0], current_board[1][1], current_board[2][2]],
        [current_board[2][0], current_board[1][1], current_board[0][2]],
    ]
    winning_combination = [player]*3
    if winning_combination in current_board_combinations:
        return True
    else:
        return False


def game_over(current_board):
    return is_player_winning(current_board, OPPONENT) or is_player_winning(current_board, COMPUTER)


def free_positions(current_board):
    coordinates = []
    for row_n, row in enumerate(current_board):
        for position_n, position in enumerate(row):
            if position == 0:
                coordinates.append([row_n, position_n])
    return coordinates


def set_move(x, y, player):
    if [x, y] in free_positions(board):
        board[x][y] = player
        return True
    else:
        return False


def minimax(current_board, depth, player):
    if player == COMPUTER:
        moves_and_score = [-1, -1, -np.inf]
    else:
        moves_and_score = [-1, -1, +np.inf]

    if depth == 0 or game_over(current_board):
        score = get_score(current_board)
        return [-1, -1, score]

    for position in free_positions(current_board):
        x, y = position[0], position[1]
        current_board[x][y] = player
        moves_and_score_candidate = minimax(current_board, depth - 1, -player)
        current_board[x][y] = 0
        moves_and_score_candidate[0], moves_and_score_candidate[1] = x, y

        if player == COMPUTER:
            if moves_and_score_candidate[-1] > moves_and_score[-1]:
                moves_and_score = moves_and_score_candidate
        else:
            if moves_and_score_candidate[-1] < moves_and_score[-1]:
                moves_and_score = moves_and_score_candidate
    return moves_and_score


def show_board(current_board, c_choice, o_choice):
    chars = {
        -1: o_choice,
        1: c_choice,
        0: ' '
    }
    table_values = []
    for row in current_board:
        curr = []
        for cell in row:
            curr.append(chars[cell])
        table_values.append(curr)

    formatted_table = str()
    line = "\n" + "-+-+-" + "\n"
    for row in table_values:
        formatted_table += "|".join(row) + line
    print(formatted_table[:-6])


def computer_turn(c_choice, o_choice):
    depth = len(free_positions(board))
    if depth == 0 or game_over(board):
        return
    if depth == 9:
        x = np.random.choice([0,2])
        y = np.random.choice([0,2])
    else:
        move = minimax(board, depth, COMPUTER)
        x, y = move[0], move[1]
    set_move(x, y, COMPUTER)
    show_board(board, c_choice, o_choice)


def opponent_turn(c_choice, o_choice):
    depth = len(free_positions(board))
    if depth == 0 or game_over(board):
        return
    moves_map = {
        0: [0, 0], 1: [0, 1], 2: [0, 2],
        3: [1, 0], 4: [1, 1], 5: [1, 2],
        6: [2, 0], 7: [2, 1], 8: [2, 2],
    }
    move = -1
    while move < 0 or move > 8:
        try:
            move = int(input('Choose a number from [0,1,..,8]: '))
            coord = moves_map[move]
            can_move = set_move(coord[0], coord[1], OPPONENT)
            if not can_move:
                print('That is taken!')
                move = -1
        except (KeyError, ValueError):
            print('Between 0 and 8, please :) ')
    show_board(board, c_choice, o_choice)


def main():
    o_choice = ''
    first = ''
    while o_choice != 'O' and o_choice != 'X':
        try:
            o_choice = input('Choose X or O: ').upper()
        except (KeyError, ValueError):
            print('Bad choice')

    if o_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (KeyError, ValueError):
            print('Choose between y or n')

    while len(free_positions(board)) > 0 and not game_over(board):
        if first == 'N':
            print('Let the game begin!' + '\n')
            computer_turn(c_choice, o_choice)
            first = ''
        if first == 'Y':
            print('Let the game begin!' + '\n')
            show_board(board, c_choice, o_choice)
            first = ''

        opponent_turn(c_choice, o_choice)
        computer_turn(c_choice, o_choice)

    if is_player_winning(board, OPPONENT):
        print('YOU WIN!')
    elif is_player_winning(board, COMPUTER):
        print('YOU LOSE!')
    else:
        print('DRAW!')


if __name__ == '__main__':
    main()