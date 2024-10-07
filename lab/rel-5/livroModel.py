from bson.objectid import ObjectId
from database import Database
from functools import wraps


def tryCatchAbstract(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    return wrapper


class LivroModel:
    def __init__(self, database: Database):
        self.collection = database.collection

    @tryCatchAbstract
    def create_livro(self, titulo: str, autor: str, ano: int, preco: float):
        livro = {
            "titulo": titulo,
            "autor": autor,
            "ano": ano,
            "preco": preco
        }
        result = self.collection.insert_one(livro)
        return result.inserted_id

    @tryCatchAbstract
    def read_livro(self, id: str):
        livro = self.collection.find_one({"_id": ObjectId(id)})
        return livro

    @tryCatchAbstract
    def update_livro(self, id: str, titulo: str, autor: str, ano: int, preco: float):
        livro = {
            "titulo": titulo,
            "autor": autor,
            "ano": ano,
            "preco": preco
        }
        result = self.collection.update_one(
            {"_id": ObjectId(id)}, {"$set": livro})
        return result.modified_count

    @tryCatchAbstract
    def delete_livro(self, id: str):
        result = self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count

from neo4j import GraphDatabase

class PageDAO:

    def __init__(self) -> None:
        self.neo4j_driver = Neo4jDriver.get_driver()

    @tryCatchAbstract
    def add_page(self, page: Page):
        page_dict = page.to_dict()
        professions = page_dict.pop('professions', [])
        cultures = page_dict.pop('cultures', [])
        
        with self.neo4j_driver.session() as session:
            # Create the page node
            session.run(
                "CREATE (p:Page {id: $id, title: $title, content: $content})",
                id=page_dict['id'], title=page_dict['title'], content=page_dict['content']
            )
            
            # Create relationships with professions
            for profession in professions:
                session.run(
                    """
                    MATCH (p:Page {id: $page_id}), (pr:Profession {name: $profession_name})
                    CREATE (p)-[:KNOWN_BY_PROFESSION]->(pr)
                    """,
                    page_id=page_dict['id'], profession_name=profession
                )
            
            # Create relationships with cultures
            for culture in cultures:
                session.run(
                    """
                    MATCH (p:Page {id: $page_id}), (c:Culture {name: $culture_name})
                    CREATE (p)-[:KNOWN_BY_CULTURE]->(c)
                    """,
                    page_id=page_dict['id'], culture_name=culture
                )

class CharacterDAO:

    def __init__(self) -> None:
        self.neo4j_driver = Neo4jDriver.get_driver()

    @tryCatchAbstract
    def add_character(self, character: Character):
        character_dict = character.to_dict()
        known_pages = character_dict.pop('known_pages', [])
        
        with self.neo4j_driver.session() as session:
            # Create the character node
            session.run(
                "CREATE (c:Character {id: $id, name: $name, profession: $profession, culture: $culture})",
                id=character_dict['id'], name=character_dict['name'], profession=character_dict['profession'], culture=character_dict['culture']
            )
            
            # Create relationships with known pages
            for page_id in known_pages:
                session.run(
                    """
                    MATCH (c:Character {id: $character_id}), (p:Page {id: $page_id})
                    CREATE (c)-[:KNOWS_PAGE]->(p)
                    """,
                    character_id=character_dict['id'], page_id=page_id
                )

from neo4j import GraphDatabase

class CharacterDAO:

    def __init__(self) -> None:
        self.neo4j_driver = Neo4jDriver.get_driver()

    @tryCatchAbstract
    def add_character(self, character: Character):
        character_dict = character.to_dict()
        known_pages = character_dict.pop('known_pages', [])
        
        with self.neo4j_driver.session() as session:
            # Create the character node
            session.run(
                "CREATE (c:Character {id: $id, name: $name, profession: $profession, culture: $culture})",
                id=character_dict['id'], name=character_dict['name'], profession=character_dict['profession'], culture=character_dict['culture']
            )
            
            # Create relationships with known pages
            for page_id in known_pages:
                session.run(
                    """
                    MATCH (c:Character {id: $character_id}), (p:Page {id: $page_id})
                    CREATE (c)-[:KNOWS_PAGE]->(p)
                    """,
                    character_id=character_dict['id'], page_id=page_id
                )

    @tryCatchAbstract
    def get_knowledge(self, character_name):
        # -------------- Questão 2 C -------------- #
        query = """
        MATCH (c:Character {name: $character_name})-[:KNOWS_PAGE]->(p:Page)
        RETURN p.id AS id, p.title AS title, p.content AS content
        """
        result = self.neo4j_driver.session().run(query, character_name=character_name)
        pages = []
        for record in result:
            pages.append({
                "id": record["id"],
                "title": record["title"],
                "content": record["content"]
            })
        return pages