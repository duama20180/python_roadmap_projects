
def greetings():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    print("\nPlease select the difficulty level:")
    print("1. Easy (10 chances)")
    print("2. Medium (5 chances)")
    print("3. Hard (3 chances)")

def get_difficulty():
    while True:
        try:
            choice = int(input("Please select a difficulty level:"))
            print("Enter a number 1, 2 or 3")
            if choice in [1, 2, 3]:
                return choice
        except ValueError:
            print("Invalid input. Please enter a number 1, 2 or 3")

def get_chances(difficulty):
    return {1:10, 2:5, 3:3}[difficulty]

def get_difficulty_name (difficulty):
    return {1:"Easy", 2:"Medium", 3:"Hard"}[difficulty]

def get_guess(guess):
    while True:
        try:
            guess = int(input("Please enter your guess:"))
            if 1 <= guess <= 100:
                return guess
            print("Please enter a number between 1 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 100.")

def provide_hint(guess, target, remaining):
    if remaining > 0:
        if guess > target:
            print(f"Incorrect guess. The number is less than {guess}. You have {remaining} remaining.")
        else:
            print(f" Incorrect guess. The number is greater than {guess}. You have {remaining} remaining.")
        if remaining >= 3 and (target % 2 == 0 and guess % 2 != 0 or target % 2 != 0 and guess % 2 == 0):
            print("Hint: The number's parity is different from your guess.")

