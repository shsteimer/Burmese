from persistencemanager import PersistenceManager

class Item(object):
	def __init__(self,parent,name):
		self.parent=parent
		self.name=name

class Attribute(Item):
	def __init__(self,parent,name,value):
		super(Attribute,self).__init__(parent,name)
		self.value=value

class Node(Item):
	def __init__(self,parent,name):
		super(Node,self).__init__(parent,name)
		self.path=self.__getPath__()
		self.depth=self.__getDepth__()
		self.attributes = []
		self.children = []
	
	def addChild(self,name):
		child = Node(self,name)
		self.children.append(child)
	
	def isRoot(self):
		return self.parent==None
	
	def __getPath__(self):
		if self.isRoot():
			return "/"
		
		parentPath = self.parent.__getPath__()
		if self.parent.isRoot():
			return parentPath + self.name
		else:
			return parentPath + "/" + self.name
	
	def __getDepth__(self):
		if self.isRoot():
			return 0
		
		parentDepth = self.parent.__getDepth__()
		return parentDepth+1
		
	def getAttributesDictionary(self):
		return dict([(attr.name,attr.value) for attr in self.attributes])
		
	def setAttribute(self,name,value):
		attr = Attribute(self,name,value)
		self.attributes.append(attr)


class Repository(object):
	def __init__(self):
		self.root = Node(None,"root")
		self.pm = PersistenceManager()
	
	def getNode(self,path):
		pass

	def addNode(self,parent,name):
		parent.addChild(name)

	def deleteNode(self,node):
		pass

	def save(self):
		self.pm.save(self)


