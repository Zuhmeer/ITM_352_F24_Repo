#with open ("Names.txt", mode="r") as textFile:
 #   Namelist = textFile.read()
  #  print(type(textFile))
   # print(Namelist)


#Seperatedlist = Namelist.split("\n")
#print(Seperatedlist) 
#count = len(Seperatedlist)
#print(f"There are {count} names in the file")


import os

file_path = "Names.txt"

if os.path.exists(file_path) and os.access(file_path, os.R_OK):
    with open(file_path, mode="r") as textFile:
        Namelist = textFile.read()
        print(type(textFile))
        print(Namelist)

    Seperatedlist = Namelist.split("\n")
    print(Seperatedlist)
    count = len(Seperatedlist)
    print(f"There are {count} names in the file")
else:
    print(f"The file '{file_path}' does not exist or is not readable.")

