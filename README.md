# S202-DB2

## running a mongoDB container
```bash
docker run --name mongodb -d -p 27017:27017 mongodb/mongodb-community-server:6.0-ubi8
```

## running a neo4j container
```bash
docker run --name neo4j -d -p 7474:7474 -p 7687:7687 neo4j
```
