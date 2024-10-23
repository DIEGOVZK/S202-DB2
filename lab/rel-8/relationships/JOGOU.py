class Jogou:
    def __init__(self, tempo, creditos):
        self.tempo = tempo
        self.creditos = creditos

    def dict(self):
        return {
            "tempo": self.tempo,
            "creditos": self.creditos
        }

    def create(self, session, Jogador, Partida):
        session.run(
            "MATCH (j:Jogador {nome: $nome}) MATCH (p:Partida {local: $local}) CREATE (j)-[:Jogou {tempo: $tempo, creditos: $creditos}]->(p)",
            nome=Jogador.nome, local=Partida.local, tempo=self.tempo, creditos=self.creditos
        )
