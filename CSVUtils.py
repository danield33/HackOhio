import csv


def findCoordinates(roomNum):
    with open('bolzrooms.csv', mode='r') as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            if lines[0] == roomNum:
                return lines[1:]
