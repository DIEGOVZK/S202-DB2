from database import Database


class ProductAnalyzer:

    def __init__(self, database: Database):
        self.database = database

    def total_de_vendas_por_dia(self):
        result = self.database.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id": "$cliente_id", "total": {
                "$sum": "$produtos.quantidade"}}},
            {"$group": {"_id": None, "total_sum": {"$sum": "$total"}}}
        ])
        return list(result)[0]['total_sum']

    def produto_mais_vendido(self):
        result = self.database.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id": "$produtos.descricao", "total": {
                "$sum": "$produtos.quantidade"}}},
            {"$sort": {"total": -1}},
            {"$limit": 1},
            {"$project": {"_id": 0, "produto_mais_vendido": "$_id"}}
        ])
        return list(result)[0]['produto_mais_vendido']

    def cliente_gastou_mais(self):
        result = self.database.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id": "$cliente_id", "total_gasto": {
                "$sum": {"$multiply": ["$produtos.quantidade", "$produtos.preco"]}}}},
            {"$sort": {"total_gasto": -1}},
            {"$limit": 1},
            {"$project": {"_id": 0, "cliente_gastou_mais": "$_id"}}
        ])
        return list(result)[0]['cliente_gastou_mais']

    def produtos_vendidos_acima_de_1_unidade(self):
        result = self.database.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$match": {"produtos.quantidade": {"$gt": 1}}},
            {"$group": {"_id": "$produtos.descricao",
                        "quantidade": {"$sum": "$produtos.quantidade"}}},
            {"$project": {"_id": 0, "descricao": "$_id", "quantidade": "$quantidade"}}
        ])
        return list(result)
