from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Handler
from random import choice
from os import listdir


token = "1741572298:AAG3j-Ay5Dtk7xZVk_3KPDLtls4XQpwUEUI"
mybot = Bot(token=token)
updater = Updater(token = token, use_context = True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "Hello, I am your new bot!" )

def hello(update, context):
    def check(update, context):
        a = update.message.text
        print("built-in function called"+a)
    print("function called")
    command = MessageHandler(Filters.text, check)
    dispatcher.add_handler(command)
    updater.start_polling()
    

def kitten(update, context):
    filename = choice(listdir("./Kittens"))
    try: image = open("./Kittens/"+filename,"rb")
    except: 
        print("Cant read image")
        return
    context.bot.send_photo(chat_id = update.effective_chat.id, photo=image)


def words_in_text(text):
    if not ' ' in text: return 1
    a = text.split(' ')
    return(len(a))


def countwords(update, context):
    print("counting")
    words_count = words_in_text(update.message.text)
    append = False
    username = update.message.from_user.name
    first_name = update.message.from_user.first_name
    chat_id = str(update.effective_chat.id)
    try:
        file = open("./CountWords/"+chat_id+".txt", "r")
        lines = file.readlines()
        file.close()
        for i in range(len(lines)): 
            if username in lines[i]:
                append = True
                temp_user, count, first_name= lines[i].split(' ')
                count = int(count)
                count+=words_count
                print(count)
                lines[i]=(username+' '+str(count)+' '+first_name)
                break   
        if not append:
            lines.append(username+' '+str(words_count)+' '+first_name+'\n')
    except(FileNotFoundError):
        lines = []
        lines.append(username+' '+str(words_count)+' '+first_name+'\n')
    file = open("./CountWords/"+chat_id+".txt", "w")
    file.writelines(lines)
    print(lines)
    #context.bot.send_message(chat_id = update.effective_chat.id, text = "Thank you!\nTake a kitten!!!")
    #kitten(update, context)


def report(update, context):
    chat_id = str(update.effective_chat.id)
    file = open("./CountWords/"+chat_id+".txt", "r")
    lines = file.readlines()
    full_text=""
    for line in lines:
        username, count, first_name= line.split(' ') 
        full_text+=(first_name[:-1]+' '+count+'\n')
    print(full_text)    
    context.bot.send_message(chat_id = update.effective_chat.id, text = full_text)

def help(update, context):
    text = "Hello!\nSo what can this bot do?\nActually now it is just word-counter, BUT\nYou can get a cutie by typing /kitten\nAlso you can see your words in this chat /words_report\nPLEASE DON'T ADD THIS BOT TO THE GROUP CHATS, IT WILL BE BROKEN\nupd: it will work"
    context.bot.send_message(text = text, chat_id = update.effective_chat.id)

start_handler = CommandHandler('start', start)
second_command = CommandHandler("hello", hello)
give_me_kitten=CommandHandler("kitten", kitten)
words_report = CommandHandler("words_report", report)
help_command = CommandHandler("help", help)
not_command_but_text = MessageHandler(Filters.text|Filters.update, countwords)
#chat_handler = Handler(countwords)

"""
Create a function
Create a handler, for example

handler = CommandHandler({command}, function_name)
handler = MessageHander(Filters.text, function.name) 

!!!!!!DONT FORGET TO ADD HANDLER TO DICPATCHER!!!!!!


(?) How to make bot wait for the input
(?) All in main & regimes or lots of functions // functions in functions
(?) Request return from functions 
(?) How does not is end 
(?) How to interact with functions? 

"""

dispatcher.add_handler(second_command)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(give_me_kitten)
dispatcher.add_handler(words_report)
dispatcher.add_handler(help_command)
#dispatcher.add_handler(chat_handler)
dispatcher.add_handler(not_command_but_text)


updater.start_polling()
