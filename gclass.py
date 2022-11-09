#!/usr/bin/env python

import random
import csv
import os.path

from colorama import init
from termcolor import colored

init()

########################################################################################################################
########################################################################################################################
"""
This is the beginning of a story of love. Sashay away!
- # Check if file exists, if not create new one when game ends
-- # games played: len of readlines
-- New option at beginning
--- Game start: Option 1: Play Game / Option 2: View Scoreboard / Option 3: Exit Game 
-- Store 3 info: Game ID, Game difficulty, # attempts
-- Add global variable SCORES.TXT etc

Should I store lose too? Win ratio? would need to remove statick win rate

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
\t [1] Reset scores (this CANNOT be undone!)
\t [2] Go back to main menu
""")
    # 1 Reset score (THIS CANNOT BE UNDONE)
    # 2 Go back to menu
    # main_menu()

    try:
        option = int(input(colored("[INPUT NEEDED]", 'yellow') + " Enter an option below (1-2): "))
        if option == 1:
            with open('scores.csv', 'w+', newline='') as score_csv:
                fieldnames = ['id', 'attempts']
                score_writer = csv.DictWriter(score_csv, fieldnames=fieldnames)
                score_writer.writeheader()

            print_space(1)
            print("You score have been reset.")
            main_menu()

        elif option == 2:
            main_menu()
        else:
            raise ValueError

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


def main_menu():
    print_space(1);
    print_line(1)
    print("""Please start by choosing one of those options. Type a number from 1-3:
    [1] Play Game
    [2] View Scoreboard
    [3] Exit
    """)

    try:
        option = int(input(colored("[INPUT NEEDED]", 'yellow') + " Enter an option below (1-3): "))

        if option == 1:
            new_game = Game(0)
            new_game.edit_difficulty()
            new_game.generate_number()
            new_game.play_game()
        elif option == 2:
            read_scores()
        elif option == 3:
            exit()
        else:
            raise ValueError

    except ValueError:
        print_space(1)
        print(colored("[WARNING]", 'red') + " Please enter a valid number")
        main_menu()


def calculate_difficulty(dictionary, key): return dictionary[key]["maxAttempts"] / dictionary[key]["maxInt"] * 100

########################################################################################################################
########################################################################################################################


class GameSettings():
    difficulty_modes = {
        1: {"name": "Easy", "maxInt": 10, "maxAttempts": 7},
        2: {"name": "Medium", "maxInt": 20, "maxAttempts": 10},
        3: {"name": "Hard", "maxInt": 50, "maxAttempts": 12}
    }

    def __init__(self, difficulty_chosen):
        self.difficulty_chosen = difficulty_chosen
        self.attempt = 0
        self.guess = 0
        self.answer = 0
        self.difficulty_confirmed = False
        self.games_id = read_game_id()

        # Define in child class Game() edit_difficulty()
        self.maxRange = 0
        self.maxAttempts = 0
        self.remaining = 0

    def save_score(self):
        if os.path.exists("scores.csv"): csv_file_exists = True
        else: csv_file_exists = False

        with open('scores.csv', 'a+', newline='') as score_csv:
            fieldnames = ['id', 'attempts']
            score_writer = csv.DictWriter(score_csv, fieldnames=fieldnames)

            if csv_file_exists is not True:
                score_writer.writeheader()
                self.games_id = 1

            score_writer.writerow({'id': self.games_id, 'attempts': self.attempt})

########################################################################################################################
########################################################################################################################
########################################################################################################################


class Game(GameSettings):
    def __init__(self, difficulty):
        super().__init__(difficulty)

    def print_difficulty(self, win_rate):
        print_space(1)
        print_line(1)
        print("Difficulty mode set to [{modeno}] {mode} ({win_rate}% win rate).".format(
            modeno=str(self.difficulty_chosen),
            mode=self.difficulty_modes[self.difficulty_chosen]["name"],
            win_rate=win_rate))

    def generate_number(self):
        self.answer = random.randint(1, self.maxRange)

    def play_game(self):
        print_space(1); print_line(1)
        print("\tWelcome!")
        print("\tYou need to enter a number from 1 to {max}".format(max=self.maxRange))
        while self.answer != self.guess:
            if self.attempt > self.maxAttempts:
                print_line(1)
                print(colored("You lose! The answer was [{answer}]".format(answer=self.answer), 'red'))
                print_line(2); print_intro()
                main_menu()
                # create a function lose + potential rematch

            try:
                self.guess = int(input(colored("[INPUT NEEDED]", 'yellow') + " {attempts} guesses left // Enter a number: ".format(attempts=self.remaining)))
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
        print_space(1); print_line(1); print_space(1)
        print("Good JOB! The answer was [{answer}] and it took you [{attempts}] attempt(s) to find it!".format(
            answer=self.answer, attempts=self.attempt))
        print_space(1); print_line(1); print_space(1)

    def set_difficulty(self):
        print("""
Please start by choosing your difficulty settings. Type a number from 1-3:
    [1] Easy mode (70% win rate)
    [2] Medium mode (50% win rate)
    [3] Hard mode (25% win rate)
""")
        try:
            difficulty_input = int(
                input(colored("[INPUT NEEDED]", 'yellow') + " Enter your difficulty settings (1-3):\n>>> "))

            if difficulty_input in self.difficulty_modes:
                win_rate = calculate_difficulty(self.difficulty_modes, difficulty_input)
                self.difficulty_chosen = difficulty_input
                self.print_difficulty(win_rate)
            else: raise ValueError

        except ValueError:
            print(colored("[WARNING]", 'red') + "  Please enter a valid number.")

    def confirm_choice(self):
        try:
            choice = input("Please enter " + colored("[Y]", 'green') + " to confirm or " + colored("[N]",'red') + " to choose a new difficulty setting.\n>>> ")
            if choice == "Y" or choice == "y": self.difficulty_confirmed = True
            elif choice == "N" or choice == "n":
                self.difficulty_confirmed = False
                self.set_difficulty()
            else: raise ValueError

        except ValueError:
            print(colored("[WARNING]", 'red') + " Please enter a valid option")
            print_line(1)

    def edit_difficulty(self):
        while self.difficulty_chosen == 0: self.set_difficulty()
        while not self.difficulty_confirmed: self.confirm_choice()
        self.maxRange = self.difficulty_modes[self.difficulty_chosen]["maxInt"]
        self.maxAttempts = self.difficulty_modes[self.difficulty_chosen]["maxAttempts"]
        self.remaining = self.difficulty_modes[self.difficulty_chosen]["maxAttempts"] - self.attempt + 1