# !* Desculpe pela formatação, autopep8 é um pouco agressivo
# !* primeiro teste rodando com sucesso
# !* segundo teste falhando, não pude identificar o motivo à tempo

from pymongo import MongoClient
from pymongo.server_api import ServerApi
from neo4j import GraphDatabase

# Adição pessoal
from functools import wraps

# Função própria para facilitar implementação
def tryCatchAbstract(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    return wrapper


class MongoDBCollection:
    '''
    Executado com Docker
    docker run --name mongodb -d -p 27017:27017 mongodb/mongodb-community-server:6.0-ubi8
    '''
    mongo_uri = "mongodb://localhost:27017"
    collection = None

    staticmethod

    def get_collection():
        if not MongoDBCollection.collection:
            client = MongoClient(MongoDBCollection.mongo_uri,
                                 server_api=ServerApi('1'))
            database = client.get_database('rpg')
            MongoDBCollection.collection = database.get_collection(
                'conhecimentos')
            MongoDBCollection.collection.delete_many({})
        return MongoDBCollection.collection


class Neo4jDriver:
    '''
    Executado com Docker
    docker run --name neo4j -d -p 7474:7474 -p 7687:7687 neo4j
    configurado no primeiro acesso para user: neo4j, password: 1234567890 
    '''
    neo4j_host = "neo4j://localhost:7687"
    neo4j_user = "neo4j"
    neo4j_password = "1234567890"

    driver = None

    staticmethod

    def get_driver():
        if not Neo4jDriver.driver:
            Neo4jDriver.driver = GraphDatabase.driver(Neo4jDriver.neo4j_host, auth=(
                Neo4jDriver.neo4j_user, Neo4jDriver.neo4j_password))
            Neo4jDriver.driver.execute_query("MATCH(n) DETACH DELETE n")
        return Neo4jDriver.driver


class Item:
    def __init__(self, name, price, weight):
        self.name = name
        self.price = price
        self.weight = weight

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "weight": self.weight,
        }


class Page:
    def __init__(self, title, description, characteristics=[]):
        self.title = title
        self.description = description
        self.characteristics = characteristics

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "characteristics": self.characteristics,
        }


class Character:
    def __init__(self, name, age, habilities, profession, culture, creation_date):
        self.name = name
        self.age = age
        self.habilities = habilities
        self.profession = profession
        self.culture = culture
        self.creation_date = creation_date

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "habilities": self.habilities,
            "profession": self.profession,
            "culture": self.culture,
            "creation_date": self.creation_date
        }


class ItemDAO:

    def __init__(self) -> None:
        self.mongo_collection = MongoDBCollection.get_collection()

    @tryCatchAbstract
    def add_item(self, item: Item):
        # -------------- Questão 1 A -------------- #
        item_dict = item.to_dict()
        result = self.mongo_collection.insert_one(item_dict)
        return result.inserted_id

    @tryCatchAbstract
    def get_available_itens(self, capacity, coins):
        # -------------- Questão 1 B -------------- #
        items = self.mongo_collection.find({
            "price": {"$lte": coins},
            "weight": {"$lte": capacity}
        }, {
            "name": 1,
            "price": 1,
            "_id": 0
        }).sort([
            ("price", 1),
            ("weight", 1)])
        return list(items)


class PageDAO:

    def __init__(self) -> None:
        self.neo4j_driver = Neo4jDriver.get_driver()

    @tryCatchAbstract
    def add_page(self, page: Page):
        # -------------- Questão 2 A -------------- #
        page_dict = page.to_dict()
        professions = page_dict.pop('professions', [])
        cultures = page_dict.pop('cultures', [])
        session = self.neo4j_driver.session()

        # Cria a página
        session.run(
            "CREATE (p:Page {title: $title, description: $description, characteristics: $characteristics})",
            title=page_dict['title'], description=page_dict['description'], characteristics=page_dict['characteristics']
        )

        # Cria as relacões com as profissões
        for profession in professions:
            session.run(
                "MATCH (p:Page {title: $page_title}), (pr:Profession {name: $profession_name}) CREATE (p)-[:KNOWN_BY_PROFESSION]->(pr)",
                page_title=page_dict['title'], profession_name=profession
            )

        # Cria as relações com as cultras
        for culture in cultures:
            session.run(
                "MATCH (p:Page {title: $page_title}), (c:Culture {name: $culture_name}) CREATE (p)-[:KNOWN_BY_CULTURE]->(c)",
                page_title=page_dict['title'], culture_name=culture
            )


class CharacterDAO:

    def __init__(self) -> None:
        self.neo4j_driver = Neo4jDriver.get_driver()

    @tryCatchAbstract
    # -------------- Questão 2 B -------------- #
    def add_character(self, character: Character):
        character_dict = character.to_dict()
        known_pages = character_dict.pop('known_pages', [])
        session = self.neo4j_driver.session()

        # Cria o nó do personem
        session.run(
            "CREATE (c:Character {name: $name, age: $age, habilities: $habilities, profession: $profession, culture: $culture, creation_date: $creation_date})",
            name=character_dict['name'], age=character_dict['age'], habilities=character_dict['habilities'], profession=character_dict[
                'profession'], culture=character_dict['culture'], creation_date=character_dict['creation_date']
        )

        # Cria as relações com as páginas conhecidas
        for page_title in known_pages:
            session.run(
                "MATCH (c:Charcter {name: $character_name}), (p:Page {title: $page_title}) CREATE (c)-[:KNOWS_PAGE]->(p)",
                character_name=character_dict['name'], page_title=page_title
            )

    @tryCatchAbstract
    # -------------- Questão 2 C -------------- #
    def get_knowledge(self, character_name):
        session = self.neo4j_driver.session()

        # Busca as páginas conhecidas pelo personagem
        result = session.run(
            "MATCH (c:Character {name: $character_name})-[:KNOWS_PAGE]->(p:Page) RETURN p.title AS title, p.description AS description",
            character_name=character_name
        )

        # Monta a lista de pginas conhecidas
        pages = []
        for record in result:
            pages.append({
                "title": record["title"],
                "description": record["description"]
            })
        return pages


item_dao = ItemDAO()
page_dao = PageDAO()
character_dao = CharacterDAO()

# Questão 1


def test_questao_1():

    items_data = [
        {"name": "Poção de cura", "price": 50, "weight": 500},
        {"name": "Adaga da noite", "price": 150, "weight": 350},
        {"name": "Bolsa de viagem", "price": 100, "weight": 600},
        {"name": "Escudo de ferro", "price": 200, "weight": 3000},
        {"name": "Espada longa", "price": 300, "weight": 4000},
        {"name": "Arco curto", "price": 120, "weight": 1200},
        {"name": "Flechas (20)", "price": 50, "weight": 800},
        {"name": "Capa de invisibilidade", "price": 500, "weight": 1000},
        {"name": "Botas do viajante", "price": 200, "weight": 800},
        {"name": "Corda de cânhamo (30 metros)", "price": 50, "weight": 3000},
        {"name": "Tocha", "price": 10, "weight": 400},
        {"name": "Mapa antigo", "price": 250, "weight": 50},
        {"name": "Martelo de guerra", "price": 350, "weight": 5000},
        {"name": "Elmo de aço", "price": 220, "weight": 1500},
        {"name": "Livro de magias", "price": 400, "weight": 1200},
        {"name": "Pó de fada", "price": 80, "weight": 50},
        {"name": "Armadura de couro", "price": 180, "weight": 3500},
        {"name": "Anel de proteção", "price": 600, "weight": 100},
        {"name": "Machado de batalha", "price": 400, "weight": 4500},
        {"name": "Grimório antigo", "price": 800, "weight": 1400}
    ]

    input_capacity = 3000
    input_coins = 250

    expected = [
        {"name": "Tocha", "price": 10},
        {"name": "Poção de cura", "price": 50},
        {"name": "Flechas (20)", "price": 50},
        {"name": "Corda de cânhamo (30 metros)", "price": 50},
        {"name": "Pó de fada", "price": 80},
        {"name": "Bolsa de viagem", "price": 100},
        {"name": "Arco curto", "price": 120},
        {"name": "Adaga da noite", "price": 150},
        {"name": "Botas do viajante", "price": 200},
        {"name": "Escudo de ferro", "price": 200},
        {"name": "Elmo de aço", "price": 220},
        {"name": "Mapa antigo", "price": 250}
    ]

    for item_data in items_data:
        item = Item(item_data['name'], item_data['price'], item_data['weight'])
        item_dao.add_item(item=item)

    output = item_dao.get_available_itens(
        capacity=input_capacity, coins=input_coins)

    assert expected == output


# Questão 2
def test_questao_2():

    pages_data = [
        {"title": "Uanteji",
         "description": "Uma organização secreta de mercenários, espiões e assassinos.",
         "characteristics": ["Ladino"]},

        {"title": "O culto do herói",
         "description": "Uma sociedade religiosa que segue os passos do Herói que salvou Granjaran dos sombrios.",
         "characteristics": ["Acadêmico", "Canalizador", "Aaron", "Eron"]},

        {"title": "A Guerra da Fé",
         "description": "Conflito que dizimou os Eron, deixando a Cidade Cinza em ruínas e marcando o início da supremacia teocrática do Culto do Herói.",
         "characteristics": ["Guerreiro", "Acadêmico", "Eron", "Aaron"]},

        {"title": "A Cidade Cinza",
         "description": "Antiga capital dos Eron, conhecida por sua grandeza arquitetônica e desenvolvimento arcano, agora abandonada e assombrada.",
         "characteristics": ["Acadêmico", "Eron", "Ladino", "Caçador"]},

        {"title": "A Grande Ilha de Grajatarur",
         "description": "Local de assentamento dos Eban após séculos de nomadismo. Centro de manufatura e comércio de artesanato do sul.",
         "characteristics": ["Comerciante", "Eban", "Canalizador"]},

        {"title": "O Vale da Morte",
         "description": "Um vale enevoado e sombrio, lar dos misteriosos Yuni, que caçam criaturas sombrias nas suas bordas.",
         "characteristics": ["Caçador", "Yuni"]},

        {"title": "Ruínas de Ynaia",
         "description": "Vestígios da antiga civilização Ynaia, espalhados pela costa leste, cheios de segredos e histórias misteriosas.",
         "characteristics": ["Ladino", "Ynaia", "Caçador"]},

        {"title": "Portoeste",
         "description": "A segunda maior cidade ativa, capital dos Uesto, sendo o principal polo comercial e marítimo do oeste.",
         "characteristics": ["Comerciante", "Uesto", "Guerreiro", "Ladino"]},

        {"title": "As Rotas dos Cem Rios",
         "description": "Rotas comerciais fluviais controladas pelos Nomi, ligando o sudoeste aos continentes logíquos.",
         "characteristics": ["Comerciante", "Nomi", "Ladino", "Caçador"]},

        {"title": "A Montanha Forja",
         "description": "A montanha onde os Hotan mineram e forjam os melhores metais e ferramentas do continente.",
         "characteristics": ["Canalizador", "Guerreiro", "Hotan", "Comerciante"]},

        {"title": "Os Boticários Ruchinos",
         "description": "Conhecidos pela ciência das plantas e cura, os Marruchi são os maiores boticários do continente, escondidos nas florestas do centro-oeste.",
         "characteristics": ["Acadêmico", "Marruchi", "Canalizador", "Caçador"]},

        {"title": "A Cidade de Heroica",
         "description": "A maior cidade do continente, lar dos Aaron e sede do poder teocrático do Culto do Herói.",
         "characteristics": ["Acadêmico", "Canalizador", "Aaron", "Guerreiro"]},

        {"title": "O Enclave Eban",
         "description": "Assentamentos Eban ao longo da Ilha de Grajatarur, focados na manufatura e comércio de objetos raros.",
         "characteristics": ["Comerciante", "Eban", "Canalizador"]},

        {"title": "O Mercado dos Nômades",
         "description": "Mercado itinerante dos Nomi, que viajam por toda a costa sul e fornecem mercadorias exóticas dos continentes logíquos.",
         "characteristics": ["Comerciante", "Nomi", "Ladino"]},

        {"title": "O Conselho dos Ferreiros Hotan",
         "description": "Grupo seleto de mestres ferreiros que governa as minas e as forjas nas montanhas do noroeste.",
         "characteristics": ["Hotan"]},

        {"title": "A Floresta Oculta",
         "description": "Território isolado e protegido pelos Ruchinos, que evitam contato com o resto do mundo.",
         "characteristics": ["Caçador", "Marruchi"]},

        {"title": "A Frota de Portoeste",
         "description": "A frota naval dos Uesto, que domina as rotas marítimas e garante o controle do comércio ocidental.",
         "characteristics": ["Comerciante", "Guerreiro", "Uesto"]},

        {"title": "Os Navios da Corda Nômade",
         "description": "Navios que ligam as rotas comerciais dos Nomi ao longo da costa sul, controlando o comércio de mercadorias raras.",
         "characteristics": ["Comerciante", "Nomi"]},

        {"title": "O Cerco dos Sombrios",
         "description": "O momento histórico em que o Herói e seus seguidores enfrentaram e derrotaram as forças sombrias que ameaçavam o continente.",
         "characteristics": ["Guerreiro", "Aaron", "Canalizador"]},

        {"title": "O Grande Templo da Espada de Heroica",
         "description": "O centro de adoração do Culto do Herói, uma imensa construção dedicada à fé e ao poder teocrático.",
         "characteristics": ["Acadêmico", "Canalizador", "Aaron"]},

        {"title": "A Expansão dos Uesto",
         "description": "O período em que os Uesto se consolidaram como a principal potência naval e comercial do oeste do continente.",
         "characteristics": ["Comerciante", "Uesto"]}
    ]

    characters_data = [
        {
            "name": "Amada Dormina",
            "age": 151,
            "habilities": ["Salto Dimensional", "Canalizar energia", "Criar dimensão"],
            "profession": ["Canalizador", "Acadêmico"],
            "culture": ["Eron", "Aaron"],
            "creation_date": "2024-09-30"
        },
        {
            "name": "Gareth'usto",
            "age": 38,
            "habilities": ["Navegação", "Comércio marítimo", "Liderança"],
            "profession": ["Comerciante", "Guerreiro"],
            "culture": ["Uesto"],
            "creation_date": "2024-09-30"
        },
        {
            "name": "Kalamimarruchi",
            "age": 26,
            "habilities": ["Herborismo", "Cura mágica", "Preparação de poções"],
            "profession": ["Acadêmico", "Canalizador"],
            "culture": ["Marruchi"],
            "creation_date": "2024-09-30"
        },
        {
            "name": "Varianel Martino",
            "age": 45,
            "habilities": ["Estrategista militar", "Manipulação da fé", "Liderança em batalha"],
            "profession": ["Guerreiro", "Acadêmico"],
            "culture": ["Aaron"],
            "creation_date": "2024-09-30"
        },
        {
            "name": "Ilona Grajatar",
            "age": 64,
            "habilities": ["Manufatura de joias", "Negociação", "Comércio intercontinental"],
            "profession": ["Comerciante", "Canalizador"],
            "culture": ["Eban"],
            "creation_date": "2024-09-30"
        },
        {
            "name": "Silar Eron",
            "age": 113,
            "habilities": ["Manipulação de magia arcana", "Estudo de artefatos antigos", "Criar golems"],
            "profession": ["Acadêmico", "Canalizador"],
            "culture": ["Eron"],
            "creation_date": "2024-09-30"
        },
        {
            "name": "Hildegar Bigorna",
            "age": 52,
            "habilities": ["Forjamento de armas", "Criação de armaduras"],
            "profession": ["Canalizador", "Guerreiro"],
            "culture": ["Hotan"],
            "creation_date": "2024-09-30"
        },
        {
            "name": "Velho Nim",
            "age": 31,
            "habilities": ["Liderança mercante", "Comércio entre reinos", "Navegação fluvial"],
            "profession": ["Comerciante", "Ladino"],
            "culture": ["Nomi"],
            "creation_date": "2024-09-30"
        },
        {
            "name": "Varyx Yuni",
            "age": 29,
            "habilities": ["Caça de criaturas das sombras", "Sobrevivência no Vale da Morte", "Camuflagem"],
            "profession": ["Caçador", "Ladino"],
            "culture": ["Yuni"],
            "creation_date": "2024-09-30"
        },
        {
            "name": "Thara Nala",
            "age": 54,
            "habilities": ["Historiadora de ruínas", "Navegação costeira", "Pesca"],
            "profession": ["Acadêmico", "Comerciante"],
            "culture": ["Ynaia"],
            "creation_date": "2024-09-30"
        }
    ]

    input_character_name = "Varianel Martino"
    expected = [
        {"title": "O culto do herói",
         "description": "Uma sociedade religiosa que segue os passos do Herói que salvou Granjaran dos sombrios."},

        {"title": "A Guerra da Fé",
         "description": "Conflito que dizimou os Eron, deixando a Cidade Cinza em ruínas e marcando o início da supremacia teocrática do Culto do Herói."},

        {"title": "A Cidade Cinza",
         "description": "Antiga capital dos Eron, conhecida por sua grandeza arquitetônica e desenvolvimento arcano, agora abandonada e assombrada."},

        {"title": "Portoeste",
         "description": "A segunda maior cidade ativa, capital dos Uesto, sendo o principal polo comercial e marítimo do oeste."},

        {"title": "A Montanha Forja",
         "description": "A montanha onde os Hotan mineram e forjam os melhores metais e ferramentas do continente."},

        {"title": "Os Boticários Ruchinos",
         "description": "Conhecidos pela ciência das plantas e cura, os Marruchi são os maiores boticários do continente, escondidos nas florestas do centro-oeste."},

        {"title": "A Cidade de Heroica",
         "description": "A maior cidade do continente, lar dos Aaron e sede do poder teocrático do Culto do Herói."},

        {"title": "A Frota de Portoeste",
         "description": "A frota naval dos Uesto, que domina as rotas marítimas e garante o controle do comércio ocidental."},

        {"title": "O Cerco dos Sombrios",
         "description": "O momento histórico em que o Herói e seus seguidores enfrentaram e derrotaram as forças sombrias que ameaçavam o continente."},

        {"title": "O Grande Templo da Espada de Heroica",
         "description": "O centro de adoração do Culto do Herói, uma imensa construção dedicada à fé e ao poder teocrático."}
    ]

    for page_data in pages_data:
        page = Page(
            page_data['title'], page_data['description'], page_data['characteristics'])
        page_dao.add_page(page)

    for character_data in characters_data:
        character = Character(character_data['name'], character_data['age'], character_data['habilities'],
                              character_data['profession'], character_data['culture'], character_data['creation_date'])
        character_dao.add_character(character)

    output = character_dao.get_knowledge(character_name=input_character_name)

    assert sorted(expected, key=lambda d: d['title']) == sorted(
        output, key=lambda d: d['title'])