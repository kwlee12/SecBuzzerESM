# -*- coding: UTF-8 -*-
#!/usr/bin/env python3
# from elasticsearch import Elasticsearch as ES

class ES:

    def __init__(self, es, es_index, doc_type):

        self.id = 0
        self.es = es
        self.index = self._check_index_exist(es_index)
        self.doc_type = doc_type


    def _check_index_exist(self, index):

        if not self.es.indices.exists(index=index):
            self.es.indices.create(index=index)

        return index


    def create(self, create_data):
        try:
            res = self.es.index(index=self.index, doc_type=self.doc_type  ,body=create_data )
            print (res)
        except Exception as e:
            print("exception = {}".format(e))