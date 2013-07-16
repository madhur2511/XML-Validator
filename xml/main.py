from __future__ import print_function
import tree_builder
#print("XML Validation based on Schema")
#fileNameXML = raw_input("enter the XML doc name:")
fileNameXML= "books.xml"
fileObjectXML = open(fileNameXML, 'r')
#fileNameXSD = raw_input("enter the XML doc name:")
fileNameXSD = "books.xsd"
fileObjectXSD = open(fileNameXSD, 'r')
tree_builder.control(fileObjectXML,fileObjectXSD)

