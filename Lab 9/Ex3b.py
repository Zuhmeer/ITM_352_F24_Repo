import csv

line_number = 0 
total_trips_miles = 0 
number_trip_miles = 0
max_trip_miles = 0
total_trip_fare = 0
trip_fares = 0
number_fares = 0

with open("/Users/javoningram/Downloads/taxi_1000.csv", "r") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=",")

    for line in csv_reader:
        if(line_number > 0):
            trip_fares = float(line[10])
            if trip_fares > 10:  # Only consider fares greater than $10
                trip_miles = float(line[5])
                total_trips_miles += trip_miles
                number_trip_miles += 1
                total_trip_fare += trip_fares
                number_fares += 1

                if trip_miles > max_trip_miles:
                    max_trip_miles = trip_miles
        line_number += 1

    if number_fares > 0:
        average_fares = total_trip_fare / number_fares
        print(f"Total Fares (greater than $10): ${round(total_trip_fare, 2)}")
        print(f"Average Cost (greater than $10): ${round(average_fares, 2)}")
        print(f"The longest trip (for fares greater than $10) was: {max_trip_miles} miles")
    else:
        print("No fares greater than $10 were found.")
