import random

from generator import generate_full_board



DIFFICULTY = {

    "easy": 35,

    "medium": 45,

    "hard": 55

}



def copy_board(board):

    return [
        row[:] 
        for row in board
    ]





def create_puzzle(level="medium"):


    solution = generate_full_board()


    puzzle = copy_board(solution)


    remove_count = DIFFICULTY.get(
        level,
        45
    )



    removed = 0


    while removed < remove_count:


        row = random.randint(
            0,
            8
        )

        col = random.randint(
            0,
            8
        )



        if puzzle[row][col] != 0:


            puzzle[row][col] = 0

            removed += 1



    return {

        "board": puzzle,

        "solution": solution

    }







def make_move(game, row, col, number):


    if game["board"][row][col] != 0:

        return False



    if game["solution"][row][col] == number:

        game["board"][row][col] = number

        return True



    return False






def is_completed(game):


    for row in game["board"]:

        if 0 in row:

            return False



    return True
