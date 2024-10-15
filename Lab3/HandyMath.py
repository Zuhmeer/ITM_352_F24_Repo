# Library of handy reuseable math functions. 

# Give it two numbers and it returns the midpoint. 
def midpoint(num1, num2):
    return ((num1 + num2)/2)

number1 = input("Enter first value")
number2 = float(input("Enter second value"))
number1 = float(number1)
mid = midpoint(number1, number2)
print("The midpoint is: ", mid)

# Return the squareroot of any number
def squareroot(num1):
    return(num1**0.5)
    
number1 = float(input("Enter Value"))
sqrt = squareroot(number1)
print("The squareroot is: ", sqrt)

# Use the exponent function for any number
def exponent(num3, num4): 
    return(num3** num4)

number3 = float(input("Enter Value Here"))
number4 = float(input("Enter Exponent Here"))
expo =  exponent(number3, number4)
print("The number " , number3, "to the power of, " , number4, " equals, ", expo)

# Use the maximum value function for 2 numbers 
def maxNum(num5, num6):
    return(max(num5, num6))

number5 = float(input("Enter Value"))
number6 = float(input("Enter Second Value"))
max1 = maxNum(number5, number6)
print("The maximum value is: " , max1)

# Use the minimum value function for 2 numbers 
def minNum(num7, num8):
    return(min(num7, num8))

number7 = float(input("Enter Value"))
number8 = float(input("Enter Second Value"))
min1 = minNum(number7, number8)
print("The minimum value is: " , min1)

