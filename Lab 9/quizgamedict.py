import json

# Dictionary of quiz questions
quiz_questions = {
    "What Nintendo character wears overalls and white gloves": [
        "Mario", "Luigi", "Bowser", "Donkey Kong"
    ],
    "Which fictional character turns yellow when they enter their special form": [
        "Sonic", "Goku", "Charizard", "Kirby"
    ],
    "What games are available for Playstation and PC but not Xbox?": [
        "Helldivers", "God of War: Ragnorok", "Halo", "Call of Duty"
    ],
    "Which game is a Playstation exclusive game?": [
        "Uncharted", "Spiderman", "Grand Theft Auto", "For Honor"
    ],
    "Which horror movie has its killer wearing a mask": [
        "Jason Voorhees", "Michael Myers", "Freddy Kruger", "Pennywise"
    ]
}

# Save dictionary to a JSON file
with open("quiz_questions.json", "w") as json_file:
    json.dump(quiz_questions, json_file, indent=4)

print("Quiz questions have been saved to quiz_questions.json")


import json

# Open and read the JSON file
with open("quiz_questions.json", "r") as json_file:
    quiz_questions = json.load(json_file)

# Print the loaded JSON data
print("Quiz Questions from JSON file:")
for question, options in quiz_questions.items():
    print(f"\n{question}:")
    for option in options:
        print(f"- {option}")

