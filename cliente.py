import Pyro4

class Cliente:

    def __init__(self,ip):        
        ######## Configurações do servidor e da conexão. #####################
        ipAddressServer = ip
        connection = Pyro4.core.Proxy('PYRO:Servidor@' + ipAddressServer + ':9090')
        ######################################################################
        print(connection.soma(1,2))
