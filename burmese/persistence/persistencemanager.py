from burmese.repository.repository import Repository,Node
import pymongo

class PersistenceManager(object):
	def __init__(self,host,port,repositoryId):
		 self._connection = pymongo.Connection(host, port)
		 self._db = connection[repositoryId]
		 self._nodes = self._db.nodes
		 self._nodes.ensureIndex({"path":1,"active":1}{"unique":true});
		 self._nodes.ensureIndex("parentId");

	def getNodeByPath(self,path):
		self._nodes.ensureIndex("path")
		doc = self._nodes.find_one({"path":path})
		return convertBSONToNode(doc)
	
	def queryNodes(self,parameters):
		docs = self._nodes.find(parameters)
		docList=[]
		for doc in docs:
			docList.append(convertBSONToNode(doc))
		
		return docList
	
	def saveNode(self,node):
		pass
		
	def addNode(self,node):
		self._nodes.insert(convertNodeToBSON(node))
	
	def deleteNodeByPath(self,path):
		pass
	
	def deleteNodeById(self,nodeId):
		pass

		
def convertNodeToBSON(node):
	nodeBSON = {"name": node.name,
			"depth":node.depth,
			"path":node.path,
			"_id":node.id,
			"nodeType":node.nodeType,
			"version":node.version,
			"active":node.active,
			"parentId":node.parentId}
	
	nodeBSON.update(node.attributes)
	nodeBSON['content']=node.content
	return nodeBSON

def convertBSONToNode(bson):
	pass


