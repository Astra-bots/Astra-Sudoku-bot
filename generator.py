import random


SIZE = 9


def create_empty_board():
    return [
        [0 for _ in range(SIZE)]
        for _ in range(SIZE)
    ]



def is_valid(board, row, col, num):

    # بررسی ردیف
    for x in range(SIZE):

        if board[row][x] == num:
            return False



    # بررسی ستون
    for x in range(SIZE):

        if board[x][col] == num:
            return False



    # بررسی مربع ۳×۳
    start_row = row - row % 3
    start_col = col - col % 3


    for i in range(3):

        for j in range(3):

            if board[start_row + i][start_col + j] == num:

                return False



    return True





def fill_board(board):

    for row in range(SIZE):

        for col in range(SIZE):

            if board[row][col] == 0:


                numbers = list(
                    range(1, 10)
                )


                random.shuffle(numbers)


                for num in numbers:


                    if is_valid(
                        board,
                        row,
                        col,
                        num
                    ):


                        board[row][col] = num



                        if fill_board(board):

                            return True



                        board[row][col] = 0



                return False



    return True





def generate_full_board():

    board = create_empty_board()

    fill_board(board)

    return board
