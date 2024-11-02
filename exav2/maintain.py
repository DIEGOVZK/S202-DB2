from neo4j import GraphDatabase
from database import Neo4jDriver


def clear_database(session):
    session.run("MATCH (n) DETACH DELETE n")


def load_mock_data(session, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        queries = file.read().split(';')
        for query in queries:
            query = query.strip()
            if query:
                session.run(query)


def main():
    driver = Neo4jDriver.get_driver()
    session = driver.session()

    clear_database(session)
    load_mock_data(session, 'mock.data.txt')

    session.close()
    driver.close()


if __name__ == "__main__":
    main()
