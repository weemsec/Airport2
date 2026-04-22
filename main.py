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

errfile = open("errors_log.txt", "w")
valid_rows = 0
invalid_rows = 0
f.readline()
for line in f:
    line = line.strip()
    fields = line.split(",")

    if len(fields) != 9:
        invalid_rows = invalid_rows + 1 
        errfile.write("Invalid row: Wrong nymber of fields\n")
        errfile.write("Raw data: " + line + '\n\n')
        continue
    
    try:
        year = int(fields[0])
    except:
        invalid_rows = invalid_rows + 1 
        errfile.write("Invalid row: Not a year number \n")
        errfile.write("Raw data: " + line + '\n')
        continue

    if year != 2024:
        invalid_rows = invalid_rows + 1
        errfile.write("Invalid row: Not in year 2024 \n")
        errfile.write("Raw data: " + line + '\n')
        continue
    

    try: 
        month = int(fields[1])
        day = int(fields[2])
    except:
        invalid_rows = invalid_rows + 1
        errfile.write("Invalid row: Not a Number \n")
        errfile.write("Raw data: " + line + '\n')
        continue
    #checks to see if its a real number for the month
    if month < 1 or month > 12:
        errfile.write("Invalid row: Not a real Month\n")
        errfile.write("Raw data: " + line + '\n')
        continue
    #check for the right days in febuary
    if month == 2:
        if day > 29 or day < 0:
            errfile.write("Invalid row: Day does not exsit in month \n")
            errfile.write("Raw data: " + line + '\n')
            continue
    #Makes sure  the month has right day
    elif month in [4,6,9,11]:
        if day != 30:
            errfile.write("Invalid row: Day does not exsit in month\n")
            errfile.write("Raw data: " + line + '\n')
            continue
    else:
        if day != 31:
            errfile.write("Invalid row: Day does not exsit in month\n")
            errfile.write("Raw data: " + line + '\n')
            continue


    #OP_UNIQUE_CARRIER Validation
    carrier = fields[3].strip()
    if len(carrier) != 2:
        invalid_rows = invalid_rows + 1
        errfile.write("Invalid row: Wrong carrier\n")
        errfile.write("Raw data: " + line + '\n')
        continue

    # Origin must be CLT or ATL
    origin = fields[4]
    if origin not in ["CLT","ATL"]:
        invalid_rows += 1
        errfile.write("Invalid row: Origin is not CLT or ATL\n")
        errfile.write("Raw data: " + line + '\n')
        continue

    #If the code reaches here, the row has passed the first 4 steps!

    #Destination
    destination = fields[5].strip()
    if len(destination) != 3:
        invalid_rows += 1
        errfile.write("Invalid row: Worng destination\n")
        errfile.write("Raw data: " + line + '\n')
        continue
    
    try:
        dep_delay = to_int_or_none(fields[6])
        arr_delay = to_int_or_none(fields[7])
    except:
        invalid_rows += 1
        errfile.write("Invalid row: \n")
        errfile.write("Raw data: " + line + '\n')
        continue

    #Cancelled changing from string to int 
    try:
        cancelled = int(fields[8])
    except:
        invalid_rows += 1
        errfile.write("Invalid row: \n")
        errfile.write("Raw data: " + line + '\n')
        continue
    #checks if 1 or 0 
    if cancelled > 1 or cancelled < 0:
        invalid_rows += 1
        errfile.write("Invalid row: \n")
        errfile.write("Raw data: " + line + '\n')
        continue
    # cancelled flights may not have delay values
    if cancelled == 1:
        if dep_delay is not None or arr_delay is not None:
            invalid_rows += 1
            print("Invlaid number")
    else:
        if dep_delay is not None and arr_delay is None:
            invalid_rows += 1
            print("Invalid number")

    valid_rows += 1

f.close()
errfile.close()

