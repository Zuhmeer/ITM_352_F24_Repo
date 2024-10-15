# Tuples for years and respondents
years_tuple = (1980, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989)
respondents_tuple = (17, 35, 26, 26, 25, 27, 35, 21, 19)

# Convert tuples to lists directly
years_list = list(years_tuple)
respondents_list = list(respondents_tuple)

# Create a dictionary to store the lists
data_dict = {
    "years": years_list,
    "respondents": respondents_list
}

# Print the resulting dictionary
print(data_dict)
