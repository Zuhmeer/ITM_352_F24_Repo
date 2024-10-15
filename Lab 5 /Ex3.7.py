# Create a list of trip durations and fares

trip_Duration = [1.1, 0.8, 2.5, 2.6]
trip_Fares  = ("$6.25", "$5.25", "$10.50", "$8.05")

tripDict = {"miles": trip_Duration, 
            "fares": trip_Fares}
print(tripDict["miles"][2:3], tripDict["fares"][2:3])


# Create a new dictionary by zipping together the duration list and the list tuple
newDict = dict(zip(trip_Duration, trip_Fares))
print("New dict=", newDict)
print(f"Trip duration={trip_Duration[2]}  cost={newDict[trip_Duration[2]]}")


# Defining the list of trips with 'duration' and 'fare'
trips = [
    {'duration': 1.1,  'fare': 6.25}, 
    {'duration': 0.8,  'fare': 5.25},
    {'duration': 2.5,  'fare': 10.50},
    {'duration': 2.6,  'fare': 8.05},
]

