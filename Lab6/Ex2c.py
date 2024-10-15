# More clear and flexible code 

myList = [
[[1], [2], [3], [4]], 
[[1], [2], [3], [4], [5], [6], [7], [8]], 
[[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]]
]

def check_list_length(myList, index):
    if len(myList[index]) < 5:
        print("less than 5 elements")
        return len(myList[index])
    elif 5 <= len(myList[index]) <= 10:
        print("Between 5 and 10 elements")
        return len(myList[index])
    else:
        print("Greater than 11 elements")
        return len(myList[index])

print(check_list_length(myList, 2))

