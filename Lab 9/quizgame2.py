QUESTIONS = {
    "What Nintendo character wears overalls and white gloves": [
        "Mario", "Luigi", "Bowser", "Donkey Kong"
    ],
    "Which fictional character turns yellow when they enter their special form": [
        "Sonic", "Goku", "Charizard", "Kirby"
    ],
    "What games are available for Playstation and PC but not Xbox?": [
        "Helldivers", "God of War: Ragnorok", "Halo", "Call of Duty"
    ],
    "Which game is a playstation exclusive game?": [
        "Uncharted",
        "Spiderman",
        "Grand Theft Auto",
        "For Honor",
    ],
    "Which horror movie has its killer wearing a mask": [
        "Jason Voorhees",
        "Michael Myers",
        "Freddy Kruger",
        "Pennywise",
    ],
}

# Initialize score
score = 0
total_questions = len(QUESTIONS)

# Using a for loop to sort the answers in alphabetical order
for question, answers in QUESTIONS.items():
    correct_answer = answers[0]
    correct_answer2 = answers[1]
    
    # Sort the answers alphabetically
    sorted_answers = sorted(answers)
    
    # Print sorted answers
    for answer in sorted_answers:
        print(f"{answer}")
    
    # Ask for user input and keep prompting until a valid response is given
    while True:
        user_answer = input(f"{question}? ")

        # Check if user answer is in the list of valid answers
        if user_answer in sorted_answers:
            break
        else:
            print(f"'{user_answer}' is not a valid response. Please choose from the given options.")

    # Check if the answer is correct and update the score
    if user_answer == correct_answer or user_answer == correct_answer2:
        print("Correct!")
        score += 1  # Increment score for a correct answer
    else:
        print("Wrong!")
        print(f"The correct answer is {correct_answer} or {correct_answer2}, not {user_answer}!")
    print()  # Blank line for spacing between questions

# Display final score
print(f"Quiz complete! You got {score} out of {total_questions} questions correct.")
