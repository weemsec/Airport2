#Eli
#Fermin

print("this is the main")

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


    #OP_UNIQUE_CARRIER Validation
    carrier = fields[3].strip()
    if len(carrier) !=2:
        invalid_rows = invalid_rows + 1
        print("Invalid Carrier")
        continue

    # Origin must be CLT or ATL
    if origin not in ["CLT","ATL"]:
        invalid_rows += 1
        print("Invalid origin")
        continue

    #If the code reaches here, the row has passed the first 4 steps!
    valid_rows += 1

