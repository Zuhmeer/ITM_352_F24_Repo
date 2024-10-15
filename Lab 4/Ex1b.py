# Ask the user to enter their first name, middle initial and 
# last name. Concatenate them together with spaaces in between 
# and print out the result. 

First = input("Please enter your first name: ")
MiddleInitial = input("Please enter your middle initial: ")
Last = input("Please enter your last name: ")

FullName = First + " " + MiddleInitial + " " + Last
print("your full name is ", FullName)

FullName = First + " " + MiddleInitial + " " + Last
print("Your full name is ", FullName)
print(f"Your full name is {First} {MiddleInitial} {Last} ")
print("Your first name is %s %s %s" % (First, MiddleInitial, Last) )
print("Your first name is {0}{1}{2} ".format(First, MiddleInitial, Last)) 

FullNamestr = [First, MiddleInitial, Last]
str = " ".join(FullNamestr)
print(f"Your full name is {str} ")

FullNamestr = (First, MiddleInitial, Last) 
print("Your full name is {0} ".format(FullNamestr)) 
