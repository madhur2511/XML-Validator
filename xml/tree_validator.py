from __future__ import print_function
import copy
# Jashwanth

def treeCompare(rootXML, rootXSD):
    '''compares the two tree of XML and XSD'''
    i = 0    
    
    #print(str(len(rootXSD.childList))+"**************")
    while(i<len(rootXSD.childList)):
                            
        if minMaxBoundCheck(rootXML,rootXSD,i) == False:
            print("BOUNDS ERROR")
            print("Number of occurrences expected in the XML is not matching XSD specification")
            print("Element tag : " + rootXSD.childList[i].attrDict['name'] + " in XSD")
            #print("unmatch1")
            exit(-1)                        
                              
        if checkValidity(i, rootXML, rootXSD) == True:
            pass
        else:
            print("NAME ERROR")            
            print("Name of element in XSD does not match corresponding XML tag name")
            print("Element tag : " + rootXSD.childList[i].attrDict['name'] + " in XSD")
            print("Element tag : \"" + rootXML.childList[i].elementName + "\" in XML")
            exit(-1)
            
        treeCompare(rootXML.childList[i],rootXSD.childList[i])
        i = i + 1 
        
    if(len(rootXSD.childList) == 0):        
        if 'type' in rootXSD.attrDict and isType(rootXML.data, rootXSD.attrDict['type']):
            #print("match")
            pass
        else:            
            print("TYPE ERROR")
            print("datatype and data not matching")
            print("Expected type : "+rootXSD.attrDict['type'])
            print("Data : "+ rootXML.data)
            exit(-1)    

def checkValidity(i, rootXML, rootXSD):
    '''checks the validity of xml tags'''
    match = False
    #print (rootXML,"\n***\n",rootXSD)       
    if (rootXML.childList[i].elementName == (rootXSD.childList[i].attrDict['name']).replace('\"', '')) and (rootXML.childList[i].elementName == (rootXSD.childList[i].attrDict['name']).replace('\"', '')) :                
        if rootXSD.attrDict.has_key("__complexType__"):              
            if (rootXSD.attrDict['__complexType__'] == 1) and rootXSD.attrDict.has_key("__sequence__"):
                match = True                                                                                                                          
            
    return match
            
    
def isType(rootXMLData , rootXSDType):  
    '''different types of data type supported'''
    if rootXSDType == '"xs:string"':
        return True
    elif rootXSDType == '"xs:decimal"':
        try:
            float(rootXMLData)
        except :
            return False
        return True
    elif rootXSDType == '"xs:integer"':
        try:
            int(rootXMLData)
        except:
            return False
        return True
    elif rootXSDType == '"xs:positiveInteger"':
        try:
            tempint = int(rootXMLData)                       
            if tempint > 0:
                return True
            else:
                return False
        except:
            return False
        return True     
    elif rootXSDType == '"xs:negativeInteger"':
        try:
            tempint = int(rootXMLData)                       
            if tempint < 0:
                return True
            else:
                return False
        except:
            return False
        return True

def countElementNumber(rootXML, eleName):    
    count = 0
    for i in rootXML.childList:        
        if i.elementName == eleName[1:len(eleName)-1]:
            
            count = count + 1
    return count
    
def minMaxBoundCheck(rootXML,rootXSD, i):
        noMinOccurs = -1
        noMaxOccurs = -1
        if rootXSD.childList[i].attrDict.has_key('minOccurs'):            
            noMinOccurs = rootXSD.childList[i].attrDict['minOccurs']
            noMinOccurs = int(noMinOccurs[1:len(noMinOccurs)-1])
        if rootXSD.childList[i].attrDict.has_key('maxOccurs'):            
            noMaxOccurs = rootXSD.childList[i].attrDict['maxOccurs']
            if noMaxOccurs == '"unbounded"':
                noMaxOccurs = -2    # -2 means unbounded
            else:
                noMaxOccurs = int(noMaxOccurs[1:len(noMaxOccurs)-1])
        
        countEleNo = countElementNumber(rootXML, rootXSD.childList[i].attrDict['name'])        
        
        #both in minoccur and maxoccur present and specified
        minmax_flag = True
        if noMinOccurs >= 0 and noMaxOccurs >= 0:
            if noMinOccurs <= countEleNo and countEleNo <= noMaxOccurs:                
                for tag in range(countEleNo -1):
                    temp = copy.deepcopy(rootXSD.childList[i])
                    temp.attrDict.pop('minOccurs')
                    temp.attrDict.pop('maxOccurs')
                    rootXSD.childList.insert(i+1+tag, temp)
            else:                
                minmax_flag = False
        
        #minoccur specified and maxoccur unbounded or not present        
        elif noMinOccurs >=0 and noMaxOccurs < 0:   
            if noMinOccurs <= countEleNo:
                for tag in range(countEleNo -1):
                    temp = copy.deepcopy(rootXSD.childList[i])
                    if noMaxOccurs == -2:
                        temp.attrDict.pop('maxOccurs')
                    temp.attrDict.pop('minOccurs')                    
                    rootXSD.childList.insert(i+1+tag, temp)
            else:                
                minmax_flag = False
        
        #maxoccur present and specified
        elif noMinOccurs == -1 and noMaxOccurs >=0:
            if countEleNo <= noMaxOccurs and countEleNo >= 1:
                for tag in range(countEleNo -1):
                    temp = copy.deepcopy(rootXSD.childList[i])
                    temp.attrDict.pop('maxOccurs')                    
                    rootXSD.childList.insert(i+1+tag, temp)
            else:                
                minmax_flag = False
                
        #maxoccur unbounded      
        elif noMinOccurs == -1 and noMaxOccurs == -2:
            if countEleNo >= 1:
                for tag in range(countEleNo -1):
                    temp = copy.deepcopy(rootXSD.childList[i])
                    temp.attrDict.pop('maxOccurs')                    
                    rootXSD.childList.insert(i+1+tag, temp)
            else:                
                minmax_flag = False
        return minmax_flag