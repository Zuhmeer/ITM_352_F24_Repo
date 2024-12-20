# Quiz app using Flask 
from flask import Flask, render_template, request, redirect, url_for
from flask import flash
import json
import random
import time

app = Flask(__name__)
app.secret_key = 'some-random-secret-key'
 

USERS = {"zing": "zing123",
        "tlc": "t123"}

@app.route('/', methods=['GET', 'POST'])
def login():
    global userid
    if request.method == 'POST':
        userid = request.form.get('username').strip()
        userpass = request.form.get('password').strip()

        # Validate inputs
        if not userid or not userpass:
            flash("Username and password cannot be empty.", "error")
            return render_template('login.html')

        # Check the username and password. If successful, take the user to the success page.
        if USERS.get(userid) == userpass:
            return redirect(url_for('home', username=userid))
        else:
            flash("Incorrect username or password. Please try again.", "error")
            return render_template('login.html')

    return render_template('login.html')

@app.route('/home/<username>')
def home(username):
    return render_template('home.html', username=username)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    global question_num, score, feedback, start_time, hint_used

    # Total questions in the quiz
    total_questions = len(question_list)

    # Calculate progress percentage based on the current question number
    progress = int(((question_num - 1) / total_questions) * 100)

    # Handle the start of the quiz
    if question_num == 1 and request.method == 'GET':
        # Record the start time only at the beginning of the quiz
        start_time = time.time()

    if request.method == 'POST':
        # Get the selected option
        selected_option = request.form.get('option')
        if not selected_option:
            flash("Please select an option before proceeding.", "error")
            return redirect(url_for('quiz'))

        # Check if the answer is correct
        correct_answer = question_list[question_num - 1][1]["answer"]
        if selected_option == correct_answer:
            score += 1
            feedback = "Correct!"
        else:
            feedback = f"Incorrect! The correct answer was: {correct_answer}"

        # Move to the next question or end the quiz
        if question_num < total_questions:
            question_num += 1
            progress = int(((question_num - 1) / total_questions) * 100)  # Update progress for the next question
        else:
            return redirect(url_for('result'))

    # Fetch the current question
    current_question = question_list[question_num - 1]

    return render_template('quiz.html',
                           num=question_num,
                           question=current_question[0],
                           options=current_question[1]["options"],
                           feedback=feedback,
                           progress=progress,
                           hint_used=hint_used)


@app.route('/use_hint', methods=['POST'])
def use_hint():
    global hint_used, score

    if hint_used:
        flash("You can only use one hint per quiz.", "error")
        return redirect(url_for('quiz'))

    hint_used = True
    # Deduct 1 point for using the hint
    score = max(0, score - 1)

    current_question = question_list[question_num - 1]
    correct_answer = current_question[1]["answer"]
   
    # Provide the hint by revealing the correct answer without giving it directly
    hint = f"The correct answer starts with '{correct_answer[0]}'."

    return render_template('quiz.html', 
                           num=question_num, 
                           question=current_question[0], 
                           options=current_question[1]["options"],
                           feedback="Hint: " + hint, 
                           hint_used=hint_used)


@app.route('/result')
def result():
    global userid, start_time
    elapsed_time = time.time() - start_time  # Time taken in seconds
    elapsed_minutes = int(elapsed_time // 60)
    elapsed_seconds = int(elapsed_time % 60)
    time_taken = f"{elapsed_minutes} minutes and {elapsed_seconds} seconds"

    # Store results in a JSON file
    result_data = {
        "username": userid,
        "score": score,
        "time_taken": time_taken,
        "total_questions": len(question_list),
    }

    # Append the result to a results.json file
    try:
        with open("results.json", "r") as results_file:
            results = json.load(results_file)
    except FileNotFoundError:
        results = []

    results.append(result_data)

    try:
        with open("results.json", "w") as results_file:
            json.dump(results, results_file, indent=4)
    
    except Exception as e:
        print(f"Error saving results: {e}")
    
    return render_template('result.html',
                           score=score,
                           username=userid,
                           question_list=question_list,
                           time_taken=time_taken)
 
@app.route('/reset')
def reset_quiz():
    global question_num, score, feedback, question_list, hint_used

    # Reset variables
    question_num = 1
    score = 0
    feedback = ""
    hints_used = {i: False for i in range(len(question_list))}

    # Reload and randomize questions and answer options
    question_list = []
    for question, options in questions.items():
        shuffled_options = options[:-1]
        random.shuffle(shuffled_options)

        question_list.append((question, {
            "options": shuffled_options,
            "answer": options[-1]
        }))
    
    # Randomize the order of the questions and limit to 5
    random.shuffle(question_list)
    question_list = question_list[:5]
    return redirect(url_for('quiz'))

# Load the question file and convert it to a list
with open("questions.json") as question_file:
    questions = json.load(question_file)

question_list = []
for question, options in questions.items():
    # Shuffle answer options
    shuffled_options = options[:-1]
    random.shuffle(shuffled_options)

    # Add question with shuffled options
    question_list.append((question, {
        "options": shuffled_options,
        "answer": options[-1]  # Keep the correct answer as-is
    }))

# Shuffle the question list and limit to 5 questions
random.shuffle(question_list)
question_list = question_list[:5]

# Create some housekeeping variables
score = 0
question_num = 1
feedback = ""
userid = ""
hint_used = False

# Run the application
if __name__ == "__main__":
    app.run(debug=True)