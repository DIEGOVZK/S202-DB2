from funct import TryCatchAll, Listify


class Query(metaclass=TryCatchAll):
    def __init__(self, session):
        self.session = session

    def get_teacher(self, name):
        return self.session.run(
            "MATCH (t:Teacher {name: $name}) RETURN t.ano_nasc, t.cpf",
            name=name
        ).single()

    @Listify
    def get_teacher_starts(self, name):
        return self.session.run(
            "MATCH (t:Teacher) WHERE t.name STARTS WITH $name RETURN t.name, t.cpf",
            name=name
        )

    @Listify
    def get_all_city_names(self):
        return self.session.run(
            "MATCH (c:City) RETURN c.name"
        )

    @Listify
    def get_schools_between(self, min_number, max_number):
        return self.session.run(
            "MATCH (s:School) WHERE $min_number <= s.number <= $max_number RETURN s.name, s.address, s.number",
            min_number=min_number, max_number=max_number
        )

    def get_oldest_teacher(self):
        return self.session.run(
            "MATCH (t:Teacher) RETURN t.ano_nasc ORDER BY t.ano_nasc ASC LIMIT 1"
        ).single()

    def get_youngest_teacher(self):
        return self.session.run(
            "MATCH (t:Teacher) RETURN t.ano_nasc ORDER BY t.ano_nasc DESC LIMIT 1"
        ).single()

    def get_avg_population(self):
        return self.session.run(
            "MATCH (c:City) RETURN avg(c.population)"
        ).single()

    def get_city_sub_a(self, cep):
        return self.session.run(
            "MATCH (c:City {cep: $cep}) RETURN replace(c.name, 'a', 'A')",
            cep=cep
        ).single()

    @Listify
    def get_teacher_substring(self):
        return self.session.run(
            "MATCH (t:Teacher) RETURN substring(t.name, 3, 1)"
        )
