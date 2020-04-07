#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-

"""
**************************************************************************************************************************************************
            python调用cmd命令获取本机的基本信息
            hostname：主机名
            machine_code：本机机器码
            localIP：本机ip
**************************************************************************************************************************************************
"""
import os, re




def system_spec():
    information = {}
    encodestr = "chcp 65001"
    cmd = 'ipconfig /all'
    os.popen(encodestr).read()
    res = os.popen(cmd)
    output_str = res.read()                                                                                                                          #获得输出字符串
    information['hostname'] = str(re.findall("Host Name . . . . . . . . . . . . : (.*?)Primary Dns Suffix", output_str, re.S)[0]).strip()            #主机名
    information['machine_code'] = str(re.findall("Physical Address. . . . . . . . . :(.*?)DHCP Enabled", output_str, re.S)[0]).strip()               #本机机器码
    information['localIP'] = re.findall("IPv4 Address. . . . . . . . . . . : (.*?)\(", output_str, re.S)[0]                                          #本机ip
    return information



if __name__ == '__main__':
    print(system_spec())



