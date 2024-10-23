from services import Neo4jDriver
from classes.jogador import Jogador
from classes.partida import Partida
from relationships.JOGOU import Jogou

neo4jd = Neo4jDriver.get_driver()

while True:
    print("\n", "-" * 10)
    print("1. Create Jogador")
    print("2. Read Jogador")
    print("3. Update Jogador")
    print("4. Delete Jogador")
    print("-" * 10)
    print("5. Create Partida")
    print("6. Read Partida")
    print("7. Update Partida")
    print("8. Delete Partida")
    print("-" * 10)
    print("9. Relacionar Jogador com Partida")
    print("-" * 10)
    print("x. Sair")
    print("-" * 10)

    choice = input("Selecione (1-9): ")

    if choice == '1':
        nome = input("Entre com o nome do Jogador: ")
        idade = input("Entre com a idade do Jogador: ")
        origem = input("Entre com a origem do Jogador: ")

        player = Jogador(nome, idade, origem)
        player.create(neo4jd.session())

    elif choice == '2':
        nome = input("Entre com o nome do Jogador: ")

        player = Jogador(nome, None, None)
        player.read(neo4jd.session())

    elif choice == '3':
        nome = input("Entre com o nome do Jogador: ")
        idade = input("Entre com a idade do Jogador: ")
        origem = input("Entre com a origem do Jogador: ")

        player = Jogador(nome, idade, origem)
        player.update(neo4jd.session())

    elif choice == '4':
        nome = input("Entre com o nome do Jogador: ")

        player = Jogador(nome, None, None)
        player.delete(neo4jd.session())

    elif choice == '5':
        local = input("Entre com o local da Partida: ")
        tipo = input("Entre com o tipo da Partida: ")
        t2c = input("Entre com o tempo até destruição: ")
        jurisdicao = input("Entre com o setor em jurisdicao da Partida: ")

        match = Partida(local, tipo, t2c, jurisdicao)
        match.create(neo4jd.session())

    elif choice == '6':
        local = input("Entre com o local da Partida: ")

        match = Partida(local, None, None, None)
        match.read(neo4jd.session())

    elif choice == '7':
        local = input("Entre com o local da Partida: ")
        tipo = input("Entre com o tipo da Partida: ")
        t2c = input("Entre com o tempo até destruição: ")
        jurisdicao = input("Entre com o setor em jurisdicao da Partida: ")

        match = Partida(local, tipo, t2c, jurisdicao)
        match.update(neo4jd.session())

    elif choice == '8':
        local = input("Entre com o local da Partida: ")

        match = Partida(local, None, None, None)
        match.delete(neo4jd.session())
    
    elif choice == '9':
        nome = input("Entre com o nome do Jogador: ")
        local = input("Entre com o local da Partida: ")
        tempo = input("Entre com o tempo de jogo: ")
        creditos = input("Entre com a quantidade de créditos: ")

        player = Jogador(nome, None, None)
        match = Partida(local, None, None, None)
        jogou = Jogou(tempo, creditos)
        jogou.create(neo4jd.session(), player, match)

    elif choice == 'x':
        break

    else:
        print("Entrada inválida, tente novamente.")
