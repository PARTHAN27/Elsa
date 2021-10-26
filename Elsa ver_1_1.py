import gc
import os
from functools import partial
from pathlib import Path
from threading import Thread
from tkinter import Tk, Entry, END

gc.disable()  # disabling garbage collection as it causes problem with tkinter threads


def loading_error_warning(e=''):
    print(e, "It seems there some problem with task1 and/or talk1 package and/or magic package and/or the main file is outdated")
    print("Suggested fix:install/update magicForElsa using pip install --upgrade magicForElsa"
          "or reinstall the elsa ver1_1.py file from https://github.com/georgerahul24/Viraver1.1")
    input("Press any key to exit....")
    exit()


try:
    from Magic import initial_setup

    # Checks if initial.elsa exists.If it doesn't exist the initial setup is run.....
    initial_file = Path((os.getcwd() + "\\resources\\ initial.elsa"))
    print("'initial.elsa' found") if initial_file.exists() else initial_setup.install_files()
    from Magic import history, tkinterlib, popups, program_run, theme, settings, indexer, usernames, highlighter, chat_client

    indexer.index_files()
except Exception as e:
    loading_error_warning(e)

# Reading the themes for the tkinter window and all
bg_colour, text_color, button_colour = theme.read_theme()

try:
    from task1 import task
    from talk1.talk1 import talk
except Exception as e:
    loading_error_warning(e)
# verifying usernames module
CHK = usernames.verify_usernames()
# see how 'not' operator works with 'if' in https://pythonexamples.org/python-if-not/
print("'Usernames.py' verified successfully") if not CHK else loading_error_warning()
print("Starting the login page")
talk("Hi. I am Elsa")
SECURITY_TRIAL = 0


def quit(event="") -> None:
    """To exit the program"""
    exec("try: chat_client.closeClient()\nexcept:pass")
    talk("Tata Bye Bye ")
    history.user_file(name, ord, "User closed")
    exit()


# password and username checks
while True:
    usernames.check_user()
    if usernames.check_user.security:
        print("Access Granted")
        talk("Access Granted")
        task.greeting(usernames.check_user.loginname)
        break

    else:
        print("Access Denied")
        SECURITY_TRIAL += 1
        if SECURITY_TRIAL >= 3:
            print("You have reached the maximum error limit")
            talk("You have reached the maximum error limit")
            exit()
        else:
            talk("Access Denied. Please Try Again")

name = usernames.check_user.loginname
del CHK, SECURITY_TRIAL
# ..............tkinter initialising starts...............................
elsagui = Tk()
# Reading the screen height and width
screen_height, screen_width = elsagui.winfo_screenheight(), elsagui.winfo_screenwidth()
tkinterlib.tkinter_initialise(elsagui, screen_width - 150, screen_height - 100)
del screen_width, screen_height
Search_box = Entry(elsagui, bg=bg_colour, fg=text_color)
Search_box.pack()
# ..............tkinter initialising ends...............................
# ...initialising chat client..........
chat_client.getNickname(name)
try:
    print("Connecting to a server")
    chat_client.startclient()
    print("Connected to a server")
except: print("Could not establish a connection with server")


# ................command input and processing starts.....................
def work(event="") -> None:
    """This is the main function where user input is read and proper actions are taken"""
    order = Search_box.get().lower()
    Search_box.delete(0, END)
    parts = order.split()
    keyword = parts[0]
    try:
        afterword = " ".join(parts[1:])
    except:
        afterword = ""

    # srch in net
    if keyword in ["search", "browse", "srch", "s"]:
        Thread(target=task.web, args=(afterword,)).start()
        history.user_file(name, order, f'"Searched:" {order}')

    elif keyword in ["msg"]:
        chat_client.sendtoserver(nameToSend := parts[1], msgTosend := " ".join(parts[2:]))
        history.user_file(name, order, f"Snd msg to {nameToSend}.Msg was {msgTosend}")

    elif keyword in ["bye", "tata", "close", "exit"]:
        quit()

    elif keyword in ["open", "o", "folder"]:
        Thread(target=indexer.search_indexed_folder, args=(afterword,)).start()
        history.user_file(name, order, f"Tried to open the folder {afterword}. Status:Unknown")

    elif keyword in ["file", "f"]:
        Thread(target=indexer.search_indexed_file, args=(afterword,)).start()
        history.user_file(name, order, f"Tried to open the file {afterword}. Status:Unknown")

    elif keyword == "run":
        Thread(target=program_run.program_run, args=(afterword,)).start()
        history.user_file(name, order, f"Opened {afterword}")

    elif keyword == "firefox":
        Thread(target=task.firefox).start()
        history.user_file(name, order, "Opened firefox")

    elif keyword in ["settings", "setting"]:
        talk("I have opened the settings page for you")
        settings.setting_page(name)
        history.user_file(name, order, "Opened Settings")

    elif keyword == "time":
        task.tell_time()
        history.user_file(name, order, "told Time ")

    elif keyword in ["website", "w"]:
        task.websiteopen(afterword)
        history.user_file(name, order, f"Tried to open the website {afterword}")

    elif order in ["what is your version", "ver"]:
        talk("My version is 1 point 1")

    elif keyword == "what is your name":
        talk("My name is Elsa")

    elif keyword in ["hello", "hlo", "hey"]:
        talk("Hi. What can I do for you")

    elif keyword == "hi":
        talk(f"Hello {name}")

    elif order == "download":
        task.download()
        history.user_file(name, order, "Opened downloads folder")

    elif order == "desktop":
        task.desktop()
        history.user_file(name, order, "Opened desktop folder")

    elif order == "music":
        task.musicFolder()
        history.user_file(name, order, "Opened music folder")

    elif order in ["show history", "sh"]:
        history.user_read(username=name)
        talk("Opened history")

    elif order == "clear history":
        history.clear_history(name)
        talk("Cleared history")

    elif order in ["tell jokes", "tell a joke", "joke"]:
        task.joke()
        history.user_file(name, order, "Told a joke")

    elif order == "shutdown":
        history.user_file(name, order, "Shutdown the computer")
        task.shutdown()

    elif order == "restart":
        history.user_file(name, order, "Restarted the computer")
        task.restart()
    else:
        def srchUserInput():
            talk("I could not understand what you meant. Do you wanna find it in the internet?")
            popups.popups(order)

        Thread(target=srchUserInput).start()
        history.user_file(name, order, f"Tried to search {order} in internet.Status unknown")
    del parts, keyword, afterword
    gc.collect()


def clearTextbox(event=""):
    Search_box.delete(0, END)


# Binding keyboard shortcuts
elsagui.bind("<Control-h>", partial(history.user_read, username=name))  # To open histroy page
elsagui.bind("<Control-e>", quit)  # exiting the program
elsagui.bind("<Control-s>", partial(settings.setting_page, username=name, state=True))  # To open setting page
elsagui.bind("<KeyRelease>", partial(highlighter.syntax_highlighting, Search_box=Search_box))  # syntax highlighting
elsagui.bind("<Return>", work)  # Binds textbox so that if user presses enter work() is called
elsagui.bind("<Control-BackSpace>", clearTextbox)
elsagui.mainloop()
