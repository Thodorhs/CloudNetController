# CloudNetController
A SDN application on top of POX controller.  Emulating the behaviour of a multi-rooted (mininet) topology acting as a data center of multiple network tenants.

You need mininet to create topologies and pox as a controler with openflow switches. The experiment can be done by pinging from a host to a server.

# Run
place **CloudNetController.py, firewall_policies.csv, migration_events.csv** under **~/home/mininet/pox/ext**

place **clos_topo.py, tcp_receiver.py, tcp_sender.py, udp_receiver.py, udp_sender.py** under **~/home/mininet**

in ~/home/mininet/pox/ext
**./pox.py openflow.discovery CloudNetController --firewall_capability=True --migration_capability=True**

in ~/home/mininet
**sudo mn -c**
**sudo python clos_topo.py -c 2 -f 2**

then **WAIT** for pings to take place (let it finish we need ARPS to learn)

after that ping between hosts or run:

**sudo python udp_receiver.py 10.0.0.8 49160 5**
**sudo python udp_sender.py 10.0.0.8 49160**

between hosts to test UDP or,

**sudo python tcp_receiver.py 10.0.0.8 49160 5**
**sudo python tcp_sender.py 10.0.0.8 49160**

between hosts to test TCP

# Brief explanation
- An tree like topology of openflow switches(core - aggregation - edge) used to move packets.
- Each egde switch haves 2 hosts.
- We calculate (NetworkX package) every shortest path between 2 edge switches and randomly chose one if a host-to-host comunication takes place (diferent paths for UDP/TCP flows).
- Firewall configuration file supported (e.g even-odd id hosts).
- Host migration configuration file supported (e.g h1 after 5 minuites of run time will migrate to h5 for maintanance purposes).

![e.g](https://github.com/Thodorhs/CloudNetController/images/ex.png)
