#Eli
#Fermin
import tkinter as tk
from tkinter import scrolledtext
        
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

#dictionary for what we want to keep track of
airport_stats = {
    "ATL": {"total": 0, "cancelled": 0, "dep_delay_total": 0, "arr_delays": [], "late": 0, "early": 0},
    "CLT": {"total": 0, "cancelled": 0, "dep_delay_total": 0, "arr_delays": [], "late": 0, "early": 0}
}

for line in f:
    line = line.strip()
    fields = line.split(",")

    if len(fields) != 9:
        invalid_rows += 1 
        errfile.write(f"Line {line_number}: Wrong number of fields\n")
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
            errfile.write(f"Line {line_number}: Day does not exist in month \n")
            errfile.write("Raw data: " + line + '\n\n')
            line_number += 1
            continue
    #Makes sure  the month has right day
    elif month in [4,6,9,11]:
        if day < 1 or day > 30:
            invalid_rows += 1
            errfile.write(f"Line {line_number}: Day does not exist in month\n")
            errfile.write("Raw data: " + line + '\n\n')
            line_number += 1
            continue
    else:
        if day < 1 or day > 31:
            invalid_rows += 1
            errfile.write(f"Line {line_number}: Day does not exist in month\n")
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
    origin = fields[4].strip()
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
        errfile.write(f"Line {line_number}: Wrong destination\n")
        errfile.write("Raw data: " + line + '\n\n')
        line_number += 1
        continue
    
    try:
        dep_delay = to_int_or_none(fields[6])
        arr_delay = to_int_or_none(fields[7])
        cancelled = int(fields[8])
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
    
    # Logic for valid rows
    airport_stats[origin]["total"] += 1
    if cancelled == 1:
        airport_stats[origin]["cancelled"] += 1
    else:
        # Only count delays for non-cancelled flights
        if dep_delay is not None:
            airport_stats[origin]["dep_delay_total"] += dep_delay
        if arr_delay is not None:
            airport_stats[origin]["arr_delays"].append(arr_delay)

    valid_rows += 1
    line_number += 1

f.close()
errfile.close()

# --- Calculate Best/Worst Airports ---
averages = {}
for code in ["ATL", "CLT"]:
    delays = airport_stats[code]["arr_delays"]
    if delays:
        averages[code] = sum(delays) / len(delays)

best_dest = "N/A"
worst_dest = "N/A"
if len(averages) == 2:
    best_dest = min(averages, key=averages.get)
    worst_dest = max(averages, key=averages.get)
elif len(averages) == 1:
    best_dest = list(averages.keys())[0]

# -- Format the Final text Output --
output_text = "AIRPORT\n"
output_text += "---------\n"

# Add stats for each airport
for code in ["ATL", "CLT"]:
    output_text += f"{code}\n"
    output_text += f"Total flights: {airport_stats[code]['total']}\n"
    output_text += f"Cancelled Flights: {airport_stats[code]['cancelled']}\n"
    output_text += f"total dep_delay: {airport_stats[code]['dep_delay_total']}\n\n"

# Add the final comparison section
output_text += "percent each destination arrival delay: \n"
for code in ["ATL", "CLT"]: # Fixed "ALT" typo to "ATL"
    if code in averages:
        output_text += f"{code}: {averages[code]:.2f}%\n"

output_text += f"\nBest Destination: {best_dest}\n"
output_text += f"Worst Destination: {worst_dest}\n"

# -- GUI --
def launch_gui(content):
    root = tk.Tk()
    root.title("Airport Data Results")
    root.geometry("400x520")

    text_area = scrolledtext.ScrolledText(root, font=("Courier", 11), bg="black")
    text_area.pack(expand=True, fill='both', padx=20, pady=20)
    
    text_area.insert(tk.INSERT, content)
    text_area.configure(state='disabled')
    
    root.mainloop()

launch_gui(output_text)