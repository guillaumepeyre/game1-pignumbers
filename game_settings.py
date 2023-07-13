import csv
import pandas as pd
from colorama import Fore
from colorama import Style

import game_functions

class GameSettings:
    difficulty_modes = {
        1: {"name": "Baby Pig", "maxInt": 10, "maxAttempts": 7},
        2: {"name": "Angry Pig", "maxInt": 30, "maxAttempts": 10},
        3: {"name": "Mean Pig", "maxInt": 60, "maxAttempts": 12},
        4: {"name": "Crazy Pig", "maxInt": 100, "maxAttempts": 15},
        5: {"name": "Lord Piggy", "maxInt": 500, "maxAttempts": 10}
    }

    hint_modes = [0, 1]

    def __init__(self, difficulty=1, difficulty_confirmed=True):
        self.difficulty_chosen = difficulty
        self.difficulty_confirmed = difficulty_confirmed
        self.hint_chosen = 0
        self.attempt = 0
        self.guess = 0
        self.answer = 0
        self.games_id = game_functions.read_game_id()

        if difficulty:
            self.maxRange = self.difficulty_modes[self.difficulty_chosen]['maxInt']
            self.maxAttempts = self.difficulty_modes[self.difficulty_chosen]['maxAttempts']
            self.remaining = self.maxAttempts

    def preferences_file_check(self):
        if game_functions.file_exists('preferences.csv'):
            # if row 'difficulty' or 'hint' doesn't exist, reset preferences file to default
            if game_functions.find_index('difficulty') == -1 or game_functions.find_index('hint') == -1: game_functions.set_basic_preference()

            # Look for main parameters indexes
            index_difficulty = game_functions.find_index('difficulty')
            index_hint = game_functions.find_index('hint')

            df = pd.read_csv('preferences.csv')

            # if difficulty value isn't OK
            if df.at[index_difficulty, 'value'] not in self.difficulty_modes:
                self.difficulty_chosen = 1
                game_functions.write_preferences(index_difficulty, 1)

            # if hint value isn't OK
            if df.at[index_hint, 'value'] not in self.hint_modes:
                self.hint_chosen = 0
                game_functions.write_preferences(index_hint, 0)

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
        csv_file_exists = game_functions.file_exists("scores.csv")

        with open('scores.csv', 'a+', newline='') as score_csv:
            fieldnames = ['id', 'attempts']
            score_writer = csv.DictWriter(score_csv, fieldnames=fieldnames)

            if csv_file_exists is not True:
                score_writer.writeheader()
                self.games_id = 1

            score_writer.writerow({'id': self.games_id, 'attempts': self.attempt})

    # Return value of an option in preferences.csv. Raised FileNotFoundError if file doesn't exists
    def retrieve_preferences(self, option):
        if game_functions.file_exists('preferences.csv'):
            # Different formula - set default at launch
            if option == 'difficulty':
                df = pd.read_csv('preferences.csv')
                # Need to control if value doesn't exists.
                index = game_functions.find_index('difficulty')
                if df.at[index, 'value'] in self.difficulty_modes:
                    return df.at[index, 'value']
                else:
                    return 0

            if option == 'hint':
                df = pd.read_csv('preferences.csv')
                # Need to control if value doesn't exists.
                index = game_functions.find_index('hint')
                if df.at[index, 'value'] in self.hint_modes:
                    return df.at[index, 'value']
                else:
                    return 0

        else:
            raise FileNotFoundError

    def toggle_hint(self):
        print(
            """[Hint Mode] It makes the game easier by letting you know if the answer is higher or lower than your input.""")
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
        game_functions.write_preferences(game_functions.find_index('hint'), self.hint_chosen)

    # Automate print statement based on difficulty mode and replace win rate with attempt/guesses
    def set_difficulty(self):
        len_difficulty_modes = len(self.difficulty_modes)

        game_functions.print_space(1)
        print(f"{Style.BRIGHT}Meet some of my pig pals... Type a number below:{Style.RESET_ALL}")
        for i in self.difficulty_modes:
            iter_name = self.difficulty_modes[i]['name']
            iter_range = self.difficulty_modes[i]['maxInt']
            iter_attempts = self.difficulty_modes[i]['maxAttempts']
            print(
                f"\t[{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}{i}{Style.RESET_ALL}] {iter_name} \t\tGuess range: 1-{iter_range}\t\tMax attempts: {iter_attempts}")

        game_functions.print_space(1)

        try:
            difficulty_input = int(input(
                f"{Fore.YELLOW}[PIG ORDER]{Style.RESET_ALL}" + " Enter an option now! (1-{max}):\n>>> ".format(
                    max=len_difficulty_modes)))

            if difficulty_input in self.difficulty_modes:
                self.difficulty_chosen = difficulty_input
            else:
                raise ValueError

        except ValueError:
            print(self.difficulty_chosen)
            print(difficulty_input in self.difficulty_modes)
            print(f"{Fore.RED}[OINK!]{Style.RESET_ALL}" + " Please enter a valid number.")

    def confirm_choice(self):
        try:
            game_functions.print_space(1)
            choice = input(
                "Please enter " + f"{Fore.GREEN}[Y]{Style.RESET_ALL}" + " to confirm or " + f"{Fore.RED}[N]{Style.RESET_ALL}" + " to choose a new difficulty setting.\n>>> ")
            if choice == "Y" or choice == "y":
                game_functions.write_preferences(game_functions.find_index('difficulty'), self.difficulty_chosen)
                self.difficulty_confirmed = True

            elif choice == "N" or choice == "n":
                self.set_difficulty()
            else:
                raise ValueError

        except ValueError:
            print(f"{Fore.RED}[OINK!]{Style.RESET_ALL}" + " Please enter a valid option")
            game_functions.print_line(1)

    def edit_difficulty(self):
        while self.difficulty_chosen == 0: self.set_difficulty()
        while not self.difficulty_confirmed: self.confirm_choice()
        self.maxRange = self.difficulty_modes[self.difficulty_chosen]["maxInt"]
        self.maxAttempts = self.difficulty_modes[self.difficulty_chosen]["maxAttempts"]
        self.remaining = self.difficulty_modes[self.difficulty_chosen]["maxAttempts"] - self.attempt
