
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

