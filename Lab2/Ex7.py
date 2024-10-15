# Ask the user to input a temperature in degrees Farenheit. 
# Convert that temperature to Celsius and output it. 

degreesF = input("Enter a temperature in Farenheit: ") 

degreesC = (degreesF - 32) * (5/9) 

print("This converts to ", degreesC, "Celcius") 
