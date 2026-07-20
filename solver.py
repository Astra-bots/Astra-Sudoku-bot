SIZE = 9



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

            if board[start_row+i][start_col+j] == num:

                return False



    return True






def find_empty(board):


    for row in range(SIZE):

        for col in range(SIZE):


            if board[row][col] == 0:

                return row, col



    return None





def solve(board):


    empty = find_empty(board)



    if not empty:

        return True



    row, col = empty



    for num in range(1, 10):


        if is_valid(
            board,
            row,
            col,
            num
        ):


            board[row][col] = num



            if solve(board):

                return True



            board[row][col] = 0



    return False
