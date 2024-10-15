# Tuples for years and respondents
years_tuple = (1980, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989)
respondents_tuple = (17, 35, 26, 26, 25, 27, 35, 21, 19)

# Lists to store the values
years_list = []
respondents_list = []

# Iterate through the tuples and append values to the lists
for year in years_tuple:
    years_list.append(year)

for respondent in respondents_tuple:
    respondents_list.append(respondent)

# Create a dictionary to store the lists
data_dict = {
    "years": years_list,
    "respondents": respondents_list
}

# Print the resulting dictionary
print(data_dict)
