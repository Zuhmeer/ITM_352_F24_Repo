# create a Dictionary with ID values as the keys and survey
# responses as the values using zip()

responses = [5, 7, 3, 8]
respondentIDs = (1012, 1035, 1021, 1053)
zipData = dict(zip(respondentIDs, responses))
print(zipData)

