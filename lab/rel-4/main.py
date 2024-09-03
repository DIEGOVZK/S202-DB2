from database import Database
from ProductAnalyzer import ProductAnalyzer

db = Database(database="mercado", collection="compras")
db.resetDatabase()

pa = ProductAnalyzer(db)

total_sum_of_items = pa.total_de_vendas_por_dia()
print(f'Total de vendas por dia: {total_sum_of_items}')

most_sold_product = pa.produto_mais_vendido()
print(f'Produto mais vendido: {most_sold_product}')

biggest_spender = pa.cliente_gastou_mais()
print(f'Cliente que mais gastou em uma única compra: nº{biggest_spender}')

products_sold_above_1_unit = pa.produtos_vendidos_acima_de_1_unidade()
print(f'Produtos vendidos acima de 1 unidades: {products_sold_above_1_unit}')

# Resultado de uma execução:

'''
Conectado ao banco de dados com sucesso!
Banco de dados resetado com sucesso!
Total de vendas por dia: 64
Produto mais vendido: Cerveja
Cliente que mais gastou em uma única compra: nº6
Produtos vendidos acima de 1 unidades: [{'descricao': 'Refrigerante', 'quantidade': 4}, {'descricao': 'Carne', 'quantidade': 2}, {'descricao': 'Cerveja', 'quantidade': 12}, {'descricao': 'Laranja', 'quantidade': 4}, {'descricao': 'Banana', 'quantidade': 4}, {'descricao': 'Tomate', 'quantidade': 2}, {'descricao': 'Mortadela', 'quantidade': 8}, {'descricao': 'Bolacha', 'quantidade': 6}, {'descricao': 'Sabonete', 'quantidade': 3}, {'descricao': 'Macarrão', 'quantidade': 4}, {'descricao': 'Maçã', 'quantidade': 3}, {'descricao': 'Detergente', 'quantidade': 2}]
'''
