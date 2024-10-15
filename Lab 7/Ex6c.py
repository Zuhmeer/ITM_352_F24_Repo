my_tuple = ("hello", 10, "goodbye", 3, "goodnight", 5)

user_input = input("Enter a string to add to the tuple: ")


if isinstance(my_tuple, tuple):
    my_tuple.append(user_input)  

print("Original tuple:", my_tuple)

