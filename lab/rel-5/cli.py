from livroModel import LivroModel

class SimpleCLI:
    def __init__(self):
        self.commands = {}

    def add_command(self, name, function):
        self.commands[name] = function

    def run(self):
        while True:
            command = input("Enter a command: ")
            if command == "Quit":
                print("Bye!")
                break
            elif command in self.commands:
                self.commands[command]()
            else:
                print("Invalid command. Try again.")

class LivroCLI(SimpleCLI):
    def __init__(self, livro_model: LivroModel):
        super().__init__()
        self.livro_model = livro_model
        self.add_command("Create", self.create_livro)
        self.add_command("Read", self.read_livro)
        self.add_command("Update", self.update_livro)
        self.add_command("Delete", self.delete_livro)

    def create_livro(self):
        titulo = input("Entre com o titulo do livro: ")
        autor = input("Entre com o autor do livro: ")
        ano = int(input("Entre com o ano do livro: "))
        preco = float(input("Entre com o preco do livro: "))
        self.livro_model.create_livro(titulo, autor, ano, preco)

    def read_livro(self):
        id = input("Entre com o id do livro: ")
        livro = self.livro_model.read_livro(id)
        print(f"Titulo: {livro['titulo']}")
        print(f"Autor: {livro['autor']}")
        print(f"Ano: {livro['ano']}")
        print(f"Preco: {livro['preco']}")

    def update_livro(self):
        id = input("Entre com o id do livro: ")
        titulo = input("Entre com o titulo do livro: ")
        autor = input("Entre com o autor do livro: ")
        ano = int(input("Entre com o ano do livro: "))
        preco = float(input("Entre com o preco do livro: "))
        self.livro_model.update_livro(id, titulo, autor, ano, preco)

    def delete_livro(self):
        id = input("Entre com o id do livro: ")
        self.livro_model.delete_livro(id)

    def run(self):
        print("Bem-vindo ao sistema de livros!")
        super().run()
