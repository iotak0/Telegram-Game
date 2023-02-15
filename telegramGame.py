import json
import telebot
from telebot import types,util
from ast import alias
import numpy as np
import random
import os
BOT_TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(BOT_TOKEN)

player1 = ""
player2 = ""
pr1 = 0
pr2 = 0
turn = ""
gameOver = True
board = []
bool_arr = []

sample_arr = []

# @client.command()
# async def stop(ctx):
#     gameOver = True
def delet(message):
    bot.delete_message(message.chat.id,message_id=message.id)
@bot.message_handler(func=lambda m:True)
def reply(message):
    global gameOver
    
    print(gameOver)
    p1=''
    p2=''
    word = message.text.split()
    if word[0] == "po":
        pos = int(" ".join(word[1:]))
        po(message, pos)
    if word[0] == "p1":
        with open("data.json", "r") as jsonFile:
            data = json.load(jsonFile)
            jsonFile.close()
        if gameOver == False and message.from_user.username == data["users"]["player2"]:
            bot.reply_to(message,"عامل ذكي ها !؟")
        if gameOver:   
            p1 =message.from_user.username
            bot.reply_to(message,str("1st Player: @"+message.from_user.username))
            with open("data.json", "r") as jsonFile:
                data = json.load(jsonFile)
                jsonFile.close()
            users = data["users"]
            users["player1"] =p1
            data["users"] = users
            with open("data.json", "w") as editedFile:
                json.dump(data, editedFile, indent=5)
            editedFile.close()
    if word[0] == "p2":
        with open("data.json", "r") as jsonFile:
            data = json.load(jsonFile)
            jsonFile.close()
        if gameOver == False and message.from_user.username == data["users"]["player1"]:
            bot.reply_to(message,"عامل ذكي ها !؟")
        if gameOver: 
            p2 =message.from_user.username
            bot.reply_to(message,str("2nd Player: @"+message.from_user.username))
            with open("data.json", "r") as jsonFile:
                data = json.load(jsonFile)
                jsonFile.close()
            users = data["users"]
            users["player2"] =p2
            data["users"] = users
            with open("data.json", "w") as editedFile:
                json.dump(data, editedFile, indent=5)
            editedFile.close()
    if word[0] == "start":
        with open("data.json", "r") as jsonFile:
            data = json.load(jsonFile)
            jsonFile.close()
        p1 = data["users"]["player1"]
        p2 = data["users"]["player2"]
        boom(message=message, p1=p1,p2=p2)
    if word[0] == "stop":
        with open("data.json", "r") as jsonFile:
            data = json.load(jsonFile)
            jsonFile.close()
        p1 = data["users"]["player1"]
        p2 = data["users"]["player2"]
        if message.from_user.username == p1 or message.from_user.username ==p2:
            gameOver= True
            bot.reply_to(message,'game Over!.')
        else: 
            bot.reply_to(message,'A game is already in progress! Finish it before starting a new one.')
    if word[0] == "it":
        print(message)
        delet(message=message)
    
@bot.message_handler(func=lambda m:True)
def delete(message):
    global gameOver
    with open("data.json", "r") as jsonFile:
        data = json.load(jsonFile)
        jsonFile.close()
    word = message.text.split()
    if word[0] == "stop":
        if message.from_user.username == data["users"]["player1"] or message.from_user.username ==data["users"]["player2"]:
            gameOver= True
        else: 
            bot.reply_to(message,'A game is already in progress! Finish it before starting a new one.')
def boom(message,p1, p2):
    global count
    global player1
    global player2
    global turn
    global gameOver    
    global bool_arr
    global sample_arr
    global pr1
    global pr2


    delete(message=message)
    if gameOver:
        global board
        board = ["🕐","🕑","🕒","🕓",
                "🕔","🕕","🕖", "🕗",
                "🕘","🕙","🕚","🕛"]
        turn = ""
        gameOver = False
        count = 0
        sample_arr = [True, False]
        bool_arr = np.random.choice(sample_arr, size=12)
        print(bool_arr)
        player1 = p1
        player2 = p2
        print(p1+"\n"+p2)
        # print the board
        line = ""
        test = ''
        for x in range(len(board)):
            if x == 3 or x == 7 or x == 11:
                line += " " + board[x]
                test += line+"\n"
                #bot.send_message(message.chat.id,line)
                line = ""
            else:
                line += " " + board[x]
        print(test)
        bot.send_message(message.chat.id,test)

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            bot.reply_to(message,"It is <@" + str(player1) + ">'s turn.")
        elif num == 2:
            turn = player2
            bot.reply_to(message,"It is <@" + str(player2) + ">'s turn.")
    else:
        bot.reply_to(message,"A game is already in progress! Finish it before starting a new one.")

def po(message, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver
    global bool_arr
    global pr1
    global pr2


    if not gameOver:
        mark = ""
        if turn == message.from_user.username:
            if turn == player1:
                mark = "🔵"
            elif turn == player2:
                mark = "🔴"
            if 0 < pos < 13 and board[pos - 1] in board:
                print(bool_arr[pos-1])
                if bool_arr[pos-1] == False:
                    mark = "💥"
                    count += 1
                    if turn == player1:
                        board[pos - 1] = mark
                        pr1 +=1
                    else:
                        board[pos - 1] = mark
                        pr2 +=1
                else:
                    board[pos - 1] = mark
                    count += 1

                # print the board
                line = ""
                test = ''
                for x in range(len(board)):
                    if x == 3 or x == 7 or x == 11:
                        line += " " + board[x]
                        test += line+"\n"
                        #bot.send_message(message.chat.id,line)
                        line = ""
                    else:
                        line += " " + board[x]
                bot.send_message(message.chat.id,test)

                if turn == player1:
                    if count < 12:
                        bot.reply_to(message,"It is Ur turn @" + str(player2) + " .")
                else:
                    if count < 12:
                        bot.reply_to(message,"It is Ur turn <@" + str(player1) + "> .")
                print(count)
                if count >= 12:
                    if pr1> pr2:
                        bot.reply_to(message,str("🔵 @" +player1+ " wins!\nUr Points: "+str(pr1)))
                    elif pr1 < pr2:
                        bot.reply_to(message,str("🔴 @" +player2+ " wins!\nUr Points: "+str(pr2)))
                    else:
                        bot.reply_to(message,str("Draw! \n🔵 @" +player1+"  Points: "+ str(pr1)+"🔴 @" +player2+"  Points: "+ str(pr2)))
                    
                    
                    gameOver = True
                

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                bot.reply_to(message,"Be sure to choose an integer between 1 and 12 (inclusive) and an unmarked tile.")
        else:
                bot.reply_to(message,"It is not your turn.")
    else:
        bot.reply_to(message,"Please start a new game using the [ start  ].")


# @boom.error
# async def tictactoe_error(message, error):
#     print(error)
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send("Please mention 2 players for this command.")
#     elif isinstance(error, commands.BadArgument):
#         await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

# @po.error
# async def place_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send("Please enter a position you would like to mark.")
#     elif isinstance(error, commands.BadArgument):
#         await ctx.send("Please make sure to enter an integer.")


# If you wish to securely hide your token, you can do so in a .env file.
# 1. Create a .env in the same directory as your Python scripts
# 2. In the .env file format your variables like this: VARIABLE_NAME=your_token_here
# 3. At the top of the Python script, import os
# 4. In Python, you can read a .env file using this syntax:
# token = os.getenv(VARIABLE_NAME)


bot.infinity_polling(allowed_updates=util.update_types)
