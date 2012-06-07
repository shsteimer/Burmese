from bermese.persistence.persistencemanager import PersistenceManager
import hashlib

class Item(object):
	def __init__(self,parent,name,session):
		self.name=name
		self.depth=self._getDepth(parent)
		
	def _getDepth(self,parent):
		if parent==None:
			return 0
		
		parentDepth = parent.depth
		return parentDepth+1

class Node(Item):
	def __init__(self,parent,name,session):
		super(Node,self).__init__(parent,name,session)
		self.session=session
		self.nodeType="unstructured"
		self.version="1.0"
		self.active=true
		self.path=self._getPath(parent)
		self.id = self._getId()
		if parent!=None:
			self.parentId=parent.id
		
		self.attributes = {}		
		self.content=None
		self._children = []
	
	def addChild(self,name):
		child = Node(self,name,self.session)
		self._children.append(child.id)
		self.session._saveNode(self)
		return child
	
	def getChildren(self):
		self.session.getNodes({"parent": self.id, "active":true})
	
	def setContentFromFile(self,contentFile):
		self.content = contentFile.readlines()
		self.session._saveNode(self)
	
	def setContentFromString(self,content):
		self.content=content.split('\n')
		self.session._saveNode(self)
		
	def versionNode(self,newVersion):
		self.active=false
		self.session._saveNode(self)
		
		self.version=newVersion
		self.id=self._getId()
		self.active=true
		self.session._saveNode(self)
	
	def clearAttribute(self,name):
		del self.attributes[name]
		self.session._saveNode(self)
	
	def setAttribute(self,name,value):
		self.attributes[str(name)]=value
		self.session._saveNode(self)
	
	def isRoot(self):
		return self.depth==0
	
	def _getPath(self,parent):
		if self.isRoot():
			return "/"
			
		parentPath = parent.path
		if parent.isRoot():
			return parentPath + self.name
		else:
			return parentPath + "/" + self.name

	def _getId():
		return hashlib.sha224(self.path + self.version).hexdigest()

class Repository(object):
	def __init__(self,pm=None,repositoryId="BurmeseDefaultRepository"):
		if pm==None:
			self._pm = PersistenceManager("localhost", 27017, repositoryId)
			root = Node(None,"root")
			ses = self.getSession()
			ses._saveNode(root)
		else
			self._pm = pm
	
	def getSession(self,credentials):
		return Session(self._pm)

class Session(object):
	def __init__(self,pm):
		self._pm=pm
		
	def getNode(self,path):
		return self._pm.getNodeByPath(path)
	
	def getNodes(self,parameters):
		return self._pm.queryNodes(parameters)
	
	def _saveNode(self,node):
		self._pm.saveNode(node)

	def deleteNodeByPath(self,path):
		self._pm.deleteNodeByPath(path)
	
	def deleteNode(self,node):
		self._pm.deleteNodeById(node.id)

