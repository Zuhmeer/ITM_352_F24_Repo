# Create a if statement that will output whether or not it is a leap year or not a leap year

leapyear = int(input("Enter a year: "))


if leapyear % 4 == 0 and leapyear % 100 !=0 or leapyear % 400 ==0: 
    print(f"{leapyear} is a leapyear.")
else:
    print(f" {leapyear} is not a leapyear.")



