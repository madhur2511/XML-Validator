class node:
    
    def __init__(self, elementName = "" , namespace = "", data = "",  attrDict = {}, childList = [], depth = 1):                      
        self.elementName = elementName
        self.namespace = namespace
        self.data = data
        self.attrDict = attrDict
        self.childList = childList
        self.depth = depth
    
    def __str__(self):
        return ("Element :" + str(self.elementName) +"\n" +
        "Namespace :" + str(self.namespace)  +"\n" +
        "Data :" + str(self.data) + "\n" +
        "AttrDict :" + str(self.attrDict)  +"\n" +
        "childList :"+ str(self.childList) +"\n" +
        "depth :"+ str(self.depth))                       


        