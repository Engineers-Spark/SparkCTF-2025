from secret import FLAG
import random
import os 

seed = random.seed(os.urandom(4))

def banner():
    print("Welcome to the Flag Guessing Game!")
    print("The rules are simple, you have to guess the 100 next numbers to get the flag.")
    print("Fail and you will be kicked out of the game.")

def choices():
    print("Choose an option:")
    print("1. get the next number")
    print("2. Guess the next number")
    print("3. Exit")

def main():
    banner()
    score = 0
    while True:
        choices()
        option = input("Enter your choice: ")
        if option == "1":
            print("Here is the next number: ", end="")
            print(random.randint(0,6969))
        elif option == "2":
            guess = int(input(f"Enter your guess number {score+1}"))
            if guess != random.randint(0,6969):
                print("Wrong guess! You are out of the game.")
                exit(1)
            score += 1
        elif option == "3":
            print("Goodbye!")
            return
        else:
            print("Invalid choice! Try again.")
            continue
        if score == 100:
            print(f"Congratulations! Here is your flag: {FLAG}")
            return


if __name__ == "__main__":
    main()