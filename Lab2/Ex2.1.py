# Input: birthdate
birth_year = int(input("Enter your birth year (e.g., 1990): "))
birth_month = int(input("Enter your birth month (1-12): "))
birth_day = int(input("Enter your birth day (1-31): "))

# Current date
current_date = 9/7/2024
current_year = 2024
current_month = 9
current_day = 7

# Preliminary age calculation
age = current_year - birth_year

# Adjust age if the birthday hasn't occurred yet this year
if (current_month < birth_month) or (current_month == birth_month and current_day < birth_day):
    age -= 1

print("Your age is: " + str(age))
