import random
import time


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
            print("Enter a number 1, 2 or 3")
            choice = int(input("Please select a difficulty level:"))
            if choice in [1, 2, 3]:
                return choice
        except ValueError:
            print("Invalid input. Please enter a number 1, 2 or 3")

def get_chances(difficulty):
    return {1:10, 2:5, 3:3}[difficulty]

def get_difficulty_name (difficulty):
    return {1:"Easy", 2:"Medium", 3:"Hard"}[difficulty]

def get_guess():
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

def update_high_score (difficulty, attempts, high_scores ):
    difficulty_name = get_difficulty_name(difficulty)
    if high_scores[difficulty_name] is None or attempts < high_scores[difficulty_name]:
        high_scores[difficulty_name] = attempts

def display_high_scores(high_scores):
    print("\nHigh score:")
    for diff, score in high_scores.items():
        print(f"{diff}: {score if score is not None else 'No score yet'}")

def play_again():
    while True:
        choice = input("Would you like to play again? (y/n) ")
        if choice in ["y", "n"]:
            return choice == "y"
        print("Invalid input. Please enter y or n.")

def main():
    high_scores = {"Easy":None, "Medium":None, "Hard":None}

    while True:
        greetings()
        difficulty = get_difficulty()
        chances = get_chances(difficulty)

        print(f"\nGreat! You have selected the {get_difficulty_name(difficulty)} difficulty level.")
        print("Let's start the game!")

        target = random.randint(1, 100)
        attempts = 0
        start_time = time.time()

        while attempts < chances:
            guess = get_guess()
            attempts += 1

            if guess == target:
                end_time = time.time()
                print(f"Congratulations! You guessed the correct number in {attempts} attempts.")
                print(f"Time taken: {end_time - start_time} seconds.")
                update_high_score(difficulty, attempts, high_scores)
                break
            provide_hint(guess, target, chances - attempts)
        if attempts >= chances and guess != target:
            print(f"Game over. The correct number was {target}.")
        display_high_scores(high_scores)
        if not play_again():
            print("Thank you for playing!")

if __name__ == "__main__":
    main()

