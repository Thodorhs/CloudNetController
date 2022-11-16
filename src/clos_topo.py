#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController

import argparse
import sys
import time


class ClosTopo(Topo):

    def __init__(self, fanout, cores, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        coreA=[]
        agreA=[]
        edgA=[]
        hstA=[]
        count=1
        "Set up Core and Aggregate level, Connection Core - Aggregation level"
        for c in range(cores):
            cor = self.addSwitch('c' + str(count))
            coreA.append(cor)
            count=count+1
            for agr in range(fanout):
                agre= self.addSwitch('a' + str(count))
                agreA.append(agre)
                count=count+1
                "Set up Edge level, Connection Aggregation - Edge level "
                for e in range(fanout):
                    edg= self.addSwitch('e' + str(count))
                    edgA.append(edg)
                    count=count+1
                    "Set up Host level, Connection Edge - Host level "
                    for h in range(fanout):
                        hst= self.addHost('h' + str(count))
                        hstA.append(hst)
                        count=count+1
        "Create links"
        for c in range(len(coreA)):
            for agr in range(len(agreA)):
                self.addLink(coreA[c],agreA[agr])
        for agr in range(len(agreA)):
            for e in range(len(edgA)):
                self.addLink(agreA[agr],edgA[e])
        i=0
        for e in range(len(edgA)):
            self.addLink(edgA[e],hstA[i])
            self.addLink(edgA[e],hstA[i+1])
            i=i+2

            
	

def setup_clos_topo(fanout=2, cores=1):
    "Create and test a simple clos network"
    assert(fanout>0)
    assert(cores>0)
    topo = ClosTopo(fanout, cores)
    net = Mininet(topo=topo, controller=lambda name: RemoteController('c0', "127.0.0.1"), autoSetMacs=True, link=TCLink)
    net.start()
    time.sleep(20) #wait 20 sec for routing to converge
    net.pingAll()  #test all to all ping and learn the ARP info over this process
    CLI(net)       #invoke the mininet CLI to test your own commands
    net.stop()     #stop the emulation (in practice Ctrl-C from the CLI 
                   #and then sudo mn -c will be performed by programmer)

    
def main(argv):
    parser = argparse.ArgumentParser(description="Parse input information for mininet Clos network")
    parser.add_argument('--num_of_core_switches', '-c', dest='cores', type=int, help='number of core switches')
    parser.add_argument('--fanout', '-f', dest='fanout', type=int, help='network fanout')
    args = parser.parse_args(argv)
    setLogLevel('info')
    setup_clos_topo(args.fanout, args.cores)


if __name__ == '__main__':
    main(sys.argv[1:])