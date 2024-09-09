from pymongo import MongoClient
from bson.objectid import ObjectId
from functools import wraps


def tryCatchAbstract(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)


class LivroModel:
    def __init__(self):
        self.database

    @tryCatchAbstract
    def create_livro(self, titulo: str, autor: str, ano: int, preco: float):
        livro = {
            "titulo": titulo,
            "autor": autor,
            "ano": ano,
            "preco": preco
        }
        result = self.database.insert_one(livro)
        return result.inserted_id

    @tryCatchAbstract
    def read_livro(self, id: str):
        livro = self.database.find_one({"_id": ObjectId(id)})
        return livro

    def update_livro(self, id: str, titulo: str, autor: str, ano: int, preco: float):
        livro = {
            "titulo": titulo,
            "autor": autor,
            "ano": ano,
            "preco": preco
        }
        result = self.database.update_one(
            {"_id": ObjectId(id)}, {"$set": livro})
        return result.modified_count

    def delete_livro(self, id: str):
        result = self.database.delete_one({"_id": ObjectId(id)})
        return result.deleted_count
