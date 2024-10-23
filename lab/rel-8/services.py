from neo4j import GraphDatabase

class Neo4jDriver:
    neo4j_host = "neo4j://localhost:7687"
    neo4j_password = "1234567890"
    neo4j_user = "neo4j"

    driver = None

    @staticmethod
    def get_driver():
        if not Neo4jDriver.driver:
            Neo4jDriver.driver = GraphDatabase.driver(Neo4jDriver.neo4j_host, auth=(
                Neo4jDriver.neo4j_user, Neo4jDriver.neo4j_password))
        return Neo4jDriver.driver


'''
jogadores - DISPOE -> vidas
jogadores - POSSUI -> recursos
jogadores - JOGOU -> partidas

'''
