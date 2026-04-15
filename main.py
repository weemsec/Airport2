print("this is the main")
print("HI")

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