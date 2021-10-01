import Pyro4
@Pyro4.expose 

class Server:    
    def soma(self):
        
        return "oi"

Pyro4.Daemon.serveSimple({
    Server: 'Servidor',
}, host="127.0.0.1", port=9090, ns=False, verbose=True)