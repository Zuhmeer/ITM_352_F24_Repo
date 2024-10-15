# Determine a movie price. The rules are:
age = int(input("Enter age: "))
day = input("Enter the current day of the week: ")
matinee = input("Attending a matinee?: ")

# The normal price is $14
PriceList = [14]

# If someone is 65 or older, they pay $8.
if age >= 65:
    PriceList.append(8)

# If it is Tuesday, the price is $10.
if day.capitalize() == "Tuesday": 
    PriceList.append(10)

# If it is a matinee, the price is $5 for seniors and $8 otherwise
if matinee.capitalize() == "Yes" and age >= 65: 
    PriceList.append(5)
elif matinee.capitalize() == "Yes":
    PriceList.append(8)

# Print out the values of the variables and the price. The price should always be the lowest one that applies. 
PriceList.sort()
print(PriceList)
print(f"The price is ${PriceList[0]}")

