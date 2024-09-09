from database import Database
from livroModel import LivroModel
from cli import LivroCLI

db = Database(database="livraria", collection="invetario")

livroModel = LivroModel(database=db)

livroCLI = LivroCLI(livro_model=livroModel)
livroCLI.run()
