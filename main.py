from colorama import init, deinit, Fore

from ui_view import UI_Manager
from terminal_view import main_program


init(autoreset=True)


menu_is_active = True
while menu_is_active:
    print("")
    print("")
    print("                Application Pur Beurre")
    print("")
    print("             1 : Terminal User Interface")
    print("             2 : Graphical User Interface")
    print("")
    print("             0 : Exit")
    print("----")
    print("")
    user_input = input(" Action : ")

    if user_input == '1':
        main_program()
    elif user_input == '2':
        # GUI instance
        new_app = UI_Manager()
        new_app.window.mainloop()
    elif user_input == '0':
        print(Fore.RED + "Exiting....")
        menu_is_active = False
    else:
        print("Unknown choice... Retry...")


deinit()
