
 # Tuple containing mixed elements
my_tuple = ("hello", 10, "goodbye", 3, "goodnight", 5)

# Variable to count the number of strings
string_count = 0

# Iterate through each element of the tuple
for element in my_tuple:
    # Check if the element is a string
    if isinstance(element, str):
        string_count += 1

# Print the result
print(f"There are {string_count} strings in the tuple.")
