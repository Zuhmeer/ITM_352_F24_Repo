# make a quiz game / application 

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

Score = 0

# Using a for loop to sort the answers in alphabetical order
# so that the answer won't always be the first and second index in the list
for question, answers in QUESTIONS.items():
    correct_answer = answers[0]
    correct_answer2 = answers[1]
    for answers in sorted(answers):
        print(f"{answers}")

# Asks for user input to pick one of two of the possible answers
    answer = input(f"{question}? ")
    if answer == correct_answer or answer == correct_answer2:
        print("Correct!")
        Score += 1
    else:
        print("Wrong!")
        print(f"The answer is {correct_answer} or {correct_answer2}, not {answer}!")

print(f"Your final score is {Score}/5")