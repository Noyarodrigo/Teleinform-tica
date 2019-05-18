#/usr/bin_/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from design import datain


def myNetwork():

    r = {}
    s = {}

    net = Mininet ( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')

    r_central = net.addHost('r_central', cls=Node, ip='')
    r_central.cmd('sysctl -w net.ipv4.ip_forward=1')

    for i in range(1, nivel[0]):

        for j in range(0, nivel[i+1]):

            s["s{}".format(j+1)] = net.addSwitch('s'+(j, cls=OVSKernelSwitch, failMode='standalone')
        
        for j in range(0, nivel[i+1]):

            '#adding routers (hosts)'
            r[r"{}".format(j+1)] = net.addHost('r'+(j+1), cls=Node, ip='')

            #configuracion de host a router
            r["r"+(j+1)].cmd('sysctl -w net.ipv4.ip_forward=1')

            #Endpoints
            """info( '*** Add hosts\n')
            habria que hacerse solo si estas en la ultima iteracion
            h1 = net.addHost('h1', cls=Host, ip='10.0.1.254/24', defaultRoute=None)
            h2 = net.addHost('h2', cls=Host, ip='10.0.2.254/24', defaultRoute=None)
            h3 = net.addHost('h3', cls=Host, ip='10.0.3.254/24', defaultRoute=None)
            h4 = net.addHost('h4', cls=Host, ip='10.0.4.254/24', defaultRoute=None)
            h5 = net.addHost('h5', cls=Host, ip='10.0.5.254/24', defaultRoute=None)
            h6 = net.addHost('h6', cls=Host, ip='10.0.6.254/24', defaultRoute=None)"""

            info( '*** Add links\n')
            #Enlaces r_central >> switchs wan
            net.addLink(r_central, s1_wan, intfName1='r_central-eth0', params1={ 'ip' : '192.168.100.6/29' })
            net.addLink(r_central, s2_wan, intfName1='r_central-eth1', params1={ 'ip' : '192.168.100.14/29' })
            net.addLink(r_central, s3_wan, intfName1='r_central-eth2', params1={ 'ip' : '192.168.100.22/29' })
            net.addLink(r_central, s4_wan, intfName1='r_central-eth3', params1={ 'ip' : '192.168.100.30/29' })
            net.addLink(r_central, s5_wan, intfName1='r_central-eth4', params1={ 'ip' : '192.168.100.38/29' })
            net.addLink(r_central, s6_wan, intfName1='r_central-eth5', params1={ 'ip' : '192.168.100.46/29' })

            #Enlace router sucursal >> switch wan
            net.addLink(r1, s1_wan, intfName1='r1-eth0-wan', params1={ 'ip' : '192.168.100.1/29' })
            net.addLink(r2, s2_wan, intfName1='r2-eth1-wan', params1={ 'ip' : '192.168.100.9/29' })
            net.addLink(r3, s3_wan, intfName1='r3-eth2-wan', params1={ 'ip' : '192.168.100.17/29' })
            net.addLink(r4, s4_wan, intfName1='r4-eth3-wan', params1={ 'ip' : '192.168.100.25/29' })
            net.addLink(r5, s5_wan, intfName1='r5-eth4-wan', params1={ 'ip' : '192.168.100.33/29' })
            net.addLink(r6, s6_wan, intfName1='r6-eth5-wan', params1={ 'ip' : '192.168.100.41/29' })
            
            #Enlace router sucursal >> switch lan
            net.addLink(r1, s1_lan, intfName1='r1-eth0-lan', params1={ 'ip' : '10.0.1.1/24' })
            net.addLink(r2, s2_lan, intfName1='r2-eth1-lan', params1={ 'ip' : '10.0.2.1/24' })
            net.addLink(r3, s3_lan, intfName1='r3-eth2-lan', params1={ 'ip' : '10.0.3.1/24' })
            net.addLink(r4, s4_lan, intfName1='r4-eth3-lan', params1={ 'ip' : '10.0.4.1/24' })
            net.addLink(r5, s5_lan, intfName1='r5-eth4-lan', params1={ 'ip' : '10.0.5.1/24' })
            net.addLink(r6, s6_lan, intfName1='r6-eth5-lan', params1={ 'ip' : '10.0.6.1/24' })

            #Enlace Endpoints con su switch lan
            net.addLink(h1, s1_lan)
            net.addLink(h2, s2_lan)
            net.addLink(h3, s3_lan)
            net.addLink(h4, s4_lan)
            net.addLink(h5, s5_lan)
            net.addLink(h6, s6_lan)
            
            info( '*** Starting network\n')
            net.build()
            info( '*** Starting controllers\n')
            
            #inicio controladores (no hay ahora)
            for controller in net.controllers:
                controller.start()

            info( '*** Starting switches\n')
            net.get('s1_lan').start([])
            net.get('s1_wan').start([])
            net.get('s2_wan').start([])
            net.get('s2_lan').start([])    
            net.get('s3_lan').start([])
            net.get('s3_wan').start([])
            net.get('s4_lan').start([])
            net.get('s4_wan').start([])
            net.get('s5_lan').start([])
            net.get('s5_wan').start([])
            net.get('s6_lan').start([])
            net.get('s6_wan').start([])
            
            #Tablas
            info( '*** Post configure switches and hosts\n')

                #hosts
            net['h1'].cmd('ip route add 0/0 via 10.0.1.1')
            net['h2'].cmd('ip route add 0/0 via 10.0.2.1')
            net['h3'].cmd('ip route add 0/0 via 10.0.3.1')
            net['h4'].cmd('ip route add 0/0 via 10.0.4.1')
            net['h5'].cmd('ip route add 0/0 via 10.0.5.1')
            net['h6'].cmd('ip route add 0/0 via 10.0.6.1')

                #router central >> sucursales 
            net['r_central'].cmd('ip route add 10.0.1.0/24 via 192.168.100.1')
            net['r_central'].cmd('ip route add 10.0.2.0/24 via 192.168.100.9') 
            net['r_central'].cmd('ip route add 10.0.3.0/24 via 192.168.100.17')
            net['r_central'].cmd('ip route add 10.0.4.0/24 via 192.168.100.25')
            net['r_central'].cmd('ip route add 10.0.5.0/24 via 192.168.100.33')
            net['r_central'].cmd('ip route add 10.0.6.0/24 via 192.168.100.41')
                
                #sucursal 1
            net['r1'].cmd('ip route add 192.168.100.9/29 via 192.168.100.6')
            net['r1'].cmd('ip route add 192.168.100.17/29 via 192.168.100.6')
            net['r1'].cmd('ip route add 192.168.100.25/29 via 192.168.100.6')
            net['r1'].cmd('ip route add 192.168.100.33/29 via 192.168.100.6')
            net['r1'].cmd('ip route add 192.168.100.41/29 via 192.168.100.6')
            net['r1'].cmd('ip route add 192.168.100.6/29 via 10.0.1.1')
            net['r1'].cmd('ip route add 10.0.0.0/22 via 192.168.100.6')
            net['r1'].cmd('ip route add 0/0 via 192.168.100.6')

                #sucursal 2
            net['r2'].cmd('ip route add 192.168.100.1/29 via 192.168.100.14')
            net['r2'].cmd('ip route add 192.168.100.17/29 via 192.168.100.14')
            net['r2'].cmd('ip route add 192.168.100.25/29 via 192.168.100.14')
            net['r2'].cmd('ip route add 192.168.100.33/29 via 192.168.100.14')
            net['r2'].cmd('ip route add 192.168.100.41/29 via 192.168.100.14')
            net['r2'].cmd('ip route add 192.168.100.14/29 via 10.0.2.1')
            net['r2'].cmd('ip route add 10.0.0.0/22 via 192.168.100.14')
            net['r2'].cmd('ip route add 0/0 via 192.168.100.14')
            net['r2'].cmd('ip route add 0/0 via 192.168.100.14')

                #sucursal 3
            net['r3'].cmd('ip route add 192.168.100.1/29 via 192.168.100.22')
            net['r3'].cmd('ip route add 192.168.100.9/29 via 192.168.100.22')
            net['r3'].cmd('ip route add 192.168.100.25/29 via 192.168.100.22')
            net['r3'].cmd('ip route add 192.168.100.33/29 via 192.168.100.22')
            net['r3'].cmd('ip route add 192.168.100.41/29 via 192.168.100.22')
            net['r3'].cmd('ip route add 192.168.100.22/29 via 10.0.3.1')
            net['r3'].cmd('ip route add 10.0.0.0/22 via 192.168.100.22')
            net['r3'].cmd('ip route add 0/0 via 192.168.100.22')


                #sucursal 4
            net['r4'].cmd('ip route add 192.168.100.1/29 via 192.168.100.30')
            net['r4'].cmd('ip route add 192.168.100.9/29 via 192.168.100.30')
            net['r4'].cmd('ip route add 192.168.100.17/29 via 192.168.100.30')
            net['r4'].cmd('ip route add 192.168.100.33/29 via 192.168.100.30')
            net['r4'].cmd('ip route add 192.168.100.41/29 via 192.168.100.30')
            net['r4'].cmd('ip route add 192.168.100.30/29 via 10.0.4.1')
            net['r4'].cmd('ip route add 10.0.0.0/22 via 192.168.100.30')
            net['r4'].cmd('ip route add 0/0 via 192.168.100.30')

                #sucursal 5
            net['r5'].cmd('ip route add 192.168.100.1/29 via 192.168.100.38')
            net['r5'].cmd('ip route add 192.168.100.9/29 via 192.168.100.38')
            net['r5'].cmd('ip route add 192.168.100.17/29 via 192.168.100.38')
            net['r5'].cmd('ip route add 192.168.100.25/29 via 192.168.100.38')
            net['r5'].cmd('ip route add 192.168.100.41/29 via 192.168.100.38')
            net['r5'].cmd('ip route add 192.168.100.38/29 via 10.0.5.1')
            net['r5'].cmd('ip route add 10.0.0.0/22 via 192.168.100.38')
            net['r5'].cmd('ip route add 0/0 via 192.168.100.38')

                #sucursal 6 
            net['r6'].cmd('ip route add 192.168.100.1/29 via 192.168.100.46')
            net['r6'].cmd('ip route add 192.168.100.9/29 via 192.168.100.46')
            net['r6'].cmd('ip route add 192.168.100.17/29 via 192.168.100.46')
            net['r6'].cmd('ip route add 192.168.100.25/29 via 192.168.100.46')
            net['r6'].cmd('ip route add 192.168.100.33/29 via 192.168.100.46')
            net['r6'].cmd('ip route add 192.168.100.46/29 via 10.0.6.1')
            net['r6'].cmd('ip route add 10.0.0.0/22 via 192.168.100.46')
            net['r6'].cmd('ip route add 0/0 via 192.168.100.46')

            #terminar las sucursales como la r_central y agregar el 0/0 para si misma
            CLI(net)
            net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    nivel = datain()

    #myNetwork()
