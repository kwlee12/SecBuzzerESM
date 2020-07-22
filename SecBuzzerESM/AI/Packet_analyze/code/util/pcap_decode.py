# -*- coding: UTF-8 -*-
#!/usr/bin/env python3
import os
import time,json
# from configparser import ConfigParser
import scapy_http.http as http

# parser=ConfigParser()
# parser.read('config.cfg')
# ETHER_ENABLE=parser.get('NetworkPacket','ETHER_ENABLE')
# IP_ENABLE=parser.get('NetworkPacket','IP_ENABLE')
# TCP_ENABLE=parser.get('NetworkPacket','TCP_ENABLE')
# UDP_ENABLE=parser.get('NetworkPacket','UDP_ENABLE')
# IPV6_ENABLE=parser.get('NetworkPacket','IPV6_ENABLE')
# HTTP_ENABLE=parser.get('NetworkPacket','HTTP_ENABLE')

# os.environ['ETHER_ENABLE']='TRUE'
# os.environ['IP_ENABLE']='TRUE'
# os.environ['TCP_ENABLE']='TRUE'
# os.environ['UDP_ENABLE']='TRUE'
# os.environ['IPV6_ENABLE']='TRUE'
# os.environ['HTTP_ENABLE']='TRUE'

# print(os.environ.get('ETHER_ENABLE'))  
# print(os.environ.get('IP_ENABLE'))  
# print(os.environ.get('TCP_ENABLE'))  
# print(os.environ.get('UDP_ENABLE'))  
# print(os.environ.get('IPV6_ENABLE'))  
# print(os.environ.get('HTTP_ENABLE'))  

class PcapDecode:

    def __init__(self,ETHER_DICT,IP_DICT,PORT_DICT,TCP_DICT,UDP_DICT):
        self.ETHER_DICT = ETHER_DICT
        self.IP_DICT = IP_DICT
        self.PORT_DICT = PORT_DICT
        self.TCP_DICT = TCP_DICT
        self.UDP_DICT = UDP_DICT


    def ether_decode(self, p):
        data = dict()
        if p.haslayer('Ether'):
            data = self.ip_decode(p)
            return data
        else:
            data['@timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
            data['SourceIP'] = 'Unknow'
            data['DestinationIP'] = 'Unknow'
            data['Procotol'] = 'Unknow'
            # data['len'] = len(str(p))
            # data['info'] = p.summary()
            return data


    def ip_decode(self, p):
        data = dict()
        if p.haslayer('IP'):  #2048:Internet IP (IPv4) 
            ip = p.getlayer('IP')
            if p.haslayer('TCP'):  #6:TCP
                data = self.tcp_decode(p, ip)
                return data
            elif p.haslayer('UDP'): #17:UDP
                data = self.udp_decode(p, ip)
                return data
            elif (os.environ['IP_ENABLE']  == 'TRUE'):
                if ip.proto in self.IP_DICT:
                    data['@timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
                    data['SourceIP'] = str(ip.src)
                    data['DestinationIP'] = str(ip.dst)
                    data['Procotol'] = self.IP_DICT[ip.proto]
                    data['len'] = len(str(p))
                    # data['info'] = p.summary()
                    return data
                else:
                    data['@timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
                    data['SourceIP'] = str(ip.src)
                    data['DestinationIP'] = str(ip.dst)
                    data['Procotol'] = 'IPv4'
                    data['len'] = len(str(p))
                    # data['info'] = p.summary()
                    return data
            else:
                pass

        elif p.haslayer('IPv6'):  #34525:IPv6
            ipv6 = p.getlayer('IPv6')
            if p.haslayer('TCP'):  #6:TCP
                data = self.tcp_decode(p, ipv6)
                return data
            elif p.haslayer('UDP'): #17:UDP
                data = self.udp_decode(p, ipv6)
                return data
            elif (os.environ['IPV6_ENABLE']  == 'TRUE'):
                if ipv6.nh in self.IP_DICT:
                    data['@timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
                    data['SourceIP'] = str(ipv6.src)
                    data['DestinationIP'] = str(ipv6.dst)
                    data['Procotol'] = self.IP_DICT[ipv6.nh]
                    data['len'] = len(str(p))
                    # data['info'] = p.summary()
                    return data
                else:
                    data['@timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
                    data['SourceIP'] = str(ipv6.src)
                    data['DestinationIP'] = str(ipv6.dst)
                    data['Procotol'] = 'IPv6'
                    data['len'] = len(str(p))
                    # data['info'] = p.summary()
                    return data
            else:
                pass

        elif (os.environ['ETHER_ENABLE']  == 'TRUE'):
            if p.type in self.ETHER_DICT:
                data['@timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
                data['SourceIP'] = str(p.src)
                data['DestinationIP'] = str(p.dst)
                data['Procotol'] = self.ETHER_DICT[p.type]
                data['len'] = len(str(p))
                data['info'] = p.summary()
                return data
            else:
                data['@timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
                data['SourceIP'] = str(p.src)
                data['DestinationIP'] = str(p.dst)
                data['Procotol'] = hex(p.type)
                data['len'] = len(str(p))
                data['info'] = p.summary()
                return data

        else:
            pass


    def tcp_decode(self, p, ip):
        data = dict()
        tcp = p.getlayer('TCP')
        if p.haslayer('HTTP') and p.haslayer(http.HTTPRequest) and (os.environ['HTTP_ENABLE']  == 'TRUE'):  #6:HTTP HTTPRequest
            data = self.http_decode(p, ip)
            return data             
        elif p.haslayer('HTTP') and p.haslayer(http.HTTPResponse) and (os.environ['HTTP_ENABLE']  == 'TRUE'):  #6:HTTP HTTPResponse
            data = self.http_decode(p, ip)
            return data 
        else:
            if(os.environ['TCP_ENABLE'] == 'TRUE'):
                data['@timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
                data['SourceIP'] = str(ip.src)
                data['SourcePort'] = str(ip.sport)
                data['DestinationIP'] = str(ip.dst)
                data['DestinationPort'] = str(ip.dport)
                # data['info'] = p.summary()

                if tcp.dport in self.PORT_DICT:
                    data['Procotol'] = self.PORT_DICT[tcp.dport]
                elif tcp.sport in self.PORT_DICT:
                    data['Procotol'] = self.PORT_DICT[tcp.sport]
                elif tcp.dport in self.TCP_DICT:
                    data['Procotol'] = self.TCP_DICT[tcp.dport]
                elif tcp.sport in self.TCP_DICT:
                    data['Procotol'] = self.TCP_DICT[tcp.sport]
                else:
                    data['Procotol'] = "TCP"

                data['len'] = len(str(tcp))
                data['TCP_header'] = str(p['TCP'].fields)

                # if tcp.flags.F:
                #     print('FIN received')
                # if tcp.flags.S:
                #     print('SYN received')
                # if tcp.flags.R:
                #     print('RST received')
                # if tcp.flags.P:
                #     print('PSH received')
                # if tcp.flags.A:
                #     print('ACK received')
                # if tcp.flags.U:
                #     print('URG received')                    
                # if tcp.flags.E:
                #     print('ECE received')
                # if tcp.flags.C:
                #     print('CWR received')

                return data
            else:
                # return data      
                pass          


    def udp_decode(self, p, ip):
        data = dict()
        udp = p.getlayer('UDP')
        if(os.environ['UDP_ENABLE'] == 'TRUE'):
            data['@timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
            data['SourceIP'] = str(ip.src)
            data['SourcePort'] = str(ip.sport)
            data['DestinationIP'] = str(ip.dst)
            data['DestinationPort'] = str(ip.dport)
            # data['info'] = p.summary()

            if udp.dport in self.PORT_DICT:
                data['Procotol'] = self.PORT_DICT[udp.dport]
            elif udp.sport in self.PORT_DICT:
                data['Procotol'] = self.PORT_DICT[udp.sport]
            elif udp.dport in self.UDP_DICT:
                data['Procotol'] = self.UDP_DICT[udp.dport]
            elif udp.sport in self.UDP_DICT:
                data['Procotol'] = self.UDP_DICT[udp.sport]
            else:
                data['Procotol'] = "UDP"

            data['len'] = len(str(udp))
            data['UDP_header'] = str(p['UDP'].fields)

            return data
        else:
            # return data
            pass


    def http_getHeader(self, request, header): 

        # print("http_getHeader request = {} , header = {}".format(request,header))
        start_index = request.find(header)
        if start_index <= 1:
            return None

        end_index = request.find('\\r\\n',start_index)
        if end_index <= 1:
            end_index = request.find(',',start_index)
            if end_index <= 1:
                return None

        # print("find start_index={} end_index={}".format(start_index,end_index))
        start_index = start_index + len(header) + 2
        return request[start_index:end_index]


    def http_decode(self, p, ip):
        data = dict()
        
        # header_list = ['Host','Method','URI','User-Agent','Accept-Language','Status','Rrferer','Const','Field']
        header_list = ['Method','URI','User-Agent','Accept-Language','Status','Rrferer','Const','Field']

        if p.haslayer(http.HTTPRequest):
            print("HTTP Request")
            http_header_dict = dict()
            httplayer = p.getlayer('http')

            data['@timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
            data['URL'] = str(p[http.HTTPRequest].Host) + str(p[http.HTTPRequest].Path)            
            data['Host'] = str(p[http.HTTPRequest].Host)      
            data['SourceIP'] = str(ip.src)
            data['SourcePort'] = str(ip.sport)
            data['DestinationIP'] = str(ip.dst)
            data['DestinationPort'] = str(ip.dport)
            data["IP"] = str(p["IP"].fields)
            data["HTTP Request"] = str(p["HTTP Request"].fields)

            str_http_request = str(p['HTTP Request'].fields)
            for header in header_list:
                tempheader = self.http_getHeader(str_http_request,header)
                if tempheader != None:
                    http_header_dict[header] = tempheader
                else:
                    http_header_dict[header] = "-"

            data['HTTP Request'] = json.dumps(http_header_dict)
            # data['info'] = p.summary()
            data['Procotol'] = 'HTTP Request'
            data['len'] = len(str(httplayer))      
            # print ("data = {}".format(data))   

            p.show()
            return data


        if p.haslayer(http.HTTPResponse):
            print("HTTP Response")
            http_header_dict = dict()
            httplayer = p.getlayer("http")

            data['@timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
            data['SourceIP'] = str(ip.src)
            data['SourcePort'] = str(ip.sport)
            data['DestinationIP'] = str(ip.dst)
            data['DestinationPort'] = str(ip.dport)
            data['IP'] = str(p['IP'].fields)
            # data["HTTP Response"] = str(p["HTTP Response"].fields)

            str_http_response = str(p['HTTP Response'].fields)
            for header in header_list:
                tempheader = self.http_getHeader(str_http_response,header)
                if tempheader != None:
                    http_header_dict[header] = tempheader
                else:
                    http_header_dict[header] = "-"

            data['HTTP Response'] = json.dumps(http_header_dict)
            # data['info'] = p.summary()
            data['Procotol'] = 'HTTP Response'
            data['len'] = len(str(httplayer))
            # print ("data = {}".format(data))         

            p.show()
            return data
        