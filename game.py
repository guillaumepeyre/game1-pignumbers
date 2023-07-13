import random
from colorama import Fore
from colorama import Style
import game_settings
import game_functions

class Game(game_settings.GameSettings):
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
        game_functions.print_space(1)
        game_functions.print_line(1)
        print("Difficulty mode set to [{modeno}] {mode} ({win_rate}% win rate).".format(
            modeno=str(self.difficulty_chosen),
            mode=self.difficulty_modes[self.difficulty_chosen]["name"],
            win_rate=win_rate))

    def generate_number(self):
        self.answer = random.randint(1, self.maxRange)

    def play_game(self):
        game_functions.print_space(1)
        game_functions.print_line(1)
        game_functions.print_space(1)
        print(f"{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}OINK OINK! LET THE GAMES BEGIN!{Style.RESET_ALL}")
        print(f"{Fore.LIGHTMAGENTA_EX}You need to enter a number from 1 to {self.maxRange}{Style.RESET_ALL}")
        while self.answer != self.guess:
            if self.attempt >= self.maxAttempts:
                game_functions.print_line(1);
                game_functions.print_space(1)
                print(f"{Fore.RED}:sad-pig-emoji: Oiink.... You lose! The answer was {self.answer}{Style.RESET_ALL}")
                game_functions.print_space(1);
                game_functions.print_line(2);
                game_functions.main_menu()
                # create a function lose + potential rematch

            try:
                game_functions.print_space(1)
                if self.hint_chosen and self.attempt:
                    if self.guess < self.answer:
                        print("*PIG WHISPER* SHhHhh.. It's higher than [{answer}]".format(answer=self.guess))
                    elif self.guess > self.answer:
                        print("*PIG WHISPER* SHhHhh.. It's lower than [{answer}]".format(answer=self.guess))
                self.guess = int(input(
                    f"{Fore.YELLOW}[PIG ORDER]{Style.RESET_ALL}" + " {attempts} guesses left // Enter a number: ".format(
                        attempts=self.remaining)))

                if 0 < self.guess <= self.maxRange:
                    self.attempt += 1
                    self.remaining -= 1

                else:
                    raise ValueError

            except (TypeError, ValueError):
                print(f"{Fore.RED}[PIG ANGRY!] I said a number from 1 to {self.maxRange}!{Style.RESET_ALL}")
        else:
            self.print_results()
            self.save_score()
            game_functions.read_scores()
            game_functions.print_line(1)
            game_functions.print_intro1()
            game_functions.main_menu()
            # print("Want to play again?\n")
            # if int(input("Type 1:")) != 1: replay = False

    def print_results(self):
        game_functions.print_space(1);
        game_functions.print_line(1);
        game_functions.print_space(1)
        print(
            f"{Fore.GREEN}Oooink Oiiiink (aka. \"Good job!\"). The answer was [{self.answer}] and it took you [{self.attempt}] attempt(s) to find it!{Style.RESET_ALL}")
        game_functions.print_space(1);
        game_functions.print_line(1);

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