# !/usr/bin/env python

import random
import csv
import os.path
import pandas as pd

from colorama import init
from termcolor import colored

init()

########################################################################################################################
########################################################################################################################
"""
GLOBAL VARIABLES
> Overwritten if valid data exists in 'preferences.csv'
"""
""" 
Take difficulty function out of game object, maybe move to game settings or global
> Not connected to a game - it's only edited outside of a game now 

settings doesn't change dif
new game default to dif 1

"""


"""
GLOBAL FUNCTIONS
"""

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
What would you like to do? Please enter [1] or [2]:
\t [1] Play a game
\t [2] Reset scores (this CANNOT be undone!)
\t [3] Go back to main menu
""")
    # 1 Play
    # 2 Reset score (THIS CANNOT BE UNDONE)
    # 3 Go back to menu
    # main_menu()

    try:
        option = int(input(colored("[INPUT NEEDED]", 'yellow') + " Enter an option below (1-2): "))
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
        else: print('boo')

    except ValueError:
        print(colored("[WARNING]", 'red') + "  Please enter a valid option")


def read_game_id():
    try:
        with open("scores.csv", newline='') as score_file_object:
            # Check if file is empty and set-up a variable
            file_rows = len(score_file_object.readlines())
            if file_rows == 1:
                return 1
            else:
                return file_rows

    except FileNotFoundError:
        return 1


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

    else: return -1


def set_basic_preference():
    with open('preferences.csv', 'w+', newline='') as preference_csv:
        fieldnames = ['name', 'value']
        preference_writer = csv.DictWriter(preference_csv, fieldnames=fieldnames)
        preference_writer.writeheader()
        preference_writer.writerow({'name': 'difficulty', 'value': 1})
        preference_writer.writerow({'name': 'hint', 'value': 0})
        # new_game.difficulty_chosen = 1
def write_pref(index, value):
    #break down retrieve into write_preferences. Retrieve gives you index, and write actually write value or default to 1)
    # Check if value is expected, if not default to Easy mode
    df = pd.read_csv('preferences.csv')
    df.at[index, 'value'] = value
    print(index)
    print(value)
    df.to_csv('preferences.csv', index=False)


def read_preference(option):
    try:
        with open("preferences.csv", newline='') as preference_object:
            if option == "difficulty":
                reader = csv.DictReader(open("preferences.csv"))
                for row in reader:
                    name = row['name']
                    value = row['value']
                    if name == 'difficulty':
                        return int(value)
            elif option == "hint":
                pass
            else:
                raise FileNotFoundError

    except FileNotFoundError:
        return False


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

            for rows in score_file_reader: print(
                "- Game no. {id}: Won in {attempts} attempt(s)".format(id=rows['id'], attempts=rows['attempts']))

            if is_file_empty is True: raise FileNotFoundError

            score_menu_options()
            # Play again?

    except FileNotFoundError:
        print_space(1);
        print(colored("It doesn't look like you've played any games yet!", 'red'))
        main_menu()


def start_game():
    # Create new instance of a game
    new_game = Game()

    # check also change variable to overwrite wrong value
    new_game.preferences_file_check()

    # set difficulty now that file is OK
    new_game.set_parameters('difficulty')

    # generate number to be guessed and launch game
    new_game.generate_number()
    new_game.play_game()
def main_menu():
    print_space(1);
    print_line(1)
    print("""Please start by choosing one of those options. Type a number from 1-4:
    [1] Play Game
    [2] Open Settings
    [3] View Scoreboard
    [4] Exit
    """)

    try:
        option = int(input(colored("[INPUT NEEDED]", 'yellow') + " Enter an option below (1-4): "))

        if option == 1: start_game()
        elif option == 2: open_settings()
        elif option == 3: read_scores()
        elif option == 4: exit()
        else: raise ValueError

    except ValueError:
        print_space(1)
        print(colored("[WARNING]", 'red') + " Please enter a valid number")
        main_menu()


def open_settings():
    print_space(1);
    print_line(1)
    print("""You are in [SETTINGS]. Please choose an option below by entering a number:
    [1] Set difficulty
    [2] Enable/Disable Hint mode
    [3] Go back to main menu
    """)

    try:
        option = int(input(colored("[INPUT NEEDED]", 'yellow') + " Enter an option below (1-3): "))

        if option == 1:
            new_game = GameSettings(0, False)
            new_game.edit_difficulty()
            main_menu()
        elif option == 2: pass
        elif option == 3: main_menu()
        else: raise ValueError

    except ValueError:
        print_space(1)
        print(colored("[WARNING]", 'red') + " Please enter a valid number")
        main_menu()


def calculate_difficulty(dictionary, key): return dictionary[key]["maxAttempts"] / dictionary[key]["maxInt"] * 100

def file_exists(file):
    if os.path.exists(file): return True
    else: return False

########################################################################################################################
########################################################################################################################


class GameSettings():
    difficulty_modes = {
        1: {"name": "Easy", "maxInt": 2, "maxAttempts": 7},
        2: {"name": "Medium", "maxInt": 20, "maxAttempts": 10},
        3: {"name": "Hard", "maxInt": 50, "maxAttempts": 12}
    }

    hint_modes = [0, 1]

    def __init__(self,difficulty=1,difficulty_confirmed=True):
        self.difficulty_chosen = difficulty
        self.difficulty_confirmed = difficulty_confirmed
        self.attempt = 0
        self.guess = 0
        self.answer = 0
        self.hint_chosen = 0
        self.games_id = read_game_id()

        if difficulty:
            self.maxRange = self.difficulty_modes[self.difficulty_chosen]['maxInt']
            self.maxAttempts = self.difficulty_modes[self.difficulty_chosen]['maxAttempts']
            self.remaining = self.maxAttempts

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
            #different formulat - set default at launch
            if option == 'difficulty':
                df = pd.read_csv('preferences.csv')
                #need to control if value doesn't exists.
                index = find_index('difficulty')
                if df.at[index, 'value'] in self.difficulty_modes: return df.at[index, 'value']
                else: return 0

        else: raise FileNotFoundError

            # if df.at[index, 'value'] in self.difficulty_modes:
            #     self.difficulty_chosen = df.at[index, 'value']
            # else:
            #     set_basic_preference()
            # #
            # else:
            #     # No preference option value but file exists. Create headers + default values
            #     df1 = pd.DataFrame(pd.read_csv('preferences.csv'), index=[0])
            #     df2 = pd.Series({'name': option, 'value': default})
            #     df3 = pd.concat([df1, df2.to_frame().T], ignore_index=True)
            #     df3.to_csv('preferences.csv', index=False)
            #     # new_game.difficulty_chosen = 1

        # if file doesn't exist, default to 1


    def set_difficulty(self):
        print("""
Please start by choosing your difficulty settings. Type a number from 1-3:
    [1] Easy mode (70% win rate)
    [2] Medium mode (50% win rate)
    [3] Hard mode (25% win rate)
""")
        try:
            difficulty_input = int(input(colored("[INPUT NEEDED]", 'yellow') + " Enter your difficulty settings (1-3):\n>>> "))

            if difficulty_input in self.difficulty_modes: self.difficulty_chosen = difficulty_input
            else: raise ValueError

        except ValueError:
            print(self.difficulty_chosen)
            print(difficulty_input in self.difficulty_modes)
            print(colored("[WARNING]", 'red') + "  Please enter a valid number.")

    def confirm_choice(self):
        try:
            choice = input("Please enter " + colored("[Y]", 'green') + " to confirm or " + colored("[N]",'red') + " to choose a new difficulty setting.\n>>> ")
            if choice == "Y" or choice == "y":
                # write_preference("difficulty", )
                # self.retrieve_preferences('difficulty', self.difficulty_chosen)
                # difficulty_chosen = self.retrieve_preferences('difficulty')
                write_pref(find_index('difficulty'), self.difficulty_chosen)

                self.difficulty_confirmed = True

            elif choice == "N" or choice == "n":
                # self.difficulty_confirmed = False
                self.set_difficulty()
            else:
                raise ValueError

        except ValueError:
            print(colored("[WARNING]", 'red') + " Please enter a valid option")
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
        # super().difficulty_chosen = difficulty

    def set_parameters(self, option):
        if option == 'difficulty':
            self.difficulty_chosen = read_preference('difficulty')
            self.maxRange = self.difficulty_modes[self.difficulty_chosen]['maxInt']
            self.maxAttempts = self.difficulty_modes[self.difficulty_chosen]['maxAttempts']
            self.remaining = self.maxAttempts

    # @property
    def preferences_file_check(self):
        if file_exists('preferences.csv'):
            # if value difficulty doesn't exist, reset preferences file to default
            if find_index('difficulty') == -1 or find_index('hint') == -1: set_basic_preference()
            print(find_index('difficulty'))

            # Look for main parameters indexes
            index_difficulty = find_index('difficulty')
            index_hint = find_index('hint')

            df = pd.read_csv('preferences.csv')

            # if difficulty value isn't OK
            if df.at[index_difficulty, 'value'] not in self.difficulty_modes:
                self.difficulty_chosen = 1
                write_pref(index_difficulty, 1)

            # if hint value isn't OK
            if df.at[index_hint, 'value'] not in self.hint_modes:
                self.hint_chosen = 1
                write_pref(index_hint, 0)

        # if file doesn't exist, default to 1
        else:
            with open('preferences.csv', 'w+', newline='') as preference_csv:
                fieldnames = ['name', 'value']
                preference_writer = csv.DictWriter(preference_csv, fieldnames=fieldnames)
                preference_writer.writeheader()
                preference_writer.writerow({'name': 'difficulty', 'value': 1})
                preference_writer.writerow({'name': 'hint', 'value': 0})
                return True
                # new_game.difficulty_chosen = 1

        #
        #     else:
        #         #No difficulty value but file exists. Create headers + default values
        #         df1 = pd.DataFrame(pd.read_csv('preferences.csv'), index=[0])
        #         df2 = pd.Series({'name': 'difficulty', 'value': 1})
        #         df3 = pd.concat([df1, df2.to_frame().T], ignore_index=True)
        #         df3.to_csv('preferences.csv', index=False)
        #         # new_game.difficulty_chosen = 1
        #
        #


    def print_difficulty(self, win_rate):
        print_space(1)
        print_line(1)
        print("Difficulty mode set to [{modeno}] {mode} ({win_rate}% win rate).".format(
            modeno=str(self.difficulty_chosen),
            mode=self.difficulty_modes[self.difficulty_chosen]["name"],
            win_rate=win_rate))

    def generate_number(self): self.answer = random.randint(1, self.maxRange)

    def play_game(self):
        print_space(1)
        print_line(1)
        print("\tWelcome!")
        print("\tYou need to enter a number from 1 to {max}".format(max=self.maxRange))
        while self.answer != self.guess:
            if self.attempt > self.maxAttempts:
                print_line(1)
                print(colored("You lose! The answer was [{answer}]".format(answer=self.answer), 'red'))
                print_line(2);
                print_intro()
                main_menu()
                # create a function lose + potential rematch

            try:
                self.guess = int(input(colored("[INPUT NEEDED]", 'yellow') + " {attempts} guesses left // Enter a number: ".format( attempts=self.remaining)))
                print_line(1)

                if 0 < self.guess <= self.maxRange:
                    self.attempt += 1
                    self.remaining -= 1

                else:
                    raise ValueError

            except (TypeError, ValueError):
                print(colored("[WARNING] You need to enter a number from 1 to {max}".format(max=self.maxRange), 'red'))
        else:
            self.print_results()
            self.save_score()
            read_scores()

            print_line(1)
            # Relaunch game
            print_intro()
            main_menu()
            # print("Want to play again?\n")
            # if int(input("Type 1:")) != 1: replay = False

    def print_results(self):
        print_space(1);
        print_line(1);
        print_space(1)
        print("Good JOB! The answer was [{answer}] and it took you [{attempts}] attempt(s) to find it!".format(
            answer=self.answer, attempts=self.attempt))
        print_space(1);
        print_line(1);
        print_space(1)


""" Gasme launch """
# new_game = Game()
# new_game.edit_difficulty()


print_intro()
main_menu()