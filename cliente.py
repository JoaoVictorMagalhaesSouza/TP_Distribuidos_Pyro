import Pyro4
import random


class Cliente:

    def __init__(self, ip):
        ######## Configurações do servidor e da conexão. #####################
        ipAddressServer = ip
        self.connection = Pyro4.core.Proxy(
            'PYRO:Servidor@' + ipAddressServer + ':9090')
        """
            Criei esses atributos abaixo p/ facilitar . auth = authenticated.
        """
        self.authID = ""
        self.authCoins = ""
        self.authNickname = ""
        self.authPassword = ""
        self.authName = ""
        self.authEmail = ""
        self.authIDMochila = ""
        self.authIDAlbum = ""
        ######################################################################

    def start(self):
        print("#################################################################")
        print("#    Olá ! Seja bem vindo ao Programming Language Collection    #")
        print("#    1) Fazer cadastro.                                         #")
        print("#    2) Fazer login.                                            #")
        print("#    3) Sair do sistema.                                        #")
        print("#################################################################")
        print("\n\n")

        escolha = input("Digite a operação: ")
        while (escolha != "3"):
            if (escolha == "1"):
                print(
                    "#################################################################")
                print(
                    "#                   INFORMAÇÕES DE CADASTRO                     #")
                print(
                    "#################################################################")
                nick = input("Digite seu nickname: ")
                senha = input("Digite sua senha: ")
                nome = input("Digite seu nome: ")
                email = input("Digite seu email: ")
                """
                    Agora a gente chama diretamente o método.
                """
                print(self.connection.cadastro(
                    "50000", nick, senha, nome, email))
                print("\n\n")
            elif (escolha == "2"):
                print(
                    "#################################################################")
                print(
                    "#                     INFORMAÇÕES DE LOGIN                      #")
                print(
                    "#################################################################")
                nick = input("Digite seu nickname: ")
                senha = input("Digite sua senha: ")
                # print(self.connection.login(nick,senha))
                """
                        Agora a gente chama diretamente o método.
                    """
                dadosLogin = self.connection.login(nick, senha)
                # print(dadosLogin)
                if (dadosLogin != 0):
                    print("=====> Login efetuado com sucesso !")
                    """
                        Armazenando as informações de login nos atributos da classe. Como se fosse o LocalStorage da WEB.
                    """
                    self.authID = dadosLogin[0]
                    self.authCoins = dadosLogin[1]
                    self.authNickname = dadosLogin[2]
                    self.authPassword = dadosLogin[3]
                    self.authName = dadosLogin[4]
                    self.authEmail = dadosLogin[5]
                    self.authIDMochila = dadosLogin[6]
                    self.authIDAlbum = dadosLogin[7]

                    self.operacoes()
                else:
                    print(
                        "=====> [ERRO] Credenciais de login inválidas! Tente novamente")
                    print("")
                    print("")

            print("#################################################################")
            print("#    Olá ! Seja bem vindo ao Programming Language Collection    #")
            print("#    1) Fazer cadastro.                                         #")
            print("#    2) Fazer login.                                            #")
            print("#    3) Sair do sistema.                                        #")
            print("#################################################################")
            print("\n\n")
            escolha = input("Digite a operação: ")

    def operacoes(self):
        while True:
            print(
                "*****************************************************************")
            print(
                "*    BEM VINDO(A) AO NOSSO GAME!                                *")
            print(
                "*    1) Acessar a Loja.                                         *")
            print(
                "*    2) Inserir Carta da Mochila no Álbum.                      *")
            print(
                "*    3) Visualizar meu Álbum de Figurinhas.                     *")
            print(
                "*    4) Visualizar Cartas na Mochila.                           *")
            print(
                "*    5) Deletar Carta da Mochila.                               *")
            print(
                "*    6) Mover Carta do Álbum para a Mochila.                    *")
            print(
                "*    7) Leiloar/Comprar/Remover uma Carta.                      *")
            print(
                "*    0) Logoff.                                                 *")
            print(
                "*****************************************************************")
            escolha = input("Digite sua escolha: ")
            print("")
            print("")
            if (escolha == "1"):  # Loja
                print("Pacotinhos disponíveis:")
                print("1) 1 carta aleatória = $50 coins.")
                print("2) 3 cartas aleatórias = $135 coins.")
                print("3) 5 cartas aleatórias = $225 coins.")
                self.authCoins = self.connection.showCoins(self.authNickname)
                pacotinho = input(
                    f"Você tem {self.authCoins} coins. Escolha qual opção de pacotinho quer comprar: ")
                print("")
                print("")

                if (int(self.authCoins) < 50):
                    print(
                        "=====> [ERRO] Voce nao tem moedas suficentes!")
                    continue
                elif (pacotinho == "1") and (int(self.authCoins) >= 50):
                    cartaPacote = []
                    # Gerar uma carta de 1 a 30.
                    cartaPacote.append(random.randint(1, 31))
                    print(self.connection.compraCartaLoja(
                        "50", str(self.authIDMochila), str(self.authID), cartaPacote))
                    self.authCoins = int(self.authCoins) - 50
                elif (pacotinho == "2") and (int(self.authCoins) >= 135):
                    cartaPacote = []
                    for i in range(3):
                        cartaPacote.append(random.randint(1, 31))
                    print(self.connection.compraCartaLoja("135", str(
                        self.authIDMochila), str(self.authID), cartaPacote))
                    self.authCoins = int(self.authCoins) - 135
                elif (pacotinho == "3") and (int(self.authCoins) >= 225):
                    cartaPacote = []
                    for i in range(5):
                        cartaPacote.append(random.randint(1, 31))
                    print(self.connection.compraCartaLoja("225", str(
                        self.authIDMochila), str(self.authID), cartaPacote))
                    self.authCoins = int(self.authCoins) - 225
                else:
                    print("=====> [ERRO] Digite uma opção válida !")

                print("")
                print("")

            elif (escolha == "2"):
                respostaCartasMochila = self.connection.minhaMochila(
                    str(self.authIDMochila))
                if (respostaCartasMochila == 0):
                    print(
                        f"=====> Você ainda não possui cartas na mochila !")
                else:
                    # print(respostaCartasMochila)
                    print("=====> Suas cartas na mochila são: ")
                    myCards = respostaCartasMochila
                    j = 0
                    for i in myCards:
                        print(f"{j}) {i}")
                        j += 1

                    escolhaCarta = input(
                        "Digite o nome da carta que você quer inserir no álbum: ")
                    if (escolhaCarta in myCards):
                        print(self.connection.insereAlbum(
                            str(self.authIDMochila), str(self.authIDAlbum), str(escolhaCarta)))
                    else:
                        print(
                            "=====> [ERRO] Digite uma carta que você possui !")
                print("")
                print("")
            elif (escolha == "3"):
                respostaVisualizaAlbum = self.connection.visualizaAlbum(
                    str(self.authIDAlbum))

                if (respostaVisualizaAlbum == 0):
                    print("=====> Voce ainda nao possui cartas no album.")
                else:
                    myAlbum = respostaVisualizaAlbum
                    print(f"=====> As cartas do seu album sao: ")
                    for i in myAlbum:
                        print(f"{i}")
                print("")
                print("")

            elif (escolha == "4"):
                respostaCartasMochila2 = self.connection.minhaMochila(
                    str(self.authIDMochila))
                if (respostaCartasMochila2 == 0):
                    print(
                        f"=====> Você ainda não possui cartas na mochila !")
                else:
                    # print(respostaCartasMochila)
                    print("=====> Suas cartas na mochila são: ")
                    myCards = respostaCartasMochila2
                    j = 0
                    for i in myCards:
                        print(f"{j}) {i}")
                        j += 1

            elif (escolha == "5"):
                carta = input(
                    'Digite o nome da carta: ')
                print('A carta escolhida é:', carta)
                print(self.connection.deletaCarta(
                    carta, str(self.authIDMochila)))
                print("")
                print("")
            elif (escolha == "6"):
                carta = input(
                    'Digite o nome da carta: ')
                print('A carta escolhida é:', carta)
                print(self.connection.retiraCartaAlbum(
                    carta, str(self.authIDMochila), str(self.authIDAlbum)))
                print("")
                print("")
            elif (escolha == "7"):
                print("Bem vindo ao leilão!")
                print("1) Anunciar uma Carta")
                print("2) Comprar/Visualizar Cartas à Venda")
                print("3) Retirar uma carta anunciada.")
                escolhaLeilao = input(
                    "Escolha uma funcionalidade: ")
                # Ver se já possui uma carta anunciada.
                if (escolhaLeilao == "1"):
                    respostaCartasMochila = self.connection.minhaMochila(
                        str(self.authIDMochila))

                    if (respostaCartasMochila == "0"):
                        print("=====> Não ha cartas na mochila!")
                    else:
                        print(f"As cartas que você pode anunciar são: ")
                        respostaCartasMochila = respostaCartasMochila

                        j = 0
                        for i in respostaCartasMochila:
                            print(f"{i}")
                            j += 1

                        cartaAnunciada = input(
                            "Digite o nome da carta a ser anunciada: ")
                        precoCarta = input(
                            "Especifique por quanto deseja leiloar essa carta: ")

                        print(self.connection.colocaCartaLeilao(
                            str(self.authIDMochila), cartaAnunciada, precoCarta))
                    print("")
                    print("")

                elif (escolhaLeilao == "2"):

                    respostaCartasLeilao = self.connection.mostraCartasLeilao()
                    if (respostaCartasLeilao == 0):
                        print("=====> Não há cartas anunciadas no leilao!")
                    else:
                        print("Cartas à venda: ")

                        for i in range(len(respostaCartasLeilao["idVenda"])):
                            print(
                                f""" => ID: {respostaCartasLeilao["idVenda"][i]}    |    Nome do Vendedor: {respostaCartasLeilao["Nome"][i]}   |   Carta: {respostaCartasLeilao["Carta"][i]}   |   Preço: {respostaCartasLeilao["Preco"][i]}""")

                        escolhaComprar = input(
                            "Deseja comprar alguma carta ? 1-Sim | 2-Não :")
                        if (escolhaComprar == "1"):
                            print(
                                f"Você possui {self.authCoins} coins.")
                            cartaDesejada = int(
                                input("Digite o id da compra que contém sua carta de interesse: "))
                            print("A carta desejada é "+respostaCartasLeilao["Carta"][cartaDesejada]+", vendida por "+respostaCartasLeilao["Nome"][cartaDesejada]+" no valor de "+str(
                                respostaCartasLeilao["Preco"][cartaDesejada])+" coins.")
                            if (int(self.authCoins) >= int(respostaCartasLeilao["Preco"][cartaDesejada])):
                                print(self.connection.vendeLeilao(str(self.authIDMochila), str(
                                    respostaCartasLeilao["Nome"][cartaDesejada])))
                            else:
                                print(
                                    "=====> [ERRO] Você não possui moedas suficientes para comprar esta carta.")
                elif (escolhaLeilao == "3"):
                    retiraLeilao = input(
                        "Tem certeza que deseja remover a carta anunciada ? 1 - Sim | Outro - Não: ")

                    if (retiraLeilao == "1"):
                        print(self.connection.retiraCartaLeilao(
                            str(self.authIDMochila)))
                print("\n\n")

            elif (escolha == "0"):
                self.connection.logout()
                break
