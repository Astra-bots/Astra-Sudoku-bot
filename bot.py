import os

from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from sudoku import (
    create_puzzle,
    make_move,
    is_completed
)

from solver import solve



load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


games = {}





def board_keyboard(game):

    keyboard = []

    board = game["board"]


    for r in range(9):

        row = []

        for c in range(9):

            value = board[r][c]


            text = (
                str(value)
                if value != 0
                else "⬜"
            )


            row.append(
                InlineKeyboardButton(
                    text,
                    callback_data=f"cell_{r}_{c}"
                )
            )


        keyboard.append(row)



    keyboard.append(
        [
            InlineKeyboardButton(
                "💡 Hint",
                callback_data="hint"
            ),

            InlineKeyboardButton(
                "🔄 بازی جدید",
                callback_data="new_game"
            )
        ]
    )


    return InlineKeyboardMarkup(keyboard)







def number_keyboard():

    keyboard = []


    row = []


    for number in range(1,10):

        row.append(
            InlineKeyboardButton(
                str(number),
                callback_data=f"num_{number}"
            )
        )


        if len(row) == 3:

            keyboard.append(row)

            row = []



    return InlineKeyboardMarkup(keyboard)







def level_keyboard():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🟢 آسان",
                    callback_data="level_easy"
                )
            ],

            [
                InlineKeyboardButton(
                    "🟡 متوسط",
                    callback_data="level_medium"
                )
            ],

            [
                InlineKeyboardButton(
                    "🔴 سخت",
                    callback_data="level_hard"
                )
            ]
        ]
    )







async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):


    await update.message.reply_text(

        "🧩 Astra Sudoku\n\n"
        "سطح بازی را انتخاب کن:",

        reply_markup=level_keyboard()

    )








async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):


    query = update.callback_query

    await query.answer()


    user_id = query.from_user.id

    data = query.data






    # انتخاب سطح

    if data.startswith("level_"):


        level = data.replace(
            "level_",
            ""
        )


        games[user_id] = create_puzzle(level)


        await query.edit_message_text(

            "🧩 بازی شروع شد!\n"
            "یک خانه انتخاب کن:",

            reply_markup=board_keyboard(
                games[user_id]
            )

        )


        return






    if user_id not in games:

        return



    game = games[user_id]







    # بازی جدید

    if data == "new_game":


        games[user_id] = create_puzzle(
            "medium"
        )


        await query.edit_message_text(

            "🔄 بازی جدید شروع شد!",

            reply_markup=board_keyboard(
                games[user_id]
            )

        )


        return






    # Hint

    if data == "hint":


        temp = [

            row[:]

            for row in game["board"]

        ]



        if solve(temp):


            for r in range(9):

                for c in range(9):


                    if game["board"][r][c] == 0:


                        await query.edit_message_text(

                            f"💡 Hint:\n\n"
                            f"ردیف {r+1}\n"
                            f"ستون {c+1}\n"
                            f"عدد درست: {temp[r][c]}",

                            reply_markup=board_keyboard(game)

                        )


                        return







    # انتخاب خانه

    if data.startswith("cell_"):


        _, row, col = data.split("_")


        game["selected"] = (

            int(row),

            int(col)

        )


        await query.edit_message_text(

            "🔢 عدد را انتخاب کن:",

            reply_markup=number_keyboard()

        )


        return








    # انتخاب عدد

    if data.startswith("num_"):


        number = int(
            data.replace(
                "num_",
                ""
            )
        )



        if "selected" not in game:

            return



        row, col = game["selected"]



        if make_move(
            game,
            row,
            col,
            number
        ):


            if is_completed(game):


                await query.edit_message_text(

                    "🏆 تبریک!\n"
                    "سودوکو را کامل حل کردی 🎉"

                )


                return



            message = "✅ حرکت درست بود"



        else:


            message = "❌ عدد اشتباه است"





        await query.edit_message_text(

            message +
            "\n\nیک خانه انتخاب کن:",

            reply_markup=board_keyboard(game)

        )








def main():


    app = Application.builder().token(TOKEN).build()


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CallbackQueryHandler(play)
    )


    print("Astra Sudoku Started 🧩")


    app.run_polling()






if __name__ == "__main__":

    main()
