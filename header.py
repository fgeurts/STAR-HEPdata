# -*- coding: utf-8 -*-
"""
    Created on Thurs July 21 2016
    header.py
    Description: This is the header file that accompanies Parser.py
    @author: Nick Luttrell
    """

import sys
import re


# Initialize the meta-data fields for a figure.
def initFields(fignum, description, reaction, sqrt_s, Quals, output):
    output.write( "*dataset:\n" )
    output.write( "*location: {0}\n".format(fignum) )
    output.write( "*dscomment: {0}\n".format(description) )
    output.write( "*obskey: \n" )
    output.write( "*reackey: {0}\n".format(reaction) )
    if ("Au" in reaction) or ("AU" in reaction):
        output.write( "*qual: SQRT(S)/NUCLEON IN GEV:  {0}\n".format(sqrt_s) )
    else:
        output.write( "*qual: SQRT(S) IN GEV: {0}\n".format(sqrt_s) )
    for item in Quals:
        output.write( "*qual: .: {0}\n".format(item))



# Iterate through and properly parse the column headers
def writeColumnHeaders(Header_List, output):
    
    commaFlag = False
    xheader = ""
    yheader = ""
    
    for item in Header_List:
        if ',' in item:    # Check to see if the x and y headers are comma delimited
            commaFlag = True

    if (commaFlag == True):
        for index, item in enumerate(Header_List):
            if "," in item:
                xheader += item
                output.write( "*xheader: {0}\n".format(xheader.replace(',', '')))
                dex2 = index+1
                break
            else:
                xheader += item + " "

        output.write( "*yheader: " )
        for index, item in enumerate(Header_List[dex2:]):
            if "," in item:
                yheader += item
                if (index+dex2 < len(Header_List)-1): # Check to see if there are more yheaders yet to go
                    output.write( "{0}: ".format(yheader.replace(',', '')))
                    yheader = ""
            else:
                yheader += item + " "

        output.write( "{0}\n".format(yheader.replace(',', ''))) # Finish out
    
    else:
        output.write( "*xheader: {0}\n".format(Header_List[0]))
        output.write( "*yheader: " )
        for index, item in enumerate(Header_List[1:]):
            yheader = item
            if (index < len(Header_List)-2):
                output.write( "{0}: ".format(yheader.replace(',', '')))
            else:
                output.write( "{0}\n".format(yheader.replace(',', ''))) # Finish out


"""
    userFormat(Command) - This function takes a line from the input file cmdfile
    to arrange the columns for a given figure in the proper order and format. The relevant
    arguments are:
    'da#' where 'da' stands for 'data' and '#' should be replaced with an integer from 0 to infinity to specify the column
    'st#' where 'st' stands for 'statistical error' and '#' should be replaced with an integer from 0 to infinity to specify the column. Assumes symmetric error
    'sy##' where 'sy' stands for 'systematic error' and '##' should be replaced with numbers 0 through 9 to specify high and low error columns (in that order!). For double-digit columns, separate the numbers with a letter (i.e. sy13u14)
    '+# -#' in cases with asymmetrical high and low statistical errors
    Note that indexing of columns begins at 0, and in cases where high and low systematic errors are equal, simply repeat the column number.
    Each set of data with accompanying errors should be separated by a semicolon (spaces on both sides!) An ending semicolon should also appear.
    In cases where there is a systematic error but not statistical, insert 'na' where the stat. error would be. HepData will not parse if this is not included!
    An example line in format.txt might look like:  
    da0 ; da1 st2 sy43 ; da5 na sy66 ; da7 +8 -9 sy10u11 ;
    This creates a table in the form  x: y: y: y (i.e. three y-values with different asymmetric errors to be plotted against x)
    Note that the above line represents all the different complexities, and can be used as a guide.
"""

def userFormat(Command):
    
    try:
        data_format = Command
        print (data_format)
        return data_format
    
    except NameError:
        print ("IMPROPER INPUT! Enter a string with 'da0 ; da1 st2 sy43' or similar. See header file for instructions.")
        output.close()
        sys.exit()
    except SyntaxError:
        print ("IMPROPER SYNTAX! Who knows what you did. Just try again.")
        output.close()
        sys.exit()


# Use the command from format.txt to parse and write out the actual data.
def writeData(current_line, numcol, data_format, output):
    order = ""
    for item in data_format.split():
        try:
            if 'da' in item:
                col_index = re.search(r"\d+(\.\d+)?", item)
                col_index = col_index.group(0)
                try:
                    order += "%r" % float(current_line[int(col_index)].strip(','))
                except ValueError:
                    order += "%r" % current_line[int(col_index)].strip(',')
                except IndexError:
                    order += "-"
            elif 'na' in item:
                order += " +- 0"
            elif '+' in item:
                col_index = re.search(r"\d+(\.\d+)?", item)
                col_index = col_index.group(0)
                try:
                    order += " +%r" % float(current_line[int(col_index)].strip(','))
                except ValueError:
                    order += " +%r" % current_line[int(col_index)].strip(',')
                except IndexError:
                    order += " +0"
            elif '-' in item:
                col_index = re.search(r"\d+(\.\d+)?", item)
                col_index = col_index.group(0)
                try:
                    order += " -%r" % float(current_line[int(col_index)].strip(','))
                except ValueError:
                    order += " -%r" % current_line[int(col_index)].strip(',')
                except IndexError:
                    order += " -0"
            elif 'st' in item:
                col_index = re.search(r"\d+(\.\d+)?", item)
                col_index = col_index.group(0)
                try:
                    order += " +- %r" % float(current_line[int(col_index)].strip(','))
                except ValueError:
                    order += " +- %r" % current_line[int(col_index)].strip(',')
                except IndexError:
                    order += " +- 0"
            elif 'sy' in item:
                col_index = re.split('[a-z]+', item)
                col_index1 = col_index[1]
                try:
                    col_index2 = col_index[2]
                    try:
                        order += " (DSYS=+%r, -%r)" % ( float(current_line[int(col_index1)].strip(',')), float(current_line[int(col_index2)].strip(',')) )
                    except ValueError:
                        order += " (DSYS=+%r, -%r)" % ( current_line[int(col_index1)].strip(','), current_line[int(col_index2)].strip(',') )
                    except IndexError:
                        continue
                except IndexError:
                    try:
                        order += " (DSYS=+%r, -%r)" % ( float(current_line[int(item[2])].strip(',')), float(current_line[int(item[3])].strip(',')) )
                    except ValueError:
                        order += " (DSYS=+%r, -%r)" % ( current_line[int(item[2])].strip(','), current_line[int(item[3])].strip(',') )
                    except IndexError:
                        continue
        
            elif ';' in item:
                order += "; "
    
            else:
                print ("IMPROPER INPUT! Use a sequence like 'da0 ; da1 st2 sy43'")
                output.close()
                sys.exit()

        except IndexError:
            print ("IndexError in writeData! Bailing out..")
            order = ""
            output.close()
            sys.exit()

    order = order.replace('\'', "")     # Eliminate single quotes around non-numerical entries.
    output.write( order + "\n" )

# End of header