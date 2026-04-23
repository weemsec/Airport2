#Eli
#Fermin
        
#takes value turns to int or no vlaue if blank
def to_int_or_none(value):
    value = value.strip()
    if value == "":
        return None
    return int(value)


filename = input("Enter the filename: ")
f = open(filename, "r")

errfile = open("errors_log.txt", "w")
valid_rows = 0
invalid_rows = 0
f.readline()
line_number = 2

for line in f:
    line = line.strip()
    fields = line.split(",")

    if len(fields) != 9:
        invalid_rows += 1 
        errfile.write(f"Line {line_number}: Wrong nymber of fields\n")
        errfile.write("Raw data: " + line + '\n\n')
        line_number += 1
        continue
    
    try:
        year = int(fields[0])
    except:
        invalid_rows += 1 
        errfile.write(f"Line {line_number}: Not a year number \n")
        errfile.write("Raw data: " + line + '\n\n')
        line_number += 1
        continue

    if year != 2024:
        invalid_rows += 1
        errfile.write(f"Line {line_number}: Not in year 2024 \n")
        errfile.write("Raw data: " + line + '\n\n')
        line_number += 1
        continue
    

    try: 
        month = int(fields[1])
        day = int(fields[2])
    except:
        invalid_rows += 1
        errfile.write(f"Line {line_number}: Not a Number \n")
        errfile.write("Raw data: " + line + '\n\n')
        line_number += 1
        continue
    #checks to see if its a real number for the month
    if month < 1 or month > 12:
        invalid_rows += 1
        errfile.write(f"Line {line_number}: Not a real Month\n")
        errfile.write("Raw data: " + line + '\n\n')
        line_number += 1
        continue
    #check for the right days in febuary
    if month == 2:
        if day < 1 or day > 29:
            invalid_rows += 1
            errfile.write(f"Line {line_number}: Day does not exsit in month \n")
            errfile.write("Raw data: " + line + '\n\n')
            line_number += 1
            continue
    #Makes sure  the month has right day
    elif month in [4,6,9,11]:
        if day < 1 or day > 30:
            invalid_rows += 1
            errfile.write(f"Line {line_number}: Day does not exsit in month\n")
            errfile.write("Raw data: " + line + '\n\n')
            line_number += 1
            continue
    else:
        if day < 1 or day > 31:
            invalid_rows += 1
            errfile.write(f"Line {line_number}: Day does not exsit in month\n")
            errfile.write("Raw data: " + line + '\n\n')
            line_number += 1
            continue


    #OP_UNIQUE_CARRIER Validation
    carrier = fields[3].strip()
    if len(carrier) != 2:
        invalid_rows += 1
        errfile.write(f"Line {line_number}: Wrong carrier\n")
        errfile.write("Raw data: " + line + '\n\n')
        line_number += 1
        continue

    # Origin must be CLT or ATL
    origin = fields[4]
    if origin not in ["CLT","ATL"]:
        invalid_rows += 1
        errfile.write(f"Line {line_number}: Origin is not CLT or ATL\n")
        errfile.write("Raw data: " + line + '\n\n')
        line_number += 1
        continue

    #If the code reaches here, the row has passed the first 4 steps!

    #Destination
    destination = fields[5].strip()
    if len(destination) != 3:
        invalid_rows += 1
        errfile.write(f"Line {line_number}: Worng destination\n")
        errfile.write("Raw data: " + line + '\n\n')
        line_number += 1
        continue
    
    try:
        dep_delay = to_int_or_none(fields[6])
        arr_delay = to_int_or_none(fields[7])
    except:
        invalid_rows += 1
        errfile.write(f"Line {line_number}: Delay value is not a number\n")
        errfile.write("Raw data: " + line + '\n\n')
        line_number += 1
        continue

    #Cancelled changing from string to int 
    try:
        cancelled = int(fields[8])
    except:
        invalid_rows += 1
        errfile.write(f"Line {line_number}: Cancelled is not a number or missing data\n")
        errfile.write("Raw data: " + line + '\n\n')
        line_number += 1
        continue
    #checks if 1 or 0 
    if cancelled not in [0, 1]:
        invalid_rows += 1
        errfile.write(f"Line {line_number}: Cancelled is not 0 or 1\n")
        errfile.write("Raw data: " + line + '\n\n')
        line_number += 1
        continue
    # cancelled flights may not have delay values
    if cancelled == 1:
        if dep_delay is not None or arr_delay is not None:
            invalid_rows += 1
            errfile.write(f"Line {line_number}: Is cancelled but contains a delay vlaue\n")
            errfile.write("Raw data: " + line + '\n\n')
            line_number +=1
            continue

    valid_rows += 1
    line_number += 1

f.close()
errfile.close()

