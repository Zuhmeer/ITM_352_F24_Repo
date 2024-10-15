#with open ("Names.txt", mode="r") as textFile:
    #line = textFile.readline()
    #count = 0
    
    #while line: 
   #     print(line)
  #      count += 1
 #       line = textFile.readline()

#print(f"There are {count} names in the file")


import os

file_path = "Names.txt"

if os.path.exists(file_path) and os.access(file_path, os.R_OK):
    # Append "Port, Dan" to the file
    with open(file_path, mode="a") as textFile:
        textFile.write("\nPort, Dan")

    with open(file_path, mode="r") as textFile:
        Namelist = textFile.read()
        print(Namelist)

    Seperatedlist = Namelist.split("\n")
    count = len(Seperatedlist)
    print(f"There are now {count} names in the file")
else:
    print(f"The file '{file_path}' does not exist or is not readable.")


