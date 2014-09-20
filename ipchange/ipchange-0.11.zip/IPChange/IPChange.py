# coding: utf-8
'''
Created on 2014年9月19日

@author: root
'''

import os,re

def getMachine_ethNum():
        '''
        返回本机的所有网卡
        '''
        output = os.popen('ifconfig -a | grep eth')
        ethStrlines = output.read()
        outputs = ethStrlines.strip().splitlines()
        eth=[]
        for line in outputs:
            ethContent = line.split()
            eth += [ethContent[0]]
        
        return eth          

def getMachine_IP():
        '''
        获取当前机器上配置的所有网卡的ip地址信息，返回形如：
        {eth0:{ip:192.168.1.2,netmask:255.255.255.0, gateway:192.168.1.2}}
        上述信息通过解析/etc/network/interfaces文件获得
        
        '''
        result={}
        netCFG = '/etc/network/interfaces'
        eths = getMachine_ethNum()
        cfg = open(netCFG, 'r')
        contents = cfg.read()
        cfg.close()
        
        ipaddresses=[]
                         
        netCFGPattern='auto\s+(eth\d+)\n+iface\s+(eth\d+)\s+inet\s+static\n+address\s+(\d+.\d+.\d+.\d+)\n+netmask\s+(\d+.\d+.\d+.\d+)\n+gateway\s+(\d+.\d+.\d+.\d+)'
        pr = re.compile(netCFGPattern)
        it = pr.finditer(contents)        
        for ma in it:   
            eth_tmp1,eth_tmp, ip_tmp, netmask_tmp, gateway_tmp = ma.groups()            
            # 写匹配部分
            eths.remove(eth_tmp)
            result[eth_tmp]={}
            result[eth_tmp]['ip']=ip_tmp
            ipaddresses += [ip_tmp]
            result[eth_tmp]['netmask']=netmask_tmp
            result[eth_tmp]['gateway']=gateway_tmp
        
        cfg = open(netCFG, 'w')
        cfg.write(contents)
        
        i=1        
        for eth in eths:
            ip = '192.168.1.%s' % (i)
            while ip in ipaddresses:
                i += 1
                ip = '192.168.1.%s' % (i)                
            netmask='255.255.255.0'
            gateway='192.168.1.1'
            netCFGChangePattern = 'auto %s\niface %s inet static\naddress %s\nnetmask %s\ngateway %s\n' % (eth, eth, ip, netmask, gateway)
            cfg.write(netCFGChangePattern)
            result[eth]={}
            result[eth]['ip']=ip
            result[eth]['netmask']=netmask
            result[eth]['gateway']=gateway
            i += 1
            
        cfg.close()
        
        return result
    
            
def updateMachine_IP(ethnum, ip, netmask, gateway):
        '''
        1,生成interfaces文件
        2,填充interfaces文件的相关部分
        3,copy生成的interfaces文件到/etc/network/interfaces
        @return: 
            -1: ethnum错误，没有这个网卡
            0： 更改成功
            1：ip地址不对
            2：netmask不对
            3：gateway不对
        '''
        
        #获得当前的所有ethnum配置信息
        
        if ethnum not in getMachine_ethNum():
            return -1  #无此网卡
        
        ipv4_pattern = re.compile(r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b")
        
        if not ipv4_pattern.match(ip):
            return 1
        if not ipv4_pattern.match(netmask):
            return 2
        if not ipv4_pattern.match(gateway):
            return 3
               
        netCFG = '/etc/network/interfaces'
        cfg = open(netCFG, 'r')
        contents = cfg.read()
        cfg.close()
        cfg = open(netCFG, 'w')        
        netCFGPattern='auto\s+(eth\d+)\n+iface\s+(eth\d+)\s+inet\s+static\n+address\s+(\d+.\d+.\d+.\d+)\n+netmask\s+(\d+.\d+.\d+.\d+)\n+gateway\s+(\d+.\d+.\d+.\d+)'
        pr = re.compile(netCFGPattern)
        it = pr.finditer(contents)
        startpos = 0
        for ma in it:   
            eth_tmp1,eth_tmp, ip_tmp, netmask_tmp, gateway_tmp = ma.groups()
            cfg.write(contents[startpos:ma.start()])
            # 写匹配部分
            if eth_tmp == ethnum:
                netCFGChangePattern = 'auto %s\niface %s inet static\naddress %s\nnetmask %s\ngateway %s\n' % (ethnum,ethnum, ip, netmask, gateway)
                cfg.write(netCFGChangePattern)
            else:
                cfg.write(contents[ma.start():ma.end()])            
            startpos = ma.end()
        
        cfg.write(contents[startpos:].strip())
        cfg.close()
        
        return 0
        

if __name__ == '__main__':
    print getMachine_ethNum()
    print getMachine_IP()
    print updateMachine_IP('eth0','192.168.1.105','255.255.255.0','192.168.1.1')