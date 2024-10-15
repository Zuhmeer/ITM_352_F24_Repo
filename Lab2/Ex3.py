# Ask the user to enter a number between 1 and 100. Square the number
# and return the value to the user. 
# Name: Zamir Ingram 
# Date created: 9/4/2024

value_entered = input("Please enter a value between 1 and 100: ")

value_entered = float(value_entered)
value_squared = value_entered**2
print ("The value squared= ", round(value_squared,2))

