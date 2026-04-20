#Eli
#Fermin

#takes value turns to int or no vlaue if blank
def to_int_or_none ():
    value = value.strip
    if value == "":
        return None
    return int(value)


filename = input("Enter the filename: ")
f = open(filename, "r")
valid_rows = 0
invalid_rows = 0

for line in f:
    line = line.strip()
    fields = line.split(",")

    if len(fields) != 9:
        invalid_rows = invalid_rows + 1 
        print("Invalid row: ", line)
        continue
    
    try:
        year = int(fields[0])
    except:
        invalid_rows = invalid_rows + 1 
        print("Invalid row: ", line)
        continue

    if year != 2024:
        invalid_rows = invalid_rows + 1
        print("Invalid row: ", line)
        continue
    

    try: 
        month = int(fields[1])
        day = int(fields[2])
    except:
        invalid_rows = invalid_rows + 1
        print("Invalid row: ", line)
        continue
    #checks to see if its a real number for the month
    if month < 1 or month > 12:
        print("Invalid moth")
    #check for the right days in febuary
    if month == 2:
        if day > 29 or day < 0:
            print("Invalid days ")
            continue
    #Makes sure  the month has right day
    elif month in [4,6,9,11]:
        if day != 30:
            print("Invalid days")
            continue
    else:
        if day != 31:
            print("Invalid days")
            continue


    #OP_UNIQUE_CARRIER Validation
    carrier = fields[3].strip()
    if len(carrier) !=2:
        invalid_rows = invalid_rows + 1
        print("Invalid Carrier")
        continue

    # Origin must be CLT or ATL
    origin = fields[4]
    if origin not in ["CLT","ATL"]:
        invalid_rows += 1
        print("Invalid origin")
        continue

    #If the code reaches here, the row has passed the first 4 steps!
    valid_rows += 1

    #Destination
    destination = fields[3].strip()
    if len(destination) != 3:
        invalid_rows += 1
        print("Invalid destination")
        continue
    
    try:
        dep_delay = to_int_or_none(fields[6])
        arr_delay = to_int_or_none(fields[7])
    except:
        invalid_rows += 1
        print("Invalid number")
        continue

    #changing from string to int
    try:
        cancelled = int(fields[8])
    except:
        invalid_rows += 1
        print("Invalid number")
        continue

    #

