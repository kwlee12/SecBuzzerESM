# -*- coding: UTF-8 -*-
#!/usr/bin/env python3
import os
from util.realtime_pcapagent import RealtimePcapAgent
from util.pcapagent import PcapAgent
# from configparser import ConfigParser


if __name__ == '__main__':
    # # realtime parse
    # parser=ConfigParser()
    # parser.read('config.cfg')    
    # INTERFACE_NAME=parser.get('Interface','INTERFACE_NAME')
    # print("INTERFACE_NAME = {}".format(INTERFACE_NAME))

    # os.environ['INTERFACE_NAME']='ens19'
    print(os.environ.get('INTERFACE_NAME'))    
    rt_parser = RealtimePcapAgent(os.environ.get('INTERFACE_NAME'))
    rt_parser.process()

    # # pcap parse
    # parser = PcapAgent('fingerprint_test1.pcap')
    # parser = PcapAgent('king_01.pcapng')
    # parser.process()
