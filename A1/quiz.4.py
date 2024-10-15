# Interactive quiz game where each question has four possible answers 

QUESTIONS = {
    "What is the airspeed of a unladen swallow in miles/hr": ["12", "11", "8", "14"],
    "What is the capital if Texas": ["Austin", "Dallas", "Houston", "San Antonio"], 
    "The Last Supper was painted by which Artist": ["Da Vinci", "Picasso", "Rembrandt", "Michelangelo"]
}

for question, alternatives in QUESTIONS.items():
    correct_answer = alternatives[0]
    sorted_alternatives = sorted(alternatives)
    for label, alternative in enumerate (sorted_alternatives):
        print(f" {label}: {alternative}")

    answer_label = int(input(f"{question}?"))
    answer = sorted_alternatives[answer_label]
    
    if answer == correct_answer:
            print("Correct!")
    else:
        print(f"The correct answer is {correct_answer!r}, not  {answer!r}")

        