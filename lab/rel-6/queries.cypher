// ----- CRIAÇÃO DE JURADOS, GAMES ----- //

CREATE(j:Jurado{nome:'Ewel'});
CREATE(j:Jurado{nome:'Gabriel'});
CREATE(j:Jurado{nome:'Davi'});

CREATE(g:Game{titulo:'League of Legends',genero:'MOBA',ano:2009});
CREATE(g:Game{titulo:'Minecraft',genero:'Sandbox',ano:2011});
CREATE(g:Game{titulo:'Phasmophobia',genero:'Terror',ano:2020});
CREATE(g:Game{titulo:'Warzone',genero:'Shooter',ano:2019});

CREATE(l:Loja{nome:'Steam'});
CREATE(l:Loja{nome:'Xbox'});
CREATE(l:Loja{nome:'Battlenet'});

// ----- RELAÇÃO ENTRE JURADOS E GAMES ----- //

MATCH(j:Jurado{nome:'Ewel'}),(g:Game{titulo:'Warzone'})
CREATE(j)-[:JOGOU{nota:10, horas:500}]->(g);

MATCH(j:Jurado{nome:'Ewel'}),(g:Game{titulo:'League of Legends'})
CREATE(j)-[:JOGOU{nota:10, horas: 1000}]->(g);

MATCH(j:Jurado{nome:'Gabriel'}),(g:Game{titulo:'Warzone'})
CREATE(j)-[:JOGOU{nota:6, horas: 156}]->(g);

MATCH(j:Jurado{nome:'Gabriel'}),(g:Game{titulo:'Minecraft'})
CREATE(j)-[:JOGOU{nota:10, horas: 200}]->(g);

MATCH(j:Jurado{nome:'Gabriel'}),(g:Game{titulo:'League of Legends'})
CREATE(j)-[:JOGOU{nota:9, horas: 10000}]->(g);

MATCH(j:Jurado{nome:'Davi'}),(g:Game{titulo:'Minecraft'})
CREATE(j)-[:JOGOU{nota:10, horas: 12000}]->(g);

MATCH(j:Jurado{nome:'Davi'}),(g:Game{titulo:'Phasmophobia'})
CREATE(j)-[:JOGOU{nota:5, horas: 2}]->(g);

// Diego Anestor Coutinho
// Exercícios S202

// ***** Elabore consultas em Neo4j para obter os seguintes resultados ***** //

// ----- Todos os registros do banco de dados ----- // tested, ok
MATCH (n) RETURN n;

// ----- Jogos lançados após o ano de 2012 ----- // tested, ok
MATCH (g:Game) WHERE g.ano > 2012 RETURN g;

// ----- Jogos do gênero de terror ----- // tested, ok
MATCH (g:Game) WHERE g.genero = 'Terror' RETURN g;

// ----- Jogos com uma nota igual ou maior que 7 ----- // tested, ok
MATCH (j:Jurado)-[r:JOGOU]->(g:Game) WHERE r.nota >= 7 RETURN j, r, g;

// ----- Acrescente quatro novos jogos ao banco de dados ----- // tested, ok
CREATE(g:Game{titulo:'Star Citizen', genero:'MMO', ano:2013});
CREATE(g:Game{titulo:'Heartbound', genero:'Adventure', ano:2018});
CREATE(g:Game{titulo:'Cities: Skylines', genero:'Simulation', ano:2015});

// ----- Adicione três novos jurados ao banco de dados ----- //
CREATE(j:Jurado{nome:'Jubsclayson'});
CREATE(j:Jurado{nome:'Avigaiudo'});
CREATE(j:Jurado{nome:'Omem'});

// ----- Estabeleça as relações entre os jurados e os jogos que eles avaliaram, incluindo a nota e a quantidade de horas jogadas ----- // tested, ok
MATCH(j:Jurado{nome:'Jubsclayson'}),(g:Game{titulo:'Star Citizen'})
CREATE(j)-[:JOGOU{nota:8, horas: 300}]->(g);

MATCH(j:Jurado{nome:'Jubsclayson'}),(g:Game{titulo:'Heartbound'})
CREATE(j)-[:JOGOU{nota:10, horas: 50}]->(g);

MATCH(j:Jurado{nome:'Avigaiudo'}),(g:Game{titulo:'Cities: Skylines'})
CREATE(j)-[:JOGOU{nota:9, horas: 200}]->(g);

MATCH(j:Jurado{nome:'Avigaiudo'}),(g:Game{titulo:'Minecraft'})
CREATE(j)-[:JOGOU{nota:10, horas: 300}]->(g);