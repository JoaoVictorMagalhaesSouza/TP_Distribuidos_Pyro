import Pyro4
from Pyro4.core import expose
import mysql.connector
from mysql.connector import Error as db_error

class Server:    
    
    def __init__(self) :
        try:
            self.connection = mysql.connector.connect(host='localhost',
                                                        database='bd_distribuidos',
                                                        user='root',
                                                        password='JVictor@00')

            if self.connection.is_connected():                        
                        self.cursor = self.connection.cursor()
                        db_Info = self.connection.get_server_info()
                        print("Connected to MySQL database... MySQL Server version on ", db_Info)
        except db_error:
                    return("Error while connecting to MySQL", db_error) 
        
    def startServer(self):
        
            
            
            try:
                
                Pyro4.Daemon.serveSimple({          #Definindo as configurações do servidor
                Server: 'Servidor',
                }, host="127.0.0.1", port=9090, ns=False, verbose=True)    
                """
                    Ele cria um loop de serviço automaticamente.
                """
                    
            except:
                return "Erro ao iniciar a conexão do Server."
        


    ##################### Funcionalidades do sistema ################################
    @Pyro4.expose    #Define as quais classes, métodos e atributos podem ser acessados remotamente.
    def cadastro(self, coins, nickname, password, nome, email):
        try:
            """
                Verificar se essas credenciais já estão no banco:
            """
            queryVerificacao = """SELECT * FROM usuario WHERE (usuario.nickname = '"""+str(
                nickname)+"""');"""
            # print(queryVerificacao)
            #cursor = self.connection.cursor()
            self.cursor.execute(queryVerificacao)
            verificacao = self.cursor.fetchall()
            #print(f"Numero de registros: {len(verificacao)}")
            if (len(verificacao) > 0):
                return("======> [ERRO] Nickname ja existente! Tente outro.")
            else:
                """
                    Primeiramente, criaremos o álbum desse usuário:
                """
                queryCriaAlbum = """INSERT INTO album VALUES();"""
                result = self.cursor.execute(queryCriaAlbum)
                self.connection.commit()
                #print("Query executada")
                #print("==> Álbum criado com sucesso !")
                """
                    Pegando o id do último album inserido
                """

                #cursor = self.connection.cursor()
                self.cursor.execute("SELECT MAX(idAlbum) AS ultimoValor FROM album")
                resultado = self.cursor.fetchall()
                for id in resultado:
                    resultado = id[0]
                """
                    Setando as cartas nos slots respectivos desse usuário
                """
                for i in range(1, 31):
                    queryInsertSlot = """INSERT INTO album_has_slot values (""" + str(
                        resultado)+""","""+str(i)+""","""+str(i)+""",False);"""
                    # print(queryInsertSlot)
                    result = self.cursor.execute(queryInsertSlot)
                    self.connection.commit()
                #print("==> Slots iniciados com sucesso!")
                """
                    Criando a mochila desse usuário
                """
                queryCriaMochila = """INSERT INTO mochila values();"""
                result = self.cursor.execute(queryCriaMochila)
                self.connection.commit()
                #print("==> Mochila criada com sucesso !")
                """
                    Montando a query de inserção do usuário em sino Banco de Dados  :
                """
                query = """INSERT INTO usuario (coins,nickname,password,nome,email,Mochila_idMochila,Album_idAlbum) values (""" + \
                    coins+",'"+nickname+"','"+password+"','"+nome+"','" + \
                        email+"',"+str(resultado)+","+str(resultado)+""");"""
                # print(f"{query}")
                result = self.cursor.execute(query)
                self.connection.commit()
                #print("===> Todas as querys foram executadas")
                return("=====> Cadastro realizado com sucesso !")

        except db_error:
            return("=====> [ERRO NO BANCO] Erro ao realizar o cadastro !")

    @Pyro4.expose
    def login(self, nickname, senha):
        """
            Formato padrão da query de seleção
        """
        query = """SELECT * FROM usuario WHERE (BINARY nickname= '""" + \
            nickname+"'"+" and password='"+senha+"');"
        # print(f"{query}")
        """
            Tentando executar a query de seleção
        """
        try:
            result = self.cursor.execute(query)
            """
                Retorna uma lista com os registros encontrados:
            """
            resultados = self.cursor.fetchall()
            if(len(resultados) > 0):
                """
                    PRÓXIMO PASSO: MANDAR ESSAS INFORMAÇÕES DE LOGIN PARA SEREM CARREGADAS NA NOSSA TELA INICIAL DO GAME
                    PARA PODER CARREGAR O ALBUM DESSE USUÁRIO, SUA MOCHILA E DEMAIS INFORMAÇÕES.
                """
                # print(resultados)
                return(tuple(resultados[0]))
                # return("=====> Login realizado com sucesso !")
            else:
                return(0)
        except db_error:
            return(0)    

    @Pyro4.expose
    def compraCartaLoja(self, coinsRemovidas, idMochila, idUser, cartas):

        # <>loja - -> tipo compra(5 cartas randons) --> tem que criar mochila_has_carta com o id
        # gerado randomicamente, além disso deve retirar a quantidade de coins.
        # <INSERT INTO mochila_has_carta VALUE(resultados[6], random, 1);>
        # <UPDATE usuario SET coins = coins - 25 WHERE idUsuario = resultados[0];>
        try:
            #print(f"Coins: {coinsRemovidas}")
            #print(f"Cartas: {cartas}")
            for i in cartas:  # Avaliar cada carta a ser inserida...
                # Primeiro temos que verificar se a carta já está na mochila
                queryVerificaCartaMochila = """SELECT * FROM mochila_has_carta WHERE (Mochila_idMochila = '"""+str(
                    idMochila)+"' and Carta_idCarta = '"+str(i)+"');"
                #print(f"Q1: {queryVerificaCartaMochila}")
                
                self.cursor.execute(queryVerificaCartaMochila)
                verificacao = self.cursor.fetchall()

                if (len(verificacao) > 0):  # Carta já está na mochila
                    queryInsereMochila = "UPDATE mochila_has_carta SET numero = numero + 1 WHERE (Mochila_idMochila = '"""+str(
                        idMochila)+"' and Carta_idCarta = '"+str(i)+"');"
                else:
                    queryInsereMochila = """INSERT INTO mochila_has_carta VALUES("""+"'"+str(
                        idMochila)+"','"+str(i)+"','1');"
                #print(f"Q2: {queryInsereMochila}")
                result = self.cursor.execute(queryInsereMochila)
                self.connection.commit()
            """
                Remover as coins
            """
            queryRemoveCoins = "UPDATE usuario SET coins = coins -" + \
                coinsRemovidas+" WHERE (idUsuario = '"+idUser+"'); "
            #print(f"Q3: {queryRemoveCoins}")
            result = self.cursor.execute(queryRemoveCoins)
            self.connection.commit()
            return("=====> Cartas compradas com sucesso ! Verifique a mochila. ")

        except db_error:
            return("=====> [ERRO NO BANCO] Erro ao comprar carta!")        
        

    @Pyro4.expose
    def minhaMochila(self, idMochila):
        try:
            queryVisualizaMochila = "SELECT * FROM mochila_has_carta WHERE (Mochila_idMochila = '" + \
                idMochila+"' and numero > 0);"
            #print(f"Q0: {queryVisualizaMochila}")
            #cursor = connection.cursor()
            self.cursor.execute(queryVisualizaMochila)
            verificacao = self.cursor.fetchall()
            cartas = []
            nomeCartas = []
            for i in verificacao:
                cartas.append(i[1])
                #print(i)

            for i in cartas:
                query = "SELECT * FROM carta WHERE (idCarta = '"+str(i)+"');"
                #print(f"Q1: {query}")
                #cursor = connection.cursor()
                self.cursor.execute(query)
                verificacao = self.cursor.fetchall()
                for j in verificacao:
                    nomeCartas.append(j[1])

            #print(f"Cartas que o usuario possui: {nomeCartas}")
            if (len(nomeCartas) == 0):
                return(0)
            else:
                return(nomeCartas)

        except db_error:
            return("=====> [ERRO NO BANCO] Erro ao visualizar dados da mochila do usuário.")
    @Pyro4.expose
    def insereAlbum(self, idMochila, idAlbum, nomeCarta):
        try:

            """
                Primeiro tirar a carta da mochila.
            """
            queryIdentificacao = "SELECT * FROM carta WHERE (nome = '" + \
                nomeCarta+"');"
            #cursor = connection.cursor()
            self.cursor.execute(queryIdentificacao)
            verificacao = self.cursor.fetchall()

            for i in verificacao:
                idCarta = i[0]
            queryRemocao = "UPDATE mochila_has_carta SET numero = numero - 1 WHERE (Mochila_idMochila = '"""+str(
                idMochila)+"' and Carta_idCarta = '"+str(idCarta)+"');"
            #print(f"QR {queryRemocao}")
            result = self.cursor.execute(queryRemocao)
            self.connection.commit()

            """
                Verificar se a carta já está lá
            """
            queryVerificaAlbum = "SELECT * FROM album_has_slot WHERE (Album_idAlbum = '"+str(
                idAlbum)+"' and Slot_Carta_idCarta = '"+str(idCarta)+"' and is_ocupado = 0);"
            #print(f"QV {queryVerificaAlbum}")
            #cursor = connection.cursor()
            self.cursor.execute(queryVerificaAlbum)
            verificacao = self.cursor.fetchall()

            # print(len(verificacao))
            if (len(verificacao) == 1):  # Significa que a carta ainda não está no Album
                queryAdicionaAlbum = "UPDATE album_has_slot SET is_ocupado = 1 WHERE (Album_idAlbum = '"+str(
                    idAlbum)+"' and Slot_Carta_idCarta = '"+str(idCarta)+"');"
                result = self.cursor.execute(queryAdicionaAlbum)
                self.connection.commit()
                return("=====> Carta inserida no album com sucesso!")
            else:  # Siginifica que a carta já está no album
                return("=====> [ERRO] Carta ja esta no album.")
        except db_error:
            return("=====> [ERRO NO BANCO] Erro ao inserir carta no album.")
    @Pyro4.expose
    def visualizaAlbum(self, idAlbum):
        try:
            # Mostrar somente as cartas que ele colocou no álbum.
            queryVisualizaAlbum = "SELECT * FROM album_has_slot WHERE (Album_idAlbum = '" + \
                idAlbum+"' and is_ocupado=1);"
            #cursor = connection.cursor()
            self.cursor.execute(queryVisualizaAlbum)
            verificacao = self.cursor.fetchall()
            cartas = []
            nomeCartas = []
            if (len(verificacao) == 0):
                return(0)
            else:
                for i in verificacao:
                    cartas.append(i[2])
                for i in cartas:
                    query = "SELECT * FROM carta WHERE (idCarta = '" + \
                        str(i)+"');"
                    print(f"Q1: {query}")
                    #cursor = connection.cursor()
                    self.cursor.execute(query)
                    verificacao = self.cursor.fetchall()
                    for j in verificacao:
                        nomeCartas.append(j[1])
                return(nomeCartas)

        except db_error:
            return("=====> [ERRO NO BANCO] Nao foi possivel exibir o album.")