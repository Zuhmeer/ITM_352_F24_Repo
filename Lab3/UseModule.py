# Program to test the use of the handy math library.
import HandyMath as HM

number1 = input("Enter first value")
number2 = float(input("Enter second value"))
number1 = float(number1)



mid = HM.midpoint(number1, number2)
print("The midpoint is: ", mid)

sqrt = HM.squareroot(number1)
print("The squareroot is: ", sqrt)

expo = HM.exponent(number1, number2)
print("The number " , number1, "to the power of, " , number2, " equals, ", expo) 

max = HM.maxNum(number1, number2)
print("The maximum value is: " , max)

min = HM.minNum(number1, number2)
print("The minimum value is: ", min)

