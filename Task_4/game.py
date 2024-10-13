import random

def get_computer_choice():
    return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "It's a tie!"
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'scissors' and computer_choice == 'paper') or \
         (user_choice == 'paper' and computer_choice == 'rock'):
        return "You win!"
    else:
        return "You lose!"

def play_game():
    user_score = 0
    computer_score = 0

    while True:
        print("\nChoose:")
        print("r - Rock")
        print("p - Paper")
        print("s - Scissors")
        
        user_input = input("Your choice: ").lower()

        if user_input not in ['r', 'p', 's']:
            print("Invalid choice. Please choose r, p, or s.")
            continue

        # Map user input to full choice
        user_choice = {'r': 'rock', 'p': 'paper', 's': 'scissors'}[user_input]
        
        computer_choice = get_computer_choice()
        print(f"Computer chose: {computer_choice}")

        result = determine_winner(user_choice, computer_choice)
        print(result)

        # Update scores
        if result == "You win!":
            user_score += 1
        elif result == "You lose!":
            computer_score += 1

        print(f"Score - You: {user_score}, Computer: {computer_score}")

        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again != 'y':
            break

    print("Thanks for playing!")

# Start the game
if __name__ == "__main__":
    play_game()