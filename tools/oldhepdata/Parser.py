"""
    Parser.py
    Description: This script, along with header.py, is intended for parsing of data files as uploaded to Drupal
                on behalf of the STAR collaboration at Brookhaven National Laboratory. The data is converted into
                the HepData input format in preparation for upload to HepData.net
    Created on Thurs July 21 2016
    @author: Nick Luttrell (Rice University)
"""

import header
import sys

# Parse each of the metadata fields (where applicable) and send to initFields. Then format and output the actual data.
def parseDataList(dataList, cmdlist, cmd_index, fignum, output):
    
    description = ""
    reaction = "AU AU --> X"    # ***CAN BE CHANGED TO APPLY REACTION KEY TO EVERY PLOT***
    sqrt_s = ""
    Quals = []
    
    for index, x in enumerate(dataList):
        if ("description" in x[0]) or ("Description" in x[0]):
            for word in x[1:]:
                description = description + word + " "

        elif ("reaction" in x[0]) or ("Reaction" in x[0]):
            for word in x[1:]:
                reaction = reaction + word + " "

        elif ("Sqrt" in x[0]) or ("sqrt" in x[0]) or ("SQRT" in x[0]):
            for word in x[1:]:
                try:
                    float(word)
                    sqrt_s = word
                    break
                except ValueError:
                    continue

        elif ("qual" in x[0]) or ("Qual" in x[0]) or ("QUAL" in x[0]):
            qualifier = ""
            for word in x[1:]:
                qualifier = qualifier + word + " "
            Quals.append(qualifier)
                
        elif ("data" in x[0]) or ("Data" in x[0]) or ("DATA" in x[0]):
            dex = index+1
            header.initFields(fignum, description, reaction, sqrt_s, Quals, output)
            break
        else:
            continue
    
    header.writeColumnHeaders(dataList[dex], output) # Write the column headers

    numcol = len(dataList[dex + 1]) # Actual data values follow immediately after x and yheaders (the place of 'dex')
    print ("There are {0} columns\n".format(numcol))
    try:
        data_format = header.userFormat(cmdlist[cmd_index])
    except IndexError:
        print ("Index Error from cmdlist!")
        output.close()
        sys.exit()

    columns = "x"
    for x in data_format[0:len(data_format) - 2]:
        if x == ";":
            columns = columns + ": y"
    output.write( "*data: {0}\n".format(columns) )

    for entry in dataList[dex+1:len(dataList)-1]:
        header.writeData(entry, numcol, data_format, output)

    output.write( "*dataend: \n\n" )



#
# Begin Main()
#

# Define any values that remain unchanged throughout the paper (usually the reaction)
fignum = ""
delimiter = "Figure"

# Open data, output, and format files

dataList = []
datafile = open('test', 'r')

output = open("output.txt", "w")
cmdfile = open('format', 'r')

cmd_index = 0
cmdlist = []
for line in cmdfile:
    cmdlist.append(line)

for line in datafile:
    nextline = line.strip() # Remove excess white space.
    nextline = nextline.split()
    if not line.strip():
        continue
    elif delimiter not in nextline[0]:
        dataList.append(nextline)
    elif (delimiter in nextline[0]):
        if dataList:
            print (fignum)
            parseDataList(dataList, cmdlist, cmd_index, fignum, output)
            cmd_index += 1
            dataList = []

        try:
            fignum = delimiter + " " + nextline[1]
        except IndexError:
            fignum = delimiter
        print (cmd_index)

else:
    if dataList:
        print (fignum)
        parseDataList(dataList, cmdlist, cmd_index, fignum, output)


output.write( "*E:" )
print ("Parsing complete. Exiting...")

datafile.close()
cmdfile.close()
output.close()


# END OF PARSER.PY