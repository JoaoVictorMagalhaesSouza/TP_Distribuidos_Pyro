import Pyro4
from Pyro4.core import expose
import mysql.connector
from mysql.connector import Error as db_error

class Server:    
    @Pyro4.expose # O expose diz sobre quais as classes, métodos e atributos que podem ser acessados remotamente.
    def startServer(self):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                        database='bd_distribuidos',
                                                        user='root',
                                                        password='JVictor@00')

            if connection.is_connected():
                        
                        cursor = connection.cursor()
                        db_Info = connection.get_server_info()
                        print("Connected to MySQL database... MySQL Server version on ", db_Info)
            
            
            try:
                
                Pyro4.Daemon.serveSimple({          #Definindo as configurações do servidor
                Server: 'Servidor',
                }, host="127.0.0.1", port=9090, ns=False, verbose=True)    
                    
            except:
                return "Erro ao iniciar a conexão do Server."
        except db_error:
                    return("Error while connecting to MySQL", db_error) 
    @Pyro4.expose    
    def soma(self,v1,v2):
        
        return v1+v2

