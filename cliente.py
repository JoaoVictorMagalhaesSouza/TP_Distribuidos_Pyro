import Pyro4

ipAddressServer = "127.0.0.1"
teste = Pyro4.core.Proxy('PYRO:Servidor@' + ipAddressServer + ':9090')
print(teste.soma())
