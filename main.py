# !/usr/bin/env python

import random
import csv
import os.path
import pandas as pd

from colorama import init
from colorama import Fore
from colorama import Style

init()

########################################################################################################################
########################################################################################################################
########################################################################################################################


def print_line(lines):
    for i in range(lines): print("########################################################################")


def print_space(spaces):
    for i in range(spaces): print("")


def print_intro():
    print("""
Welcome to Pig's famous "GUESS MY NUMBER" game

----------------------------------------------
The goal is to guess the right number in as little attempts as possible!
You can use a pre-made difficulty build or just make up your own!""")


def score_menu_options():
    print("""
What would you like to do?
\t [1] Play a game
\t [2] Reset scores (this CANNOT be undone!)
\t [3] Go back to main menu
""")

    try:
        option = int(input(f"{Fore.YELLOW}[INPUT NEEDED]{Style.RESET_ALL}" + " Enter an option below: "))
        if option == 1: start_game()

        if option == 2:
            with open('scores.csv', 'w+', newline='') as score_csv:
                fieldnames = ['id', 'attempts']
                score_writer = csv.DictWriter(score_csv, fieldnames=fieldnames)
                score_writer.writeheader()

            print_space(1)
            print("You score have been reset.")
            main_menu()

        elif option == 3: main_menu()
        else: raise ValueError

    except ValueError: print(f"{Fore.RED}[WARNING]{Style.RESET_ALL}" + "Please enter a valid option")


def read_game_id():
    try:
        with open("scores.csv", newline='') as score_file_object:
            # Check if file is empty and set-up a variable
            file_rows = len(score_file_object.readlines())
            if file_rows == 1:return 1
            else: return file_rows

    # If not file, then this is game #1
    except FileNotFoundError: return 1


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

        else: return -1
    else: return -1


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
            print("""[SCORES DASHBOARD] Please see below for a list of all the games you won since the last reset:""")
            for rows in score_file_reader: print("\tGame no. {id}: Won in {attempts} attempt(s)".format(id=rows['id'], attempts=rows['attempts']))

            if is_file_empty is True: raise FileNotFoundError

            score_menu_options()
            # Play again?

    except FileNotFoundError:
        print_space(1);
        print(f"{Fore.YELLOW}It doesn't look like you've played any games yet!{Style.RESET_ALL}")
        main_menu()


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


def main_menu():
    print_space(1); print_line(1); print_space(1)
    print("""Please start by choosing one of those options. Type a number from 1-4:
    [1] Play Game
    [2] Open Settings
    [3] View Scoreboard
    [4] Exit
    """)

    try:
        option = int(input(f"{Fore.YELLOW}[INPUT NEEDED]{Style.RESET_ALL}" + " Enter an option below (1-4): "))

        if option == 1: start_game()
        elif option == 2: open_settings()
        elif option == 3: read_scores()
        elif option == 4: exit()
        else: raise ValueError

    except ValueError:
        print_space(1)
        print(f"{Fore.RED}[WARNING] Please enter a valid number{Style.RESET_ALL}")
        main_menu()


def open_settings():
    print_space(1); print_line(1)

    # Initialize an instance of gamesettings to run checks and prepare game settings
    new_game = GameSettings(0, False)
    new_game.preferences_file_check()

    # Retrieve current hint status to display in menu
    print_hint_status = new_game.retrieve_preferences('hint')
    if print_hint_status == 1: print_hint_status = 'ON'
    elif print_hint_status == 0: print_hint_status = 'OFF'

    print(f"""You are in [SETTINGS]. Please choose an option below by entering a number:
    [1] Set difficulty
    [2] Toggle Hint Mode [Current Status: {Fore.YELLOW}{print_hint_status}{Style.RESET_ALL}]
    [3] Go back to main menu
    """)

    try:
        option = int(input(f"{Fore.YELLOW}[INPUT NEEDED]{Style.RESET_ALL}" + " Enter an option below (1-3): "))

        if option == 1:
            new_game.edit_difficulty()
            main_menu()
        elif option == 2:
            new_game.toggle_hint()
            open_settings()
        elif option == 3: main_menu()
        else: raise ValueError

    except ValueError:
        print_space(1)
        print(f"{Fore.RED}[WARNING] Please enter a valid number{Style.RESET_ALL}")

        main_menu()


def calculate_difficulty(dictionary, key): return dictionary[key]["maxAttempts"] / dictionary[key]["maxInt"] * 100


def file_exists(file):
    if os.path.exists(file): return True
    else: return False


def test_color():
    print(f"This is {Fore.GREEN}color{Style.RESET_ALL}!")

########################################################################################################################
########################################################################################################################


class GameSettings():
    difficulty_modes = {
        1: {"name": "Easy", "maxInt": 10, "maxAttempts": 7},
        2: {"name": "Medium", "maxInt": 20, "maxAttempts":10},
        3: {"name": "Hard", "maxInt": 40, "maxAttempts": 12},
        4: {"name": "Lucky", "maxInt": 80, "maxAttempts": 16},
        5: {"name": "Oink!", "maxInt": 160, "maxAttempts": 24}
    }

    hint_modes = [0, 1]

    def __init__(self,difficulty=1,difficulty_confirmed=True):
        self.difficulty_chosen = difficulty
        self.difficulty_confirmed = difficulty_confirmed
        self.hint_chosen = 0
        self.attempt = 0
        self.guess = 0
        self.answer = 0
        self.games_id = read_game_id()

        if difficulty:
            self.maxRange = self.difficulty_modes[self.difficulty_chosen]['maxInt']
            self.maxAttempts = self.difficulty_modes[self.difficulty_chosen]['maxAttempts']
            self.remaining = self.maxAttempts

        # @property
    def preferences_file_check(self):
        if file_exists('preferences.csv'):
            # if row 'difficulty' or 'hint' doesn't exist, reset preferences file to default
            if find_index('difficulty') == -1 or find_index('hint') == -1: set_basic_preference()

            # Look for main parameters indexes
            index_difficulty = find_index('difficulty')
            index_hint = find_index('hint')

            df = pd.read_csv('preferences.csv')

            # if difficulty value isn't OK
            if df.at[index_difficulty, 'value'] not in self.difficulty_modes:
                self.difficulty_chosen = 1
                write_preferences(index_difficulty, 1)

            # if hint value isn't OK
            if df.at[index_hint, 'value'] not in self.hint_modes:
                self.hint_chosen = 0
                write_preferences(index_hint, 0)

        # if file doesn't exist, default to 1
        else:
            with open('preferences.csv', 'w+', newline='') as preference_csv:
                fieldnames = ['name', 'value']
                preference_writer = csv.DictWriter(preference_csv, fieldnames=fieldnames)
                preference_writer.writeheader()
                preference_writer.writerow({'name': 'difficulty', 'value': 1})
                preference_writer.writerow({'name': 'hint', 'value': 0})
                return True

    def save_score(self):
        csv_file_exists = file_exists("scores.csv")

        with open('scores.csv', 'a+', newline='') as score_csv:
            fieldnames = ['id', 'attempts']
            score_writer = csv.DictWriter(score_csv, fieldnames=fieldnames)

            if csv_file_exists is not True:
                score_writer.writeheader()
                self.games_id = 1

            score_writer.writerow({'id': self.games_id, 'attempts': self.attempt})

    # Return value of an option in preferences.csv. Raised FileNotFoundError if file doesn't exists
    def retrieve_preferences(self, option):
        if file_exists('preferences.csv'):
            # Different formula - set default at launch
            if option == 'difficulty':
                df = pd.read_csv('preferences.csv')
                # Need to control if value doesn't exists.
                index = find_index('difficulty')
                if df.at[index, 'value'] in self.difficulty_modes: return df.at[index, 'value']
                else: return 0

            if option == 'hint':
                df = pd.read_csv('preferences.csv')
                # Need to control if value doesn't exists.
                index = find_index('hint')
                if df.at[index, 'value'] in self.hint_modes: return df.at[index, 'value']
                else: return 0

        else: raise FileNotFoundError

    def toggle_hint(self):
        print("""
[Hint Mode] It makes the game easier by letting you know if the answer is higher or lower than your input.""")
        # Comes after preferences_file_check() which ensured preferences.csv hasn't been tempered with
        self.hint_chosen = self.retrieve_preferences('hint')

        # Toggle hint on or off depending on original status
        if self.hint_chosen == 0:
            self.hint_chosen = 1
            print("\t Hint mode is now [ENABLED]")

        elif self.hint_chosen == 1:
            self.hint_chosen = 0
            print("]t Hint mode is now [DISABLED]")

        # Update preferences.csv file
        write_preferences(find_index('hint'), self.hint_chosen)

    # Automate print statement based on difficulty mode and replace win rate with attempt/guesses
    def set_difficulty(self):
        len_difficulty_modes = len(self.difficulty_modes)

        print("Please start by choosing your difficulty settings. Type a number below:")

        for i in self.difficulty_modes:
            iter_name = self.difficulty_modes[i]['name']
            iter_range = self.difficulty_modes[i]['maxInt']
            iter_attempts = self.difficulty_modes[i]['maxAttempts']
            print("\t[{number}] {difficulty_mode} \t\tGuess range: 1-{range}\t\tMax attempts: {max_attempts}".format(number=i,difficulty_mode=iter_name,range=iter_range, max_attempts=iter_attempts))

        print_space(1)

        try:
            difficulty_input = int(input(f"{Fore.YELLOW}[INPUT NEEDED]{Style.RESET_ALL}" + " Enter your difficulty settings (1-{max}):\n>>> ".format(max=len_difficulty_modes)))

            if difficulty_input in self.difficulty_modes: self.difficulty_chosen = difficulty_input
            else: raise ValueError

        except ValueError:
            print(self.difficulty_chosen)
            print(difficulty_input in self.difficulty_modes)
            print(f"{Fore.RED}[WARNING]{Style.RESET_ALL}" + " Please enter a valid number.")



    def confirm_choice(self):
        try:
            print_space(1)
            choice = input("Please enter " + f"{Fore.GREEN}[Y]{Style.RESET_ALL}" + " to confirm or " + f"{Fore.RED}[N]{Style.RESET_ALL}" + " to choose a new difficulty setting.\n>>> ")
            if choice == "Y" or choice == "y":
                write_preferences(find_index('difficulty'), self.difficulty_chosen)
                self.difficulty_confirmed = True

            elif choice == "N" or choice == "n": self.set_difficulty()
            else: raise ValueError

        except ValueError:
            print(f"{Fore.RED}[WARNING]{Style.RESET_ALL}" + " Please enter a valid option")
            print_line(1)

    def edit_difficulty(self):
        while self.difficulty_chosen == 0: self.set_difficulty()
        while not self.difficulty_confirmed: self.confirm_choice()
        self.maxRange = self.difficulty_modes[self.difficulty_chosen]["maxInt"]
        self.maxAttempts = self.difficulty_modes[self.difficulty_chosen]["maxAttempts"]
        self.remaining = self.difficulty_modes[self.difficulty_chosen]["maxAttempts"] - self.attempt + 1





########################################################################################################################
########################################################################################################################
########################################################################################################################


class Game(GameSettings):
    def __init__(self):
        super().__init__()

    def set_parameters(self, option):
        if option == 'difficulty':
            self.difficulty_chosen = self.retrieve_preferences('difficulty')
            self.maxRange = self.difficulty_modes[self.difficulty_chosen]['maxInt']
            self.maxAttempts = self.difficulty_modes[self.difficulty_chosen]['maxAttempts']
            self.remaining = self.maxAttempts

        if option == 'hint':
            self.hint_chosen = self.retrieve_preferences('hint')

    def print_difficulty(self, win_rate):
        print_space(1); print_line(1)
        print("Difficulty mode set to [{modeno}] {mode} ({win_rate}% win rate).".format(
            modeno=str(self.difficulty_chosen),
            mode=self.difficulty_modes[self.difficulty_chosen]["name"],
            win_rate=win_rate))

    def generate_number(self): self.answer = random.randint(1, self.maxRange)

    def play_game(self):
        print_space(1); print_line(1); print_space(1)
        print("Welcome!")
        print("You need to enter a number from 1 to {max}".format(max=self.maxRange))
        while self.answer != self.guess:
            if self.attempt > self.maxAttempts:
                print_line(1); print_space(1)
                print(f"{Fore.RED}You lose! The answer was {self.answer}{Style.RESET_ALL}")
                print_space(1); print_line(2);
                print_intro()
                main_menu()
                # create a function lose + potential rematch

            try:
                if self.hint_chosen and self.attempt:
                    if self.guess < self.answer: print("[Hint] It's higher than [{answer}]".format(answer=self.guess))
                    elif self.guess > self.answer: print("[Hint] It's lower than [{answer}]".format(answer=self.guess))
                self.guess = int(input(f"{Fore.YELLOW}[INPUT NEEDED]{Style.RESET_ALL}" + " {attempts} guesses left // Enter a number: ".format( attempts=self.remaining)))
                print_line(1)

                if 0 < self.guess <= self.maxRange:
                    self.attempt += 1
                    self.remaining -= 1

                else: raise ValueError

            except (TypeError, ValueError):
                print(f"{Fore.RED}[WARNING] You need to enter a number from 1 to {self.maxRange}{Style.RESET_ALL}")
        else:
            self.print_results()
            self.save_score()
            read_scores()
            print_line(1)
            print_intro()
            main_menu()
            # print("Want to play again?\n")
            # if int(input("Type 1:")) != 1: replay = False

    def print_results(self):
        print_space(1)
        print(f"{Fore.GREEN}Good JOB! The answer was [{self.answer}] and it took you [{self.attempt}] attempt(s) to find it!{Style.RESET_ALL}")
        print_space(1); print_line(1);


""" Game launch """
test_color()
print_intro()
main_menu()
