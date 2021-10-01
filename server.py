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
    
    @Pyro4.expose
    def deletaCarta(self, nomeCarta, idMochila):
        # <>deletar carta
        # <UPDATE mochila_has_carta SET numero = numero - 1 WHERE Mochila_idMochila = resultados[6]>
        #print(f'Nome da carta é {nomeCarta}')
        queryExisteCarta = f"SELECT idCarta FROM Carta WHERE nome = '{nomeCarta.strip()}';"
        #cursor = connection.cursor()
        self.cursor.execute(queryExisteCarta)
        verificacao = self.cursor.fetchall()
        # return verificacao

        if len(verificacao) > 0:  # a carta passada (nome) é válida
            try:
                # verificar se ele possui um mochila_has_carta para essa carta.
                idCarta = verificacao[0][0]
                queryPossuiCarta = f"SELECT numero FROM Mochila_has_Carta WHERE Mochila_idMochila = '{idMochila}' and Carta_idCarta = '{idCarta}';"
                #cursor = connection.cursor()
                self.cursor.execute(queryPossuiCarta)
                verificacao = self.cursor.fetchall()
                if len(verificacao) > 0:
                    numero = verificacao[0][0]
                    # print('O numero é', numero)
                    if numero > 0:
                        # signiifica que ele tem a carta.
                        queryDecrementaNumero = f"UPDATE Mochila_has_Carta SET numero = numero - 1 WHERE Mochila_idMochila = '{idMochila}' and Carta_idCarta = '{idCarta}';"
                        self.cursor.execute(queryDecrementaNumero)
                        self.connection.commit()
                        return (f"=====> Uma carta de ({nomeCarta}) cujo id eh {idCarta} deleta com sucesso!")
                    else:
                        return("=====> [ERRO] Voce nao tem nenhuma carta dessas!")
                else:
                    return("=====> [ERRO] Você nao tem nenhuma carta dessas!")
            except db_error:
                return("=====> [ERRO NO BANCO] Erro na delecao da carta")
    @Pyro4.expose
    def retiraCartaAlbum(self, nomeCarta, idMochila, idAlbum):
        # <>retirar carta do album --> incremnta do mochila_has_carta e faz is_ocupado ser 0
        # SELECT is_ocupado FROM Album_has_Slot WHERE Album_idAlbum = 1 and Slot_Carta_idCarta = x;
        # SELECT idCarta FROM Carta WHERE nome = {nomeCarta};
        #print(f'Nome da carta é {nomeCarta}')
        queryExisteCarta = f"SELECT idCarta FROM Carta WHERE nome = '{nomeCarta.strip()}';"

        #cursor = connection.cursor()
        self.cursor.execute(queryExisteCarta)
        verificacao = self.cursor.fetchall()
        # return verificacao

        if len(verificacao) > 0:  # a carta passada (nome) é válida
            try:
                idCarta = verificacao[0][0]
                # print('O id da carta é', idCarta)  # certo
                queryExisteSlotOcupado = f"SELECT is_ocupado FROM Album_has_Slot WHERE Album_idAlbum = '{idAlbum}' and Slot_Carta_idCarta = '{idCarta}';"
                #cursor = connection.cursor()
                self.cursor.execute(queryExisteSlotOcupado)
                verificacao = self.cursor.fetchall()  # verificação indica se usuário tem a carta como 1
                if (verificacao[0][0] == 1):
                    #print('Eu tenho essa carta!')
                    queryRetiraAlbum = f"UPDATE Album_has_Slot SET is_ocupado = 0 WHERE Album_idAlbum = '{idAlbum}' and Slot_Carta_idCarta = '{idCarta}';"
                    self.cursor.execute(queryRetiraAlbum)
                    self.connection.commit()

                    queryAdicionaMochila = f"UPDATE Mochila_has_Carta SET numero = numero + 1 WHERE Mochila_idMochila = '{idMochila}' and Carta_idCarta = '{idCarta}';"
                    self.cursor.execute(queryAdicionaMochila)
                    self.connection.commit()
                    return (f"=====> Carta {nomeCarta} de id {idCarta} retirada com sucesso!")
                    # OBS: essa função considera que para o usuário, o Mochila_has_Carta vai
                    # existir. Assim, o atributo "numero" é pelo menos 0.
                else:
                    return('=====> [ERRO] Você nao tem essa carta!')
            except db_error:
                return("=====> [ERRO NO BANCO]Erro ao retirar carta do album")
        else:
            return('=====> [ERRO] Essa carta nao existe!')
    
    @Pyro4.expose
    def colocaCartaLeilao(self, idMochila, carta, precoCarta):
        try:
            """
                Primeiro vamos verificar se o usuario já possui cartas no leilão, pois ele só pode anunciar 1 carta por vez.
            """
            queryVerificaLeilao = "SELECT * FROM leilao WHERE (Mochila_has_Carta_Mochila_idMochila = '"+str(
                idMochila)+"');"
            #cursor = connection.cursor()
            self.cursor.execute(queryVerificaLeilao)
            verificacao = self.cursor.fetchall()
            if (len(verificacao) > 0):  # Significa que o usuário já possui carta no leilão
                carta = []
                nomeCarta = ""
                for i in verificacao:
                    carta.append(i[2])
                for i in carta:
                    query = "SELECT * FROM carta WHERE (idCarta = '" + \
                        str(i)+"');"
                    #print(f"Q1: {query}")
                    #cursor = connection.cursor()
                    self.cursor.execute(query)
                    verificacao = self.cursor.fetchall()
                    for j in verificacao:
                        nomeCarta = (j[1])
                return(f"=====> [ERRO] Voce ja possui uma carta anunciada: {nomeCarta}")
            else:
                """
                    Criar o leilão para aquele user.
                """
                """
                    Primeiro pesquisar o id da carta a ser leiloada
                """
                queryIdCarta = "SELECT idCarta FROM carta WHERE (nome = '"+str(
                    carta)+"');"
                #print(f"Q2: {queryIdCarta}")
                #cursor = connection.cursor()
                self.cursor.execute(queryIdCarta)
                verificacao = self.cursor.fetchall()
                for i in verificacao:
                    idCarta = verificacao[0]
                novo = []
                for x in idCarta:
                    idCarta = str(x)
                # print(f"{idCarta}")
                queryCriaLeilao = "INSERT INTO leilao (Mochila_has_Carta_Mochila_idMochila,Mochila_has_Carta_Carta_idCarta,precoCarta) VALUES ('"+str(
                    idMochila)+"','"+str(idCarta)+"','"+str(precoCarta)+"');"
                #print(f"Q3: {queryCriaLeilao}")
                result = self.cursor.execute(queryCriaLeilao)
                self.connection.commit()
                """
                    Carta inserida no leilão, remover da mochila.
                """
                queryRemocao = "UPDATE mochila_has_carta SET numero = numero - 1 WHERE (Mochila_idMochila = '"""+str(
                    idMochila)+"' and Carta_idCarta = '"+str(idCarta)+"');"
                #print(f"Q4: {queryRemocao}")
                result = self.cursor.execute(queryRemocao)
                self.connection.commit()
                return("=====> Carta leiloada com sucesso. ")
        except db_error:
            return("=====> [ERRO NO BANCO]Erro ao anunciar carta no leilao!")
    
    @Pyro4.expose
    def mostraCartasLeilao(self):
        try:
            queryMostraCartas = "SELECT * FROM leilao;"
            #print(f"Q2: {queryMostraCartas}")
            #cursor = connection.cursor()
            self.cursor.execute(queryMostraCartas)
            verificacao = self.cursor.fetchall()
            dados = {}
            nomeCarta = []
            nomeAnunciante = []
            precoCarta = []
            ids = []
            if(len(verificacao)==0):
                return(0)
            else:

                for i in verificacao:
                    # idMochila.append(i[1])
                    aux = i[1]  # Qual o usuario ?
                    query1 = "SELECT * FROM usuario WHERE (Mochila_idMochila = '"+str(
                        i[1])+"');"
                    #cursor = self.connection.cursor()
                    self.cursor.execute(query1)
                    verificacao2 = self.cursor.fetchall()
                    for j in verificacao2:
                        nomeAnunciante.append(j[2])

                    query2 = "SELECT * FROM carta WHERE (idCarta = '" + \
                        str(i[2])+"');"
                   # cursor = connection.cursor()
                    self.cursor.execute(query2)
                    verificacao3 = self.cursor.fetchall()
                    for j in verificacao3:
                        nomeCarta.append(j[1])

                    precoCarta.append(i[3])
                for i in range(len(verificacao)):
                    ids.append(i)
            dados["idVenda"] = ids
            dados["Nome"] = nomeAnunciante
            dados["Carta"] = nomeCarta
            dados["Preco"] = precoCarta
            return(dados)
        except db_error:
            return("=====> [ERRO NO BANCO] Erro ao mostrar cartas leiloadas.")

    @Pyro4.expose
    def vendeLeilao(self, idMochilaComprador, nicknameVendedor):
        try:
            """
                Obter informações do vendedor.
            """
            queryIDVendedor = "SELECT * FROM usuario WHERE (nickname = '" + \
                nicknameVendedor+"');"
            #cursor = connection.cursor()
            self.cursor.execute(queryIDVendedor)
            verificacao = self.cursor.fetchall()
            for i in verificacao:
                idVendedor = i[0]  # Nickname único
                mochilaVendedor = i[6]

            """
                Obter informações sobre a carta a ser comprada.
            """
            queryInfoCarta = "SELECT * FROM leilao WHERE (Mochila_has_Carta_Mochila_idMochila = '"+str(
                mochilaVendedor)+"');"
            #cursor = connection.cursor()
            self.cursor.execute(queryInfoCarta)
            verificacao = self.cursor.fetchall()
            for i in verificacao:
                precoCarta = i[3]
                idCarta = i[2]

            """
                Removendo do leilão 
            """
            queryDeletaLeilao = "DELETE FROM leilao WHERE (Mochila_has_Carta_Mochila_idMochila = '"+str(
                mochilaVendedor)+"');"
            result = self.cursor.execute(queryDeletaLeilao)
            self.connection.commit()
            """
                Inserindo a carta na mochila do comprador e debitando as coins dele
            """
            queryVerificaCarta = "SELECT * FROM mochila_has_carta WHERE (Mochila_idMochila = '"+str(
                idMochilaComprador)+"' and Carta_idCarta = '"+str(idCarta)+"');"
            #cursor = connection.cursor()
            self.cursor.execute(queryVerificaCarta)
            verificacao = self.cursor.fetchall()
            if (len(verificacao) > 0):  # Significa que eu tenho a carta
                queryInsertCarta = "UPDATE mochila_has_carta SET numero = numero + 1 WHERE (Mochila_idMochila = '"""+str(
                    idMochilaComprador)+"' and Carta_idCarta = '"+str(idCarta)+"');"
                result = self.cursor.execute(queryInsertCarta)
                self.connection.commit()
            else:
                queryInsertCarta = "INSERT INTO mochila_has_carta VALUES ('"+str(
                    idMochilaComprador)+"','"+str(idCarta)+"',1);"
                result = self.cursor.execute(queryInsertCarta)
                self.connection.commit()

            queryTiraCoins = "UPDATE usuario SET coins = coins - " + \
                str(precoCarta)+" WHERE (Mochila_idMochila = '" + \
                str(idMochilaComprador)+"');"
            result = self.cursor.execute(queryTiraCoins)
            self.connection.commit()

            """
                Inserindo as coins no vendedor
            """
            queryInsereCoins = "UPDATE usuario SET coins = coins + " + \
                str(precoCarta)+" WHERE (Mochila_idMochila = '" + \
                str(mochilaVendedor)+"');"
            result = self.cursor.execute(queryInsereCoins)
            self.connection.commit()
            return ("=====> Compra realizada com sucesso !")

        except db_error:
            return ("=====> [ERRO NO BANCO] Erro na transferencia entre as cartas.")
    
    @Pyro4.expose
    def retiraCartaLeilao(self, idMochila):
        try:
            queryBusca = f"SELECT * FROM leilao WHERE ( Mochila_has_Carta_Mochila_idMochila = '{idMochila}');"

            #cursor = connection.cursor()
            self.cursor.execute(queryBusca)
            verificacao = self.cursor.fetchall()
            for i in verificacao:
                idCarta = i[2]

            if (len(verificacao) > 0):  # Usuario possui carta no leilao
                queryTiraLeilao = f"DELETE FROM leilao WHERE ( Mochila_has_Carta_Mochila_idMochila = '{idMochila}');"
                result = self.cursor.execute(queryTiraLeilao)
                self.connection.commit()
                queryInsereIV = f"UPDATE mochila_has_carta SET numero = numero + 1 WHERE (Mochila_idMochila = '{idMochila}' and Carta_idCarta = '{idCarta}');"
                result = self.cursor.execute(queryInsereIV)
                self.connection.commit()
                return("=====> Carta removida do leilao com sucesso !")
            else:
                return("=====> [ERRO] Voce nao possui carta para retirar !")

        except db_error:
            return ("=====> [ERRO NO BANCO] Erro ao carregar carta leiloada.")