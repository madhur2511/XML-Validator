# build tree
from __future__ import print_function
import re
import copy
import node
import tree_validator

# Ankur
def control(fileObjectXML, fileObjectXSD):
    '''the main control of the tree builder and validator'''
    lineXML = ""
    for line in fileObjectXML:
        lineXML = lineXML + line
                
    lineXSD = ""
    for line in fileObjectXSD:
        lineXSD = lineXSD + line
    
    lineXML = remove_comments(lineXML)
    lineXSD = remove_comments(lineXSD)
    lineXML = remove_extra_spaces(lineXML)
    lineXSD = remove_extra_spaces(lineXSD)
    lineXML = lineXML.replace('\n','')
    lineXSD = lineXSD.replace('\n','')  
      
    listXMLTags = makeNodeList(lineXML)  
    listXSDTags = makeNodeList(lineXSD)         
    
    rootXML = makeTree(listXMLTags)    
    rootXSD = makeTree(listXSDTags)    
    
    newrootXSD = node.node("","","",{},[],0)
    augmentXSDTree(rootXSD,newrootXSD, 0)
    #printTree(newrootXSD)
    tree_validator.treeCompare(rootXML.childList[0],newrootXSD.childList[0])  
    
    print("Successfully matched!!")
    print("No errors found")

def remove_extra_spaces(s):
        '''removes duplicate spaces from stripped string s(param)'''
        s=s.strip()
        pc=' '
        ns=''
        for c in s:
                if ((c==' ') & (pc==' '))==False:
                        ns=ns+c
                        pc=c
        return ns
    
def remove_comments(line):
    ''' removes extra comments '''     
    i = 0
    search = line.find('<!--', i)    
    while search != -1:
        searchend = line.find('-->', i)
        if searchend == -1:
            print("malformed comment")
            exit(-1)
        else:
            line = line[:search] + line[searchend+3:]
            i = search + 1
        search = line.find('<!--', i)
    return line

class depth:
    ''' depth of each node initialized'''
    def __init__(self):
        self.depth = 0

def addClosingTags(line):  
    ''' Add closing tags to tags with /> '''      
    closing = line.find('/>')
    opening = line.find('<')
    if(closing != -1):
        openingName = line[opening+1:line.find(' ')]
        line = line[:len(line)-2] + '></' + openingName + '>'    
    return line
        

            
def makeNodeList(line):            
    ''' makes a list of objects of type node '''
    patternData = re.compile('<[^>]*>[^<]*')    
    tagList = patternData.findall(line)
  
    nodeList = []    
    d = depth()
    index = 0
    for i in tagList:
        data = i[i.find('>')+1:].strip()
        i = i[:i.find('>')+1]           
        tmp = addClosingTags(i)         
        tempList = patternData.findall(tmp)
        
        if(len(tempList) == 2):
            nodeList.append(makeNode(tempList[0], d, data)) 
            nodeList.append(makeNode(tempList[1], d, ""))
        else:
            nodeList.append(makeNode(tmp, d, data))  
        index = index + 1
        #print(i)
    return nodeList

def makeNode(line, d, adata):   
    ''' makes a object of type node from a string '''
    closing = line.find('</')
    if(closing != -1):
        d.depth = d.depth - 1
        line = line[2:len(line)-1]
    else:
        d.depth = d.depth + 1
        line = line[1:len(line)-1]        

    entities = line.split(' ')    
    if entities[0].find(':') != -1:
        tempName = entities[0].split(':')
        elementName = tempName[1]
        namespace  = tempName[0]
    else:
        elementName = entities[0]
        namespace = ""
        
        
    data = adata
    attrDict = {}
    childList = []
    i=1
    while(i<len(entities)):
        try:
            tempattr = entities[i].split('=')   
        except:
            print('Syntax Error in XSD :' + entities[i])
            exit(-1)        
        attrDict[tempattr[0]] = tempattr[1]
        i = i + 1
    
    newnode = node.node(elementName, namespace, data, attrDict, childList, d.depth)
    return newnode

# Madhur         
    
def makeTree(listXMLTags):
    ''' makes a tree of nodes '''
    stack=[node.node("","","",{},[],0)]
    tos=0
    i=0;
    while(i<len(listXMLTags)):
        if(stack[tos].depth < listXMLTags[i].depth):
            stack.append(listXMLTags[i])
            tos=tos+1
        elif(tos>0):
            stack.append(listXMLTags[i])
            if listXMLTags[i].elementName != stack[tos].elementName:
                print("SYNTAX ERROR !!")
                print("Starting tag does not have a matching closing Tag")
                print("Starting Tag : " + listXMLTags[i].elementName + " , Closing Tag : " + stack[tos].elementName)
                #print("unmatch")    
                exit(-1)
            stack.pop()
            stack[tos-1].childList.append(stack[tos])
            stack.pop()
            tos=tos-1 
        i=i+1
    return stack[0]  


def printTree(root):    
    ''' prints the tree '''
    for i in root.childList:        
        print(i, end = '\n\n')
        printTree(i)
    
                 
def augmentXSDTree(rootXSD, newrootXSD, j):
    '''modifies the tree to suit tree comparison'''
    for i in rootXSD.childList:		
        if i.elementName == 'element':            
            j=0
            temp = copy.deepcopy(i)
            temp.childList = []
            newrootXSD.childList.append(temp)
            augmentXSDTree(i, temp, j)
                
        elif i.elementName == 'complexType':
            j = j+1
            newrootXSD.attrDict['__complexType__'] = j			
            augmentXSDTree(i, newrootXSD,j)
        elif i.elementName == 'sequence':
		 j = j+1
		 newrootXSD.attrDict['__sequence__'] = j
		 augmentXSDTree(i, newrootXSD, j)        
        else:			
            augmentXSDTree(i, newrootXSD, j)
                       
