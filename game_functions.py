""" Formatting functions """
import csv
import os
import pandas as pd
from colorama import Fore, Style

from game_settings import GameSettings
from game import Game


def print_line(lines):
    for i in range(lines): print("########################################################################")


def print_space(spaces):
    for i in range(spaces): print("")


def print_intro1():
    print(f"""
{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}Oink Oink, HELLO!!!
Welcome to Learning Python: Pig Games!{Style.RESET_ALL}
{Fore.LIGHTMAGENTA_EX}I'm PIG! And this is the terminal game: "GUESS A NUMBER"{Style.RESET_ALL}
""")


def print_intro2():
    print(f"""{Fore.LIGHTMAGENTA_EX}Oink... I'm thinking about a number. Can you guess it???
There are different options to make our game more interesting:
\t* 5 different difficulties
\t* Hint mode (for the pig cheaters!)
\t* Locally-saved scoreboard
\t* Oink oink stuff{Style.RESET_ALL}""")


########################################################################################################################
########################################################################################################################
########################################################################################################################


""" Menu functions """


def main_menu():
    print_space(1)
    print_line(1)
    print_space(1)
    print(f"""{Style.BRIGHT}Let's get oinking... Choose any option by typing the number below:{Style.RESET_ALL}
    [{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}1{Style.RESET_ALL}] Play Game
    [{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}2{Style.RESET_ALL}] Open Settings
    [{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}3{Style.RESET_ALL}] View Scoreboard
    [{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}4{Style.RESET_ALL}] Exit
    """)

    try:
        option = int(input(f"{Fore.YELLOW}[PIG ORDER]{Style.RESET_ALL}" + " Enter an option now! (1-4): "))

        if option == 1:
            start_game()
        elif option == 2:
            open_settings()
        elif option == 3:
            read_scores()
        elif option == 4:
            print_space(1)
            print(f"{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}Pig bye! See ya soon.{Style.RESET_ALL}")
            exit()
        else:
            raise ValueError

    except ValueError:
        print_space(1)
        print(f"{Fore.RED}[OINK!] Please enter a valid number{Style.RESET_ALL}")
        main_menu()


def open_settings():
    print_space(1);
    print_line(1);
    print_space(1)

    # Initialize an instance of gamesettings to run checks and prepare game settings
    new_game = GameSettings(0, False)
    new_game.preferences_file_check()

    # Retrieve current hint status to display in menu
    print_hint_status = new_game.retrieve_preferences('hint')
    if print_hint_status == 1:
        print_hint_status = 'ON'
    elif print_hint_status == 0:
        print_hint_status = 'OFF'

    print(f"""You are in [{Style.BRIGHT}PIG SETTINGS{Style.RESET_ALL}]. Choose an option below by entering a number:
    [{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}1{Style.RESET_ALL}] Set difficulty
    [{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}2{Style.RESET_ALL}] Toggle Hint Mode [Current Status: {Fore.LIGHTMAGENTA_EX + Style.BRIGHT}{print_hint_status}{Style.RESET_ALL}]
    [{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}3{Style.RESET_ALL}] Go back to main menu
    """)

    try:
        option = int(input(f"{Fore.YELLOW}[PIG ORDER]{Style.RESET_ALL}" + " Enter an option now! (1-3): "))

        if option == 1:
            new_game.edit_difficulty()
            main_menu()
        elif option == 2:
            new_game.toggle_hint()
            open_settings()
        elif option == 3:
            main_menu()
        else:
            raise ValueError

    except ValueError:
        print_space(1)
        print(f"{Fore.RED}[OINK!] Please enter a valid number{Style.RESET_ALL}")

        main_menu()


def score_menu_options():
    print(f"""
What would you like to do?
\t [{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}1{Style.RESET_ALL}] Play a game
\t [{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}2{Style.RESET_ALL}] Reset scores (this CANNOT be undone!)
\t [{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}3{Style.RESET_ALL}] Go back to main menu
""")

    try:
        option = int(input(f"{Fore.YELLOW}[PIG ORDER]{Style.RESET_ALL}" + " Enter an option now!: "))
        if option == 1: start_game()

        if option == 2:
            with open('scores.csv', 'w+', newline='') as score_csv:
                fieldnames = ['id', 'attempts']
                score_writer = csv.DictWriter(score_csv, fieldnames=fieldnames)
                score_writer.writeheader()

            print_space(1)
            print(f"{Fore.LIGHTGREEN_EX}Your score dashboard have been reset.{Style.RESET_ALL}")
            main_menu()

        elif option == 3:
            main_menu()
        else:
            raise ValueError

    except ValueError:
        print(f"{Fore.RED}[OINK!]{Style.RESET_ALL}" + "Please enter a valid option")


########################################################################################################################
########################################################################################################################
########################################################################################################################


""" File management functions """


def file_exists(file):
    if os.path.exists(file):
        return True
    else:
        return False


def find_index(option):
    if file_exists('preferences.csv'):
        df = pd.read_csv('preferences.csv')
        if option in df.values:
            # Find index to make program more dynamic
            count = 0
            index = -1
            for i in df.values:
                if option in i: index = count
                count += 1
            return index

        else:
            return -1
    else:
        return -1


def read_game_id():
    try:
        with open("scores.csv", newline='') as score_file_object:
            # Check if file is empty and set-up a variable
            file_rows = len(score_file_object.readlines())
            if file_rows == 1:
                return 1
            else:
                return file_rows

    # If not file, then this is game #1
    except FileNotFoundError:
        return 1


def read_scores():
    print_space(0)
    is_file_empty = False

    try:
        with open("scores.csv", newline='') as score_file_object:
            # Check if file is empty and set-up a variable
            file_rows = len(score_file_object.readlines())
            if file_rows == 1: is_file_empty = True

            # Reset pointer to beginning of CSV file object
            score_file_object.seek(0)

            # Reset reader object
            score_file_reader = csv.DictReader(score_file_object)
            print_space(1)
            print(f"""You are in [{Style.BRIGHT}SCORE DASHBOARD{Style.RESET_ALL}]. Here are the games you won:""")
            for rows in score_file_reader: print(
                f"{Fore.LIGHTMAGENTA_EX}-->{Style.RESET_ALL} Game no. {rows['id']}: Won in {rows['attempts']} attempt(s)")

            if is_file_empty is True: raise FileNotFoundError

            score_menu_options()
            # Play again?

    except FileNotFoundError:
        print_space(1);
        print(f"{Fore.YELLOW + Style.BRIGHT}It doesn't look like you've played any games yet!{Style.RESET_ALL}")
        main_menu()


def set_basic_preference():
    with open('preferences.csv', 'w+', newline='') as preference_csv:
        fieldnames = ['name', 'value']
        preference_writer = csv.DictWriter(preference_csv, fieldnames=fieldnames)
        preference_writer.writeheader()
        preference_writer.writerow({'name': 'difficulty', 'value': 1})
        preference_writer.writerow({'name': 'hint', 'value': 0})


def write_preferences(index, value):
    # Update index in preferences.csv
    df = pd.read_csv('preferences.csv')
    df.at[index, 'value'] = value
    df.to_csv('preferences.csv', index=False)


########################################################################################################################
########################################################################################################################
########################################################################################################################



""" Main function to launch or relaunch a game """

def start_game():
    # Create new instance of a game
    new_game = Game()

    # check also change variable to overwrite wrong value
    new_game.preferences_file_check()

    # set difficulty now that file is OK
    new_game.set_parameters('difficulty')
    new_game.set_parameters('hint')

    # generate number to be guessed and launch game
    new_game.generate_number()
    new_game.play_game()