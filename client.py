import time
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '* Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    info( '* Add switches\n')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)

    info( '* Add hosts\n')
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h9 = net.addHost('h9', cls=Host, ip='10.0.0.9', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)

    info( '* Add links\n')

    net.addLink(h1, s1, bw=40)
    net.addLink(s2, s1, bw=40)
    net.addLink(s1, s3, bw=40)
    net.addLink(s3, s7, bw=20)
    net.addLink(s3, s6, bw=20)
    net.addLink(s2, s5, bw=20)
    net.addLink(s2, s4, bw=20)
    net.addLink(s4, h2, bw=10)
    net.addLink(s4, h3, bw=10)
    net.addLink(s5, h4, bw=10)
    net.addLink(s5, h5, bw=10)
    net.addLink(s6, h6, bw=10)
    net.addLink(s6, h7, bw=10)
    net.addLink(s7, h8, bw=10)
    net.addLink(s7, h9, bw=10)

    info( '* Starting network\n')
    net.build()
    info( '* Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '* Starting switches\n')
    net.get('s2').start([c0])
    net.get('s4').start([c0])
    net.get('s5').start([c0])
    net.get('s6').start([c0])
    net.get('s1').start([c0])
    net.get('s3').start([c0])
    net.get('s7').start([c0])

    info( '* Post configure switches and hosts\n')

   

   
    h1.cmd("python server.py &")
    h2.cmd("python client.py &")
    h5.cmd("python client.py &")
    h7.cmd("python client.py &")
    h9.cmd("python client.py &")
    time.sleep(10)
    
    #print(h1.cmd(">"))
    print(h2.cmd(">"))
    print(h5.cmd(">"))
    print(h7.cmd(">"))
    print(h9.cmd(">"))

    print("\n\n")
    #h1.cmd("python ts_thread.py &")
    #h2.cmd("python tc.py 1 &")
    #h3.cmd("python tc.py 2 &")
    #h4.cmd("python tc.py 3 &")
    #h5.cmd("python tc.py 4 &")
    #time.sleep(6)
    #print(h1.cmd(">"))
    time.sleep(10)
    #print(h2.cmd(">"))
    #print(h3.cmd(">"))
    #print(h4.cmd(">"))
    #print(h5.cmd(">"))

    CLI(net)
    net.stop()

setLogLevel( 'info' )
myNetwork()
