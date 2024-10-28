Cassandra DB em ambiente local virtualizado com **Docker**.  
Container executado com comando **```docker compose up --build -d```** no arquivo `docker-compose.yml`.  

Especificamente **para este exemplo desconsidera-se o uso multi-nodal** do Cassandra. Para motivos de implementação facilitada, o exemplo utiliza apenas um container (serviço compose) executando a imagem `cassandra:latest`.

Script executado em um ambiente virtual **`Python 3.10.11`** para evitar o erro de incompatibilidade com o driver do Cassandra. Este erro ocorre devido à remoção do módulo `asyncore` na versão 3.12 do Python. 