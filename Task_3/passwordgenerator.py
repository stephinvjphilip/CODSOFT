import random
import string

def get_user_input():
    length = int(input("Enter the desired length of the password (minimum 5): "))
    if length < 5:
        print("Password length should be at least 5.")
        return None, None
    
    include_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
    include_lowercase = input("Include lowercase letters? (y/n): ").lower() == 'y'
    include_digits = input("Include digits? (y/n): ").lower() == 'y'
    include_special = input("Include special characters? (y/n): ").lower() == 'y'

    return length, (include_uppercase, include_lowercase, include_digits, include_special)

def generate_password(length, options):
    characters = ''
    
    if options[0]:
        characters += string.ascii_uppercase
    if options[1]:
        characters += string.ascii_lowercase
    if options[2]:
        characters += string.digits
    if options[3]:
        characters += string.punctuation

    if not characters:
        print("At least one character type must be selected.")
        return None
    
    password = ''.join(random.choice(characters) for _ in range(length))
    
    return password

def display_password(password):
    if password:
        print(f"Generated Password: {password}")

def main():
    length, options = get_user_input()
    
    if length is not None:
        password = generate_password(length, options)
        display_password(password)

if __name__ == "__main__":
    main()