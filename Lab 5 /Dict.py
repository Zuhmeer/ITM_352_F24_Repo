# print the dictionary 

capitals = {"Germany": "Berlin",
            "Canada": "Ottowa"
            "England"  "London"}

# print the dictionary
print(capitals)

print(capitals["Germany"])
print(capitals["England"])

del capitals("Germany")
print("after delete:", capitals)

capitals["Italy"] = "Rome"
capitals["Italy"] = "Naples"

print("After add: ", capitals)

print("Length of capitals=", len(capitals))

#capitals.clear()
#print("After clear: ", capitals)


print("Canada"in capitals)




