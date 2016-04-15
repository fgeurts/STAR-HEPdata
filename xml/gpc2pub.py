#!/usr/bin/python
### Python script to remove all non-public information from the STAR
### publication database, remove any paper entries that have not yet
### been published (i.e. no official pubID), and add three new
### (external) IDs to the paper record: arXiv, Inspire.net, and HEPdata.net
###
### Frank Geurts (Rice U.) April 15, 2016
### -----------------

#import the XML library, open file from disk, and parse into Element
import xml.etree.ElementTree as ET
tree = ET.parse("input.xml")
papers = tree.getroot()

# Loop over all <Paper> entries
for paper in papers.findall("Paper"):
  # remove papers without publication ID
  value = paper.find("pubID").text
  try:
   pubId = int(0 if value is None else value)
  except ValueError:
   # catch those pesky not-so-empty strings
   pubId = 0
  if pubId:
   # remove the following list of non-public subelements
   removalList = paper.findall("Title")
   removalList += paper.findall("Date_GPC_Requested")  
   removalList += paper.findall("Date_GPC_Formed")  
   removalList += paper.findall("GPC_Chair")  
   removalList += paper.findall("GPC_Members")  
   removalList += paper.findall("Date_Collaboration")
   removalList += paper.findall("Date_Submitted")
   removalList += paper.findall("Principle_Authors")
   removalList += paper.findall("Institutional_Readers")
   removalList += paper.findall("analysisID")
   for removeMe in removalList:
     paper.remove(removeMe)
   # add the following list of elements
   ET.SubElement(paper,"arxivID")
   ET.SubElement(paper,"inspireID")
   ET.SubElement(paper,"hepdataID")
   # print pubId, "keep"
  else:
   # if no pubID then remove this (non-public) entry completely
   papers.remove(paper)
   #print pubId, "removed"

tree.write("output.xml", encoding='utf-8', xml_declaration=True)

