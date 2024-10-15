# Interactive quiz game with questions and answers in a list 

QUESTIONS = [ 
    "What is the airspeed of a unladen swallow in miles/hr": ["12", "11", "8", "14"]
    "What is the capital if Texas": ["Austin", "Dallas", "Houston", "San Antonio"] 
    "The Last Supper was painted by which Artist": ["Da Vinci", "Picasso", "Rembrandt", "Michelangelo"]
    ]

for question, correct_answer in QUESTIONS:
    answer = input(f"{question}? ")
    if answer == correct_answer:
        print("Correct!")
else: 
        print(f"The answer is {correct_answer!r}, not {answer!r}")

# "Who won Superbowl XXXIV": ["Rams"]