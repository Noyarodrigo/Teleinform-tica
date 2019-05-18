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
    sh = {}
    h = {}
    y = 6
    x = 1
    c = 0
    f = ''
    net = Mininet ( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    
    #r00 >>>> r_central
    r_central = net.addHost('r_central', cls=Node, ip='')
    r_central.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    #agregar switchs lan/wan sin distincion
    for i in range(0, nivel[0]):
        for j in range(0, nivel[i+1]):
            f = "{}{}".format(i+1, j+1) 
            s["s{}".format(f)] = net.addSwitch("s{}".format(f), cls=OVSKernelSwitch, failMode='standalone')

    #agregar switchs últimos para host
    for j in range(0, nivel[i+1]):
        sh["sh{}".format(j+1)] = net.addSwitch("sh{}".format(j+1), cls=OVSKernelSwitch, failMode='standalone')

    #agregar router y conexion con la etapa anterior, agregar endpoints (hosts)
    for i in range(0, nivel[0]):
        for j in range(0, nivel[i+1]):
            f = "{}{}".format(i+1, j+1) 
            #se agrega el host para router
            r[r"{}".format(f)] = net.addHost('r'+f, cls=Node, ip='')
            #configuracion de host a router
            r["r{}".format(f)].cmd('sysctl -w net.ipv4.ip_forward=1')
            #Enlaces
            if i == 0:
                #Enlaces r_central >> switchs wan
                net.addLink(r_central, "s{}".format(f), intfName1='r_central-eth'+f, params1={ 'ip' : '192.168.100.'+y+'/29' })
                y += 8
            elif i == (nivel[0]-1):
                #Endpoints
                h["h{}".format(j+1)] = net.addHost('h'+(j+1), cls=Host, ip='10.0.'+(j+1)+'.254/24', defaultRoute=None)
                #Enlace last switch con el ult router
                net.addLink("r{}".format(f), "sh{}".format(j+1), intfName1='r'+f+'-eth0-wan', params1={ 'ip' : '192.168.100.'+x+'/29' })
                #Enlace Endpoints con su switch lan
                net.addLink("h{}".format(j+1), "sh{}".format(j+1))
            else:
                #Enlace router sucursal >> switch wan
                net.addLink("r{}".format(f), "s{}".format(f), intfName1='r'+f+'-eth0-wan', params1={ 'ip' : '192.168.100.'+x+'/29' })
                x =+ 8
    
    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')

    #inicio controladores (no hay ahora)
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    for switch in s:
        net.get(switch).start([])
    
    for switchh in sh:
        net.get(switchh).start([])

    #hosts
    for host in h:
        c += 1
        net[host].cmd('ip route add 0/0 via 10.0.'+c+'.1')

#habria que hacer el for para las tablas, la cantidad de iteraciones deberia estar en la longitud de los diccionarios r o ver de donde 
    #router central >> sucursales 
    net['r_central'].cmd('ip route add 10.0.1.0/24 via 192.168.100.1')


if __name__ == '__main__':
    setLogLevel( 'info' )
    nivel = datain()

    #myNetwork()
