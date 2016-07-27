# STAR-HEPdata
STAR Published Data for HEPdata.net



# Notes on Parser.py and header.py
The python script Parser.py takes two input files and produces a single output file in the HepData input format. The first input file is the data file to be parsed, preferably in a simple .txt format. The second input file is a list of instructions created by the user to specify the structure format for the data in a given figure (i.e. if there were 3 figures in data.txt, then format.txt would have 3 lines of commands to be parsed. Specific instructions on making format.txt with proper syntax can be found in header.py
