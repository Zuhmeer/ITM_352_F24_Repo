# Given the input of a student number, generate two integers 
# indicating the questions that a student needs to answer.
# 

def generate_numbers(a_student_id, num_questions):

# remove any non-numerical characters
    id = ''.join(filter(str.isdigit, a_student_id))

# check that the student id is valid (8 digits)
if len(id) != 8: 
    raise ValueError("Invalid student ID: it should be 8 digits")


# Use a simple algorithm to generate two distinct numbers from 1 to num_questions 
sum_digits = sum(int(digit) for digit in id)
first = (sum_digits % 7) + 1 

# calculate the second number using the prodcut of the digits 
product = 1
for digit in id: 
    if (int(digit)):
        product *= int(digit)
    second = (product % 7) + 1
    while first == second:
        second = (second % 7) + 1
  
    return first, second


try:
    N_QUESTIONS = 10
    student_id = input("Enter your student ID (XXX-XX-XXX)")
    num1, num2 = generate_numbers(student_id, N_QUESTIONS)
    print(f"Your two assignemnts are {num1} and {num2}")
except ValueError as e:
    print(f"Error {e}")
