# Ask the user to enter an arbitrary sentence. Caluculate the length of that
# string and return that value. 

sentence = input("Enter a sentence: ") 

string_Length = len(sentence)
outputString = "You entered \"" + sentence + "\". It has length " + str(string_Length)

print("The length of your sentence is ", string_Length)
