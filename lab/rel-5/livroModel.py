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
