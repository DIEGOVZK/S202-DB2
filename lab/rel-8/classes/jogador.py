class Jogador:
    def __init__(self, nome, idade, origem):
        self.nome = nome
        self.idade = idade
        self.origem = origem

    def dict(self):
        return {
            "nome": self.nome,
            "idade": self.idade,
            "origem": self.origem
        }

    def create(self, session):
        session.run(
            "CREATE (j:Jogador {nome: $nome, idade: $idade, origem: $origem})",
            nome=self.nome, idade=self.idade, origem=self.origem
        )

    def read(self, session):
        result = session.run(
            "MATCH (j:Jogador {nome: $nome}) RETURN j",
            nome=self.nome
        ).single()

        self.idade = result["j"]["idade"]
        self.origem = result["j"]["origem"]
        print(f"Nome: {self.nome}, Idade: {self.idade}, Origem: {self.origem}")

    def update(self, session):
        session.run(
            "MATCH (j:Jogador {nome: $nome}) SET j.idade = $idade, j.origem = $origem",
            nome=self.nome, idade=self.idade, origem=self.origem
        )

    def delete(self, session):
        session.run(
            "MATCH (j:Jogador {nome: $nome}) DELETE j",
            nome=self.nome
        )
