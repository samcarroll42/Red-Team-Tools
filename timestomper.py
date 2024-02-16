# timestomper.py
# A red team tool that modifies various times and dates in a file's metadata to ward off forensics and blue teams.
# For Windows files, this script changes the create, modify, and access dates.
# For Linux files, this script changes the access and modify dates.
#
# This script was written as a red team tool for the first competition in CSEC 473 - Cyber Defense Techniques.
#
# Prerequisites - Python module win32_setctime (pip install win32_setctime)
#
# Author - Sam Carroll
# Date: February 16, 2024

# TO DO:
    # Add millisecond representation (%f)
# FUTURE ADDITIONS
    # Time zone handling
    # Handling for Mac files

from win32_setctime import setctime
from datetime import datetime
import os

# Clear screen
os.system("cls" if os.name == "nt" else "clear")

# Converts a string representation of a date to epoch time.
# Parameters:
#     string - a string representation of a date.
def string_to_epoch(string):
    date_time = datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
    epoch_time = date_time.timestamp()

    return epoch_time

# Ensures that the format of an inputted string is correct.
# Parameters:
#     string - a string representation of a date.
def test_format(string):
    try:    
        date_time = datetime.strptime(string, "%Y-%m-%d %H:%M:%S")     
    except ValueError:
        return False

    return True 

def main():
    while 1 == 1:
        # Takes input for the file path.
        print("Dates must be in Python datetime format (yyyy-mm-dd hh:mm:ss) and in UTC.")
        file_path = input("Enter the full path of a file: ")

        # Checks if the file path exists.
        # If not, restarts prompt.
        if not os.path.exists(file_path):
            print("File not found.")
            continue

        # Checks if the script is being run on a Windows machine.
        if os.name == "nt":
            # Workflow for Windows files.

            # Takes user input for a create date and checks for proper formatting.
            create_date = input("Enter a wanted creation date: ")
            if not test_format(create_date):
                print("Create date format incorrect.")
                continue

            # Takes user input for a modify date and checks for proper formatting.
            modify_date = input("Enter a wanted modify date: ")
            if not test_format(modify_date):
                print("Modify date format incorrect.")
                continue

            # Takes user input for an access date and checks for proper formatting.
            access_date = input("Enter a wanted access date: ")
            if not test_format(access_date):
                print("Access date format incorrect.")
                continue

            # Converts string representations of dates to epoch time.
            epoch_create_date = string_to_epoch(create_date)
            epoch_modify_date = string_to_epoch(modify_date)
            epoch_access_date = string_to_epoch(access_date)

            # Sets access and modify dates.
            os.utime(file_path, (epoch_access_date, epoch_modify_date))

            # Sets create date.
            setctime(file_path, epoch_create_date)
        else:
            # Workflow for other OS's files (specifically written with Linux in mind).

            # Takes user input for an access date and checks for proper formatting.
            access_date = input("Enter a wanted access date: ")
            if not test_format(access_date):
                print("Access date format incorrect.")
                continue

            # Takes user input for a modify date and checks for proper formatting.
            modify_date = input("Enter a wanted modify date: ")
            if not test_format(modify_date):
                print("Modify date format incorrect.")
                continue

            # Takes user input for a change date and checks for proper formatting.
            #change_date = input("Enter a wanted change date: ")
            #if not test_format(change_date):
            #    print("Change date format incorrect.")
            #    continue

            # Converts string representations of dates to epoch time.
            epoch_access_date = string_to_epoch(access_date)
            epoch_modify_date = string_to_epoch(modify_date)
            #epoch_change_date = string_to_epoch(change_date)

            # Sets access and modify dates.
            os.utime(file_path, (epoch_access_date, epoch_modify_date))

        # Breaks the loop if files were modified.
        break

main()