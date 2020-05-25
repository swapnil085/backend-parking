#import elastic search
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host':'localhost','port':9200}])

def create_index(indx,data):
	res = es.index(index=indx,doc_type='booking',body=data)
	return res

def delete_index(indx):
	es.indices.delete(index=indx, ignore=[400, 404])
