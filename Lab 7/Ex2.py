# Create Python code that uses a Python for-statement 
# to create a list of elements that 
# are the even numbers between 1 and 50

number = range(0, 51)

for i in number: 
    if i % 2 == 0: 
        continue
    print(i)
