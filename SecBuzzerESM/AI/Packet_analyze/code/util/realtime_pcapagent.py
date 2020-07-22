# -*- coding: UTF-8 -*-
#!/usr/bin/env python3
import os, json
from datetime import datetime as dt
from scapy.all import sniff, TCP, IP
# from configparser import ConfigParser
from elasticsearch import Elasticsearch
from .pcap_decode import PcapDecode
from .pcap_read_protocol import PcapReadProtocol
from .es import ES

# define for ES connection
# parser=ConfigParser()
# parser.read('config.cfg')
# ELASTICSEARCH_HOST=parser.get('ElasticSearch','ELASTICSEARCH_HOST')
# ELASTICSEARCH_PORT=parser.get('ElasticSearch','ELASTICSEARCH_PORT')
# ELASTICSEARCH_INDEX=parser.get('ElasticSearch','ELASTICSEARCH_INDEX')
# ELASTICSEARCH_DATA_TYPE=parser.get('ElasticSearch','ELASTICSEARCH_DATA_TYPE')
# ES_CONN = ELASTICSEARCH_HOST + ':' + ELASTICSEARCH_PORT

# os.environ['ELASTICSEARCH_HOST']='192.168.70.174'
# os.environ['ELASTICSEARCH_PORT']='19200'
# os.environ['ELASTICSEARCH_INDEX']='king_0601'
# os.environ['ELASTICSEARCH_DATA_TYPE']='test'
ES_CONN = os.environ['ELASTICSEARCH_HOST'] + ':' + os.environ['ELASTICSEARCH_PORT']


class RealtimePcapAgent():

    def __init__(self, ifname):
        self.ifname = ifname
        self.ETHER_DICT = dict()
        self.IP_DICT = dict()
        self.PORT_DICT = dict()
        self.TCP_DICT = dict()
        self.UDP_DICT = dict()
        self.counter = 0


    def saveToES(self,decode_data):

        try:
            es_conn = Elasticsearch([ES_CONN])
            # es_conn = Elasticsearch([{'host':ELASTICSEARCH_HOST,'port':ELASTICSEARCH_PORT}])
            es = ES(es_conn, os.environ['ELASTICSEARCH_INDEX'], os.environ['ELASTICSEARCH_DATA_TYPE'])

            # print("saveToES = {}\n".format(decode_data))
            es.create(decode_data)
            self.counter = self.counter + 1
            print ("self.counter = {} \n".format(self.counter))
        except Exception as e:
            print("saveToES error")


    def pktCallback(self, pkt):

        # print("RealtimePcapAgent pktCallback")
        pd = PcapDecode(self.ETHER_DICT,self.IP_DICT,self.PORT_DICT,self.TCP_DICT,self.UDP_DICT)
        # decode_data = pd.ip_decode(pkt)
        decode_data = pd.ether_decode(pkt)
        # print("data = {}\n".format(decode_data))
        if decode_data != None and len(decode_data)>1 :
            # print("data = {}\n".format(decode_data))
            self.saveToES(decode_data)


    def sniff_filter(self, pkt):

        # if TCP in pkt and IP in pkt:
        #     if pkt[TCP].dport==80 or pkt[TCP].sport==80:
        #         return pkt
        return pkt


    def sniff(self):

        try:
            # print("RealtimePcapAgent sniff before")
            sniff(lfilter=self.sniff_filter,prn=self.pktCallback, iface=self.ifname) 
            # print("RealtimePcapAgent sniff end")
        except Exception as e:
            print("sniff error")
        return


    def process(self):

        prp = PcapReadProtocol()
        self.ETHER_DICT,self.IP_DICT,self.PORT_DICT,self.TCP_DICT,self.UDP_DICT  = prp.read()

        print("process network packet ~~~\n\n")
        self.sniff()
