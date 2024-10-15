# Ask the user to input a temperature in degrees Farenheit. 
# Convert that temperature to Celsius and output it. 

# Function to convert degrees F to C
def FtoC(temperatureF):
    degreesC = (float(degreesF) - 32) * (5/9)
    return(degreesC)

degreesF = input("Enter a temperature in Farenheit: ") 

print("This converts to ", FtoC(degreesF), "Celcius") 
