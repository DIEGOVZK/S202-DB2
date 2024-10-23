class Partida:
    def __init__(self, local, tipo, t2c, jurisdicao):
        self.local = local
        self.tipo = tipo
        self.t2c = t2c
        self.jurisdicao = jurisdicao

    def dict(self):
        return {
            "local": self.local,
            "tipo": self.tipo,
            "t2c": self.t2c,
            "jurisdicao": self.jurisdicao
        }

    def create(self, session):
        session.run(
            "CREATE (p:Partida {local: $local, tipo: $tipo, t2c: $t2c, jurisdicao: $jurisdicao})",
            local=self.local, tipo=self.tipo, t2c=self.t2c, jurisdicao=self.jurisdicao
        )

    def read(self, session):
        result = session.run(
            "MATCH (p:Partida {id: $id}) RETURN p",
            id=self.id
        ).single()

        self.data = result["p"]["data"]
        self.jogador_ids = result["p"]["jogador_ids"]
        print(f"ID: {self.id}, Data: {self.data}, Jogador IDs: {', '.join(self.jogador_ids)}")


    def update(self, session):
        session.run(
            "MATCH (p:Partida {local: $local}) SET p.tipo = $tipo, p.t2c = $t2c, p.jurisdicao = $jurisdicao",
            local=self.local, tipo=self.tipo, t2c=self.t2c, jurisdicao=self.jurisdicao
        )

    def delete(self, session):
        session.run(
            "MATCH (p:Partida {local: $local}) DELETE p",
            local=self.local
        )
