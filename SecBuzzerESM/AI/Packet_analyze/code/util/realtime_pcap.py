import pcap
import dpkt
import socket
import pandas as pd
import numpy as np
import datetime


class RealtimePcap:

    def __init__(self,ifname):    
        print("")
        self.ifname = ifname
        # self.sniffer=pcap.pcap(name=None, promisc=True, immediate=True, timeout_ms=50)        
        self.sniffer=pcap.pcap(name=self.ifname, promisc=True, immediate=True, timeout_ms=50)
        self.sniffer.setfilter('tcp') # 可以是'tcp' 'udp' 'port 80'        

    def arpProcess(self, eth):
        print("arpProcess")
        arp = eth.arp
        src_ip = socket.inet_ntoa(arp.spa)
        src_port = np.nan
        dst_ip = socket.inet_ntoa(arp.tpa)
        dst_port = np.nan

        print("arpProcess : src_ip = {}, src_port = {}, dst_ip = {}, dst_port = {}"\
            .format(src_ip, src_port, dst_ip, dst_port))    

        return [src_ip, src_port, dst_ip, dst_port]


    def normalProcess(self, eth):   
        ip = eth.data
        if ip.v == 4:   
            src_ip = socket.inet_ntoa(ip.src)
            dst_ip = socket.inet_ntoa(ip.dst)
            
        elif ip.v == 6:
            src_ip = socket.inet_ntop(socket.AF_INET6, ip.src)
            dst_ip = socket.inet_ntop(socket.AF_INET6, ip.dst)
            try:
                src_ip = IPNetwork(src_ip).ipv4()
            except:
                pass
            try:
                dst_ip = IPNetwork(dst_ip).ipv4()
            except:
                pass
            src_ip = str(src_ip).split('/')[0]
            dst_ip = str(dst_ip).split('/')[0]
              
        try:
            src_port = ip.data.sport
            dst_port = ip.data.dport
        except:
            src_port = np.nan
            dst_port = np.nan

        print("normalProcess : src_ip = {}, src_port = {}, dst_ip = {}, dst_port = {}"\
            .format(src_ip, src_port, dst_ip, dst_port))    

        return [src_ip, src_port, dst_ip, dst_port]


    def run(self):

        for i,streamdata in self.sniffer:

            eth = dpkt.ethernet.Ethernet(streamdata)
            # print ("Ethernet Frame: ", mac_addr(eth.src), mac_addr(eth.dst), eth.type)

            if not isinstance(eth.data, dpkt.ip.IP):
                print ("Non IP Packet type not supported {} \n".format(eth.data.__class__.__name__))
                continue
                
            try:
                # 2054 是 ARP
                if eth.type == 2054:
                    self.arpProcess(eth)
                else:
                    self.normalProcess(eth)
            except:
                print("except")
