from database import Database, mklog


class Pokedex:
    '''
    Classe agregada à Database
    Permite instanciação e interação com banco Pokedex
    '''

    def __init__(self, database: Database):
        self.database = database

    def get(self, pokemonName: str):
        pokemonData = self.database.collection.find({"name": pokemonName})
        return mklog(pokemonData, pokemonName)

    def getByWeightRange(self, lightest: float, heaviest: float):
        pokemonData = self.database.collection.find({
            "$expr": {
                "$and": [
                    {"$gte": [
                        {"$convert": {
                            "input": {"$substr": ["$weight", 0, {"$indexOfBytes": ["$weight", " "]}]},
                            "to": "double"
                        }},
                        lightest
                    ]},
                    {"$lte": [
                        {"$convert": {
                            "input": {"$substr": ["$weight", 0, {"$indexOfBytes": ["$weight", " "]}]},
                            "to": "double"
                        }},
                        heaviest
                    ]}
                ]
            }
        })
        return mklog(pokemonData, f"weightRange_{lightest}_{heaviest}")

    def getAllWeakAgainst(self, pokemonName: str):
        pokemonData = self.database.collection.find({"name": pokemonName})
        allWeakAgainst = self.database.collection.find({
            "weaknesses": {
                "$in": pokemonData[0]["type"]
            }
        })
        return mklog(allWeakAgainst, f"weakAgainst_{pokemonName}")

    def getAllStrongAgainst(self, pokemonName: str):
        pokemonData = self.database.collection.find({"name": pokemonName})
        allStrongAgainst = self.database.collection.find({
            "type": {
                "$in": pokemonData[0]["weaknesses"]
            }
        })
        return mklog(allStrongAgainst, f"strongAgainst_{pokemonName}")

    def getImageUrl(self, pokemonName: str):
        pokemonData = self.database.collection.find({"name": pokemonName})
        return mklog(pokemonData, pokemonName)[0]["img"]
