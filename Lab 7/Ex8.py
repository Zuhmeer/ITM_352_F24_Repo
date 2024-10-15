my_tuple = ("hello", 10, "goodbye", 3, "goodnight", 5)

user_input = input("Enter a string to add to the tuple: ")

try:
    my_tuple.append(user_input)
except AttributeError:
    my_list = list(my_tuple)
    my_list.append(user_input)
    my_tuple = tuple(my_list)

print("Updated tuple:", my_tuple)
