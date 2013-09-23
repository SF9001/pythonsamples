'''
 PYTHON CODE TO FLATTEN AN LDAP STYLE FILE TO CSV FORMAT
'''

import sys
import time


def writeOut(outFile, dictionary, key, comma, isDate):
    '''
    Writes entries from a dictionary to the output file and adds a comma after the entry if required.
    '''

    if key in dictionary:
        if isDate:
            outFile.write(formatDate(dictionary[key]))
        else:
            outFile.write(dictionary[key])

    if comma:
        outFile.write(",")


def flattenOutput(inputFile, outputFile):
    '''
    Reads an LDAP style file and flattend the output into CSV style
    '''
    with open(outputFile, "w") as fout:
        fout.write("UserName,Group1,Group2,Group3,Group4,UserName2,AgencyCode,FirstName,LastName,LastLogin\n")

        with open(inputFile, "r") as fin:

            # Create an empty dictionary object
            ldapDict = {}

            for line in fin:
                #If the line is empty then we need to output the stuff we've built up in the dictionary.
                if line.__len__() == 1:
                    columnOrder = (
                        ("dn", True, False),
                        ("uid", True, False),
                        ("agencyCode", True, False),
                        ("givenName", True, False),
                        ("lastName", True, False),
                        ("lastLogin", False, True))
                    for detail in columnOrder:
                        writeOut(fout, ldapDict, detail[0], detail[1], detail[2])
                    fout.write("\n")
                    ldapDict = {}
                else:
                    # Remove the carriage return from the line and split it at the FIRST colon mark and add these
                    # key/value pairs to the dictionary
                    cleaned = line.rstrip().split(":", 1)
                    key = cleaned[0]
                    value = cleaned[1]
                    ldapDict.update({key: value})


def formatDate(aDate):
    '''
    Formats a date supplied in the format dd-MM-YYYY h:mm:ss to the format YYYY-MM-dd hh:mm:ss
    e.g.: 11-May-2010 12:00:27 --> "2010-05-11 12:00:27"
    '''
    try:
        x = time.strptime(aDate.strip(), "%d-%b-%Y %H:%M:%S")
        return time.strftime("%Y-%m-%d %H:%M:%S", x)
    except:
        return ""


print("Please wait...")
flattenOutput("c:/temp/data.txt", "c:/temp/dataout.csv")
print("Done")
