# Create a Python program that will iterate through the list sample_fares = [8.60, 5.75, 13.25, 21.21] and 
# print a message “This fare is high!” 
# if the fare is greater than 12 dollars and “This fare is low” otherwise.

#all the fares are low!
Samplefares = [5, 6, 7, 8]
def function(e):
    for i in e: 
        if i >= 12:
            print("This fare is high!")
        else:
            print("This fare is low!")

print(function(Samplefares))


