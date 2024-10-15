# read from the survey _1000.csv file and calculate the 
# the acerage, maximum, and minimum values for the real inc field
# if the numbers are greater than 0, report the numbers of non-zero values.

import csv

line_number = 0 
number_values = 0
total_RealInc = 0
max_RealInc = 0
min_RealInc = 999999999999999 

with open("/Users/javoningram/Downloads/survey_1000.csv", "r") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=",")
    
    for line in csv_reader:
        if (line_number > 0):
            RealInc = float(line[5456])
            if (RealInc > 0):
                number_values += 1
                total_RealInc += RealInc
                if (RealInc > max_RealInc):
                    max_RealInc = RealInc
                if (RealInc < min_RealInc):
                    min_RealInc = RealInc
        line_number += 1
print(f"Number of non-zero values: {number_values}")
print(f"Average RealInc: ${round(total_RealInc / number_values,2)})")
                





