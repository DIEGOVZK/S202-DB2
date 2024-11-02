from funct import TryCatchAll, Listify


class TeacherCRUD(metaclass=TryCatchAll):
    def __init__(self, session):
        self.session = session

    def create(self, name, ano_nasc, cpf):
        self.session.run(
            "CREATE (t:Teacher {name: $name, ano_nasc: $ano_nasc, cpf: $cpf})",
            name=name, ano_nasc=ano_nasc, cpf=cpf
        )

    def read(self, name):
        return self.session.run(
            "MATCH (t:Teacher {name: $name}) RETURN t.ano_nasc, t.cpf",
            name=name
        ).single()

    def update(self, name, newCPF):
        self.session.run(
            "MATCH (t:Teacher {name: $name}) SET t.cpf = $newCPF",
            name=name, newCPF=newCPF
        )

    def delete(self, name):
        self.session.run(
            "MATCH (t:Teacher {name: $name}) DELETE t",
            name=name
        )
