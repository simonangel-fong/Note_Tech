# py file of demo: Rock, paper, and scissors game
# print topic: function, input, if expression, exception
import random

OPTION_LIST = ["rock",  "paper",  "scissors"]


class MyError(Exception):
    '''A customized Error used to quit game'''

    def __init__(self, err_msg):
        self.err_msg = err_msg

    def __str__(self):
        return self.err_msg


def get_choices():
    user_choice = input(
        "\nInput your choice\n0: Rock\n1: Paper\n2: Scissors\nq: Quit Game\n>> ")
    if user_choice == "q":
        raise MyError("Quit Game")
    computer_choice = random.randint(0, 2)
    choices = {"user": int(user_choice), "computer": computer_choice}
    return choices


def get_result(user, computer):
    if (user == computer):
        return f"\nUser choice:\t\t {OPTION_LIST[user]}\nComputer choice:\t {OPTION_LIST[computer]}\nResult:\t\t\t Tie Game"
    elif user+1 == computer or (user == 2 and computer == 0):
        return f"\nUser choice:\t\t {OPTION_LIST[user]}\nComputer choice:\t {OPTION_LIST[computer]}\nResult:\t\t\t Computer Wins."
    else:
        return f"\nUser choice:\t\t {OPTION_LIST[user]}\nComputer choice:\t {OPTION_LIST[computer]}\nResult:\t\t\t User Wins."


print("\n--------Rock, paper, and scissors game--------\n")

while (True):
    try:
        choices = get_choices()
        result = get_result(choices["user"], choices["computer"])
        print(result)
    except ValueError:
        print("\nError: Input Must be number!")
        continue
    except IndexError:
        print("\nError: Input Must be 0, 1, or 2!")
        continue
    except MyError as e:
        print(f"\n{e}")
        break

print("\n--------End game--------\n")
