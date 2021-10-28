#!/usr/bin/env python3

import docker
from python_hosts import Hosts, HostsEntry
import time


def getDockerIp2names():
    client = docker.DockerClient()
    return {v['IPAddress']: v['Aliases'] for c in client.containers.list() for k, v in c.attrs['NetworkSettings']['Networks'].items() if len(v['IPAddress'])>0}

def getHostsIp2names(flag='managed'):
    h = Hosts()
    r = h.find_all_matching(name=flag)
    return {e.address: e.names for e in r}

def addFlag(ip2nameDict, flag='managed'):
    return {k: v + ['managed'] for k,v in ip2nameDict.items()}

def hostDiff(p, n):
    return {k: v for k, v in p.items() if k not in n or set(n[k]) != set(v)}

def addHostEntries(ip2nameFlaggedDict):
    h = Hosts()
    h.add([HostsEntry(entry_type='ipv4', address=k, names=v) for k, v in ip2nameFlaggedDict.items()])
    h.write()

def delHostEntries(addresses):
    h = Hosts()
    for address in addresses:
        h.remove_all_matching(address=address)
    h.write()

def printEntries(title, ip2namesDict):
    if len(ip2namesDict) == 0:
        return
    print(title)
    for k, v in ip2namesDict.items():
        print('  {} {}'.format(k, ' '.join(v)))



if __name__ == '__main__':
    print('Starting up docker -> /etc/hosts management')
    while True:
        dockerHosts = getDockerIp2names()
        target = addFlag(dockerHosts)
        current = getHostsIp2names()
        #print(dockerHosts)
        sub = hostDiff(current, target)
        add = hostDiff(target, current)
        printEntries('Removing entries:', sub)
        delHostEntries(sub.keys())
        printEntries('Adding entries:', add)
        #addHostEntries(add) # this must be coded this way, because adding entries with same flag/name like existing entries not working:
        if len(add) > 0:
            delHostEntries(current.keys())
            addHostEntries(target)
        time.sleep(1)




