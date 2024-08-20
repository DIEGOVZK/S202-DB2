from pokedex import Pokedex
from database import Database
import requests

database = Database("rel-3", "pokedex")
database.resetDatabase()
pokedex = Pokedex(database)

pidgeotto = pokedex.get("Pidgeotto")
heavyPokemons = pokedex.getByWeightRange(100, 200)
allweakagainst = pokedex.getAllWeakAgainst(pidgeotto[0]["name"])
allstrongagainst = pokedex.getAllStrongAgainst(pidgeotto[0]["name"])
imageUrl = pokedex.getImageUrl("Caterpie")

pokemonImage = requests.get(imageUrl).content
with open(f"./logs/imageFrom_Caterpie.png", "wb") as image:
    image.write(pokemonImage)
